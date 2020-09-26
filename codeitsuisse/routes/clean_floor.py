import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

move = 0


def make_move(arr, new_pos):
    global move
    move += 1
    if arr[new_pos] == 0:
        arr[new_pos] = 1
        return 1
    else:
        arr[new_pos] -= 1
        return -1


def clean(arr):
    global move
    move = 0
    n = len(arr)

    # get the last tile with dirt
    last = n - 1
    while last > 0 and arr[last] == 0:
        last -= 1

    dirt = sum(arr)
    for i in range(1, last + 1):
        dirt += make_move(arr, i)
        print(arr)

    pos = last
    while dirt > 0:
        if pos + 1 < n and arr[pos + 1] > 0:
            pos += 1
        else:
            pos -= 1
        dirt += make_move(arr, pos)
        print(arr)


@app.route('/clean_floor', methods=['POST'])
def cleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("tests")
    result = dict()
    for k, v in inputValue.items():
        clean(v['floor'])
        result[k] = move
    logging.info("My result :{}".format(result))
    return json.dumps({"answers": result})



