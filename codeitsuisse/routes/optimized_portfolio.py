import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def round_acc(num, decimals=0):
    multiplier = 10 ** decimals
    if decimals == 0:
        return math.floor(num * multiplier + 0.5) // multiplier
    else:
        return math.floor(num * multiplier + 0.5) / multiplier


def round_up(num, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(num * multiplier) / multiplier


def optimal_hedge_ratio(cc, std_spot, std_future):
    return round_acc(cc * std_spot / std_future, 3)


def num_future_contract(ohr, pf_value, future_price, notional):
    return round_acc(ohr * pf_value / future_price / notional)


def best_future(portfolio):
    value = portfolio['Portfolio']['Value']
    s_std = portfolio['Portfolio']['SpotPrcVol']
    best = dict()
    min_ohr = dict()
    min_f_std = dict()
    min_nfc = dict()
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
            # "f_std": f_std
        }
        # print(best[name])
        if opt_hr in min_ohr:
            min_ohr[opt_hr] += [name]
        else:
            min_ohr[opt_hr] = [name]
        if f_std in min_f_std:
            min_f_std[f_std] += [name]
        else:
            min_f_std[f_std] = [name]
        if nfc in min_nfc:
            min_nfc[nfc] += [name]
        else:
            min_nfc[nfc] = [name]

    min_ohr = min_ohr[min(min_ohr.keys())]
    min_f_std = min_f_std[min(min_f_std.keys())]
    min_nfc = min_nfc[min(min_nfc.keys())]

    keys = set(min_ohr).intersection(set(min_f_std))
    if len(keys) == 0:
        return best[min_nfc[0]]
    else:
        key = min(keys, key=lambda x: best[x]['NumFuturesContract'])
        return best[key]


@app.route('/optimizedportfolio', methods=['POST'])
def optimizedPortfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs")

    # best_pf_future = dict()
    # for pf in inputs:
    #     best_f = best_future(pf)
    #     if pf['Portfolio']['Name'] not in best_pf_future:
    #         best_pf_future[pf['Portfolio']['Name']] = best_f
    #     else:
    #         cur_best_f = best_pf_future[pf['Portfolio']['Name']]
    #         if best_f['OptimalHedgeRatio'] < cur_best_f['OptimalHedgeRatio'] and best_f['f_std'] < cur_best_f['f_std']:
    #             best_pf_future[pf['Portfolio']['Name']] = best_f
    #         elif best_f['OptimalHedgeRatio'] >= cur_best_f['OptimalHedgeRatio'] and best_f['f_std'] >= cur_best_f['f_std']:
    #             continue
    #         elif best_f['NumFuturesContract'] < cur_best_f['NumFuturesContract']:
    #             best_pf_future[pf['Portfolio']['Name']] = best_f
    # outputs = list()
    # for v in best_pf_future.values():
    #     v.pop("f_std")
    #     outputs.append(v)

    outputs = {'outputs': [best_future(pf) for pf in inputs]}
    logging.info("My result :{}".format(outputs))
    return json.dumps(outputs)



