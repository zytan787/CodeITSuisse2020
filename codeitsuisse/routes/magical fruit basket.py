import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))
    weight = 0
    data = json.loads(data)
    for key in data:
        if key == "maPomegranate":
            weight += data[key] * 20
        elif key == "maRamubutan":
            weight += data[key] * 15
        elif key == "maAvocado":
            weight += data[key] * 10
        elif key == "maWatermelon":
            weight += data[key] * 60    
        elif key == "maApple":
            weight += data[key] * 20
        elif key == "maPineapple":
            weight += data[key] * 80
    result = weight
    logging.info("My result :{}".format(result))
    return jsonify(result)



