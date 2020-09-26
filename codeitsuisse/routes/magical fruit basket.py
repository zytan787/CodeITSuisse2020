import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))
    count = 0
    data = json.loads(data)
    for key in data:
        count += data[key]
    result = count * 10
    logging.info("My result :{}".format(result))
    return jsonify(result)



