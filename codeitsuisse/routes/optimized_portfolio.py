import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def optimal_hedge_ratio(cc, std_spot, std_future):
    return round(cc * std_spot / std_future, 3)


def num_future_contract(ohr, pf_value, future_price, notional):
    return round(ohr * pf_value / notional / future_price)


def best_future(portfolio):
    value = portfolio['Portfolio']['Value']
    s_std = portfolio['Portfolio']['SpotPrcVol']
    best = dict()
    for future in portfolio['IndexFutures']:
        name = future['Name']
        corr_coef = future['CoRelationCoefficient']
        f_std = future['FuturePrcVol']
        f_price = future['IndexFuturePrice']
        notion = future['Notional']
        opt_hr = optimal_hedge_ratio(corr_coef, s_std, f_std)
        if len(best) == 0 or \
                opt_hr < best['OptimalHedgeRatio'] and f_std < best['f_std']:
            nfc = num_future_contract(opt_hr, value, f_price, notion)
            best["HedgePositionName"] = name
            best["OptimalHedgeRatio"] = opt_hr
            best["NumFuturesContract"] = nfc
            best["f_std"] = f_std
        elif opt_hr == best['OptimalHedgeRatio'] and f_std == best['f_std']:
            nfc = num_future_contract(opt_hr, value, f_price, notion)
            if nfc < best['NumFuturesContract']:
                best["HedgePositionName"] = name
                best["OptimalHedgeRatio"] = opt_hr
                best["NumFuturesContract"] = nfc
                best["f_std"] = f_std
    best.pop('f_std', None)
    return best


@app.route('/optimizedportfolio', methods=['POST'])
def optimizedPortfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs")
    outputs = {'outputs': [best_future(pf) for pf in inputs]}
    logging.info("My result :{}".format(outputs))
    return json.dumps(outputs)



