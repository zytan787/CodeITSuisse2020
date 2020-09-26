import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n_apple = data.get("maApple")
    n_watermelon = data.get("maWatermelon")
    n_banana = data.get("maBanana")
    result = (n_apple + n_watermelon + n_banana) * 50
    logging.info("My result :{}".format(result))
    return jsonify(result)



