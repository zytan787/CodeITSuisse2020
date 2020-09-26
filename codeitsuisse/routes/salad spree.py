import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_salads")
    lst = data.get("salad_prices_street_map")
    min_price = float('inf')
    price = 0

    for shop in lst:
        for i in range(len(shop)-n+1):
            if "X" in shop[i:i+n]:
                continue
            else:
                price = sum(list(int(num) for num in shop[i:i+n]))
                min_price = min(min_price, price)

    result = {"result": 0 if min_price == float('inf') else min_price}
    logging.info("My result :{}".format(result))
    return json.dumps(result)



