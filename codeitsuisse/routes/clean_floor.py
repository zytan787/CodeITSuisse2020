import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def clean(arr):
    # ans = 0
    # for i in range(len(arr)-2):
    #     if arr[i] == 0:
    #         continue
    #     _sum = arr[i] + arr[i+1]
    #     _diff = arr[i] - arr[i+1]
    #     arr[i] = 0
    #     if _diff == 0:
    #         if _sum % 2 == 0:
    #             steps = _sum + 1
    #         else:
    #             steps = _sum
    #     elif _diff > 0:
    #         if _diff % 2 != 0:
    #             steps = _sum + _diff + 1
    #         else:
    #             steps = _sum + _diff
    #     elif _diff < 0:
    #         if abs(_diff) % 2 != 0:
    #             steps = _sum + abs(_diff) - 1
    #         else:
    #             steps = _sum + abs(_diff)

    #     ans += steps
    #     arr[i+1] = steps % 2 == 0

    # _sum = arr[-2] + arr[-1]
    # _diff = arr[-2] - arr[-1]

    # if _diff == 0:
    #     steps = _sum
    # elif _diff > 0:
    #     if _diff % 2 != 0:
    #         steps = _sum + _diff + 1
    #     else:
    #         steps = _sum + _diff
    # elif _diff < 0:
    #     if abs(_diff) % 2 != 0:
    #         steps = _sum + abs(_diff) - 1
    #     else:
    #         steps = _sum + abs(_diff)

    # ans += steps

    ans = 0
    i = 1
    n = len(arr)
    right = True
    while i < n:
        if arr.count(0) == n:
            break
        if i != n-1 and arr[i+1] == 0:
            if right:
                i -= 1
                right = False
            else:
                i += 1
                right = True
        if arr[i] == 0:
            arr[i] = 1
            i += 1
        else:
            arr[i] -= 1
            if arr[i] == 0:
                if right:
                    i -= 1
                    right = False
                else:
                    i += 1
                    right = True
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



