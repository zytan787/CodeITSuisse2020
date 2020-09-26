import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def clean(arr):
    ans = 0
    current_position = 0
    n = len(arr)

    while not all(v == 0 for v in arr):
        if current_position == 0:
            current_position += 1
            arr[current_position] = 1 if arr[current_position] == 0 else arr[current_position] - 1
        elif current_position == n - 1:
            current_position -= 1
            arr[current_position] = 1 if arr[current_position] == 0 else arr[current_position] - 1
        else:
            if arr[i-1] > arr[i+1]:
                current_position -= 1
                arr[current_position] = 1 if arr[current_position] == 0 else arr[current_position] - 1
            else:
                current_position += 1
                arr[current_position] = 1 if arr[current_position] == 0 else arr[current_position] - 1
        ans += 1

    return ans
            
            


# def update_pos(arr, pos):
#     if arr[pos] == 0:
#         arr[pos] = 1
#         return 1
#     else:
#         arr[pos] -= 1
#         return -1


# def clean(arr):
#     n = len(arr)

#     last = n - 1
#     while last > 0 and arr[last] == 0:
#         last -= 1

#     move = last
#     pos = 0
#     dirt = arr[0]
#     while pos < last:
#         pos += 1
#         update_pos(arr, pos)
#         dirt += arr[pos]

#     while dirt > 0:
#         if arr[pos] == 0:
#             move += 1
#             pos -= 1
#             dirt += update_pos(arr, pos)
#         else:
#             move += 2 * arr[pos]
#             if pos > 0:
#                 if arr[pos - 1] > arr[pos]:
#                     arr[pos - 1] -= arr[pos]
#                     dirt -= 2 * arr[pos]
#                     arr[pos] = 0
#                 else:
#                     dirt -= arr[pos - 1]
#                     arr[pos - 1] = (arr[pos] - arr[pos - 1]) % 2
#                     dirt -= arr[pos]
#                     dirt += arr[pos - 1]
#                 if dirt > 0:
#                     pos -= 1
#                     move += 1
#                     dirt += update_pos(arr, pos)
#             else:
#                 arr[1] = arr[0] % 2
#                 dirt -= arr[0]
#                 dirt += arr[1]
#                 if dirt > 0:
#                     move += 1
#                     break

#     return max(0, move)

# {
#   "tests": {
#         "0": {
#       "floor":[0, 1]
#     },
#     "1": {
#       "floor":[1, 1]
#     },
#     "2": {
#         "floor": [0, 1, 0, 2, 0, 1, 0, 2]
#     },
#     "3": {
#         "floor":[2, 1, 4]
#     },
#     "4": {
#         "floor": [1, 4, 3, 1]
#     },
#     "5": {
#         "floor": [1, 2, 3, 2, 1]
#     },
#     "6": {
#         "floor": [5, 4, 3, 2, 1]
#     }
#   }
# }


@app.route('/clean_floor', methods=['POST'])
def cleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("tests")
    result = {'answers': dict()}
    for k, v in inputValue.items():
        result['answers'][k] = clean(v['floor'])
    logging.info("My result :{}".format(result))
    return json.dumps(result)



