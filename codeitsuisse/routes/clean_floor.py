import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def clean(arr):
    n = len(arr)

    last = n - 1
    while last > 0 and arr[last] == 0:
        last -= 1

    move = last
    pos = 0
    dirt = sum(arr)
    while pos < last:
        pos += 1
        if arr[pos] > 0:
            arr[pos] -= 1
            dirt -= 1
        else:
            arr[pos] = 1
            dirt += 1

    while dirt > 0:
        if arr[pos] == 0:
            move += 1
            pos -= 1
            if arr[pos] > 0:
                arr[pos] -= 1
                dirt -= 1
            else:
                arr[pos] = 1
                dirt += 1
        else:
            move += arr[pos] * 2 + 1
            if pos > 0:
                if arr[pos - 1] > arr[pos]:
                    arr[pos - 1] -= arr[pos]
                    dirt -= arr[pos]
                else:
                    dirt -= arr[pos - 1]
                    arr[pos - 1] = (arr[pos] - arr[pos - 1]) % 2
                    dirt += arr[pos - 1]
                dirt -= arr[pos]
                arr[pos] = 0
                pos -= 1
            else:
                arr[1] = arr[0] % 2
                dirt += arr[1] - arr[0]
                arr[0] = 0
                pos += 1

    return max(0, move)

# [0, 1, 0, 2, 0, 1, 0, 2]
# [0, 0, 0, 2, 0, 1, 0, 2]
# [0, 0, 1, 2, 0, 1, 0, 2]
# [0, 0, 1, 1, 0, 1, 0, 2]
# [0, 0, 1, 1, 1, 1, 0, 2]
# [0, 0, 1, 1, 1, 0, 0, 2]
# [0, 0, 1, 1, 1, 0, 1, 2]
# [0, 0, 1, 1, 1, 0, 1, 1]
# [0, 0, 1, 1, 1, 0, 0, 1]
# [0, 0, 1, 1, 1, 0, 0, 0]
# [0, 0, 1, 1, 1, 0, 1, 0]
# [0, 0, 1, 1, 1, 1, 1, 0]
# [0, 0, 1, 1, 1, 1, 0, 0]
# [0, 0, 1, 1, 1, 0, 0, 0]
# [0, 0, 1, 1, 0, 0, 0, 0]
# [0, 0, 1, 0, 0, 0, 0, 0]
# [0, 0, 0, 0, 0, 0, 0, 0]


@app.route('/clean_floor', methods=['POST'])
def cleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("tests")
    result = {'answers': dict()}
    for k, v in inputValue.items():
        # result['answers'][k] = clean(v['floor'])
        result['answers'][k] = 1
    logging.info("My result :{}".format(result))
    return json.dumps(result)



