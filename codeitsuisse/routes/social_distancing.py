import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def c(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n - r)


def num_ways(seats, people, space):
    holes = people + 1
    seat_left = seats - people - space * (people - 1)
    if seat_left == 0:
        return 1
    total = 0
    for i in range(1, min(holes, seat_left) + 1):
        total += c(holes, i) * c(seat_left - 1, i - 1)
    return total


@app.route('/social_distancing', methods=['POST'])
def socialDistancing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get('tests')
    result = {'answers': dict()}
    for k, v in tests.items():
        result['answers'][k] = num_ways(v['seats'], v['people'], v['spaces'])
    logging.info("My result :{}".format(result))
    return json.dumps(result)



