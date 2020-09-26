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
    min_ohr = None
    min_f_std = None
    min_nfc = None
    for future in portfolio['IndexFutures']:
        name = future['Name']
        corr_coef = future['CoRelationCoefficient']
        f_std = future['FuturePrcVol']
        f_price = future['IndexFuturePrice']
        notion = future['Notional']
        opt_hr = optimal_hedge_ratio(corr_coef, s_std, f_std)
        nfc = num_future_contract(opt_hr, value, f_price, notion)
        best[name] = {
            "HedgePositionName": name,
            "OptimalHedgeRatio": opt_hr,
            "NumFuturesContract": nfc,
            "f_std": f_std
        }
        if min_ohr is None or opt_hr < min_ohr[0]:
            min_ohr = (opt_hr, name)
        if min_f_std is None or f_std < min_f_std[0]:
            min_f_std = (f_std, name)
        if min_nfc is None or nfc < min_nfc[0]:
            min_nfc = (nfc, name)

    if min_ohr[1] == min_f_std[1]:
        best[min_ohr[1]].pop('f_std', None)
        return best[min_ohr[1]]
    else:
        best[min_nfc[1]].pop('f_std', None)
        return best[min_nfc[1]]


@app.route('/optimizedportfolio', methods=['POST'])
def optimizedPortfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs")
    outputs = {'outputs': [best_future(pf) for pf in inputs]}
    logging.info("My result :{}".format(outputs))
    return json.dumps(outputs)



