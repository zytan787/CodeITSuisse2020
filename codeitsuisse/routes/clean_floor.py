import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def clean(arr):
    ans = 0
    n = len(arr)
    if arr[0] > 0:
        value = arr[0]
        ans += value * 2
        if arr[0] == arr[1]:
            arr[1] = 0
        else:
            arr[1] -= abs(arr[1] - arr[0])
        if arr[1] < 0:
            arr[1] = abs(arr[1]) % 2 == 0

    for i in range(1, n-1):
        ans += 1
        if arr[i] == 0:
            arr[i] = 1
        else:
            arr[i] -= 1
        value = arr[i]
        ans += value * 2
        if arr[i] == arr[i+1]:
            arr[i+1] = 0
        else:
            arr[i+1] -= abs(arr[i+1] - arr[i])
        if arr[i+1] < 0:
            arr[i+1] = abs(arr[i+1]) % 2 == 0

    if arr[-1] > 0:
        if arr[-1] % 2 == 0:
            ans += arr[-1] * 2
        else:
            ans += arr[-1] * 2 - 1
    return ans

    # ans = 0
    # i = 1
    # n = len(arr)
    # right = True
    # while i < n:
    #     print(i)
    #     if arr.count(0) == n:
    #         break
    #     if i != n-1 and arr[i+1] == 0:
    #         if right:
    #             i -= 1
    #             right = 0
    #         else:
    #             i += 1
    #             right = True
    #     if arr[i] == 0:
    #         arr[i] = 1
    #         if right and i < n-1:
    #             i += 1
    #         else:
    #             i -= 1
    #             right = False
    #     else:
    #         arr[i] -= 1
    #         if arr[i] == 0:
    #             if right:
    #                 i -= 1
    #                 right = False
    #             else:
    #                 i += 1
    #                 right = True
    #         else:
    #             if right and i < n-1:
    #                 i += 1
    #             else:
    #                 i -= 1
    #                 right = False
    #     ans += 1

    # ans = 0
    # n = len(arr)
    # current_position = 0
    # count = arr.count(0)
    # while(count < n):
    #     if current_position == 0:
    #         current_position += 1
    #     elif current_position == n-1:
    #         current_position -= 1
    #     else:
    #         if arr[current_position-1] > arr[current_position+1]:
    #             current_position -= 1
    #         else:
    #             current_position += 1

    #     arr[current_position] = 1 if arr[current_position] == 0 else arr[current_position] - 1
    #     if arr[current_position] == 0:
    #         count += 1
    #     ans += 1

    # return ans
            
            


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
    return jsonify(result)



