import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def slsm(boardSize, player, jumps):
    board = [i for i in range(boardSize + 1)]
    ans = []

    for jump in jumps:
        temp = jump.split(":")
        if int(temp[0]) == 0:
            board[int(temp[1])] = '+'
        elif int(temp[1]) == 0:
            board[int(temp[0])] = '-'
        elif int(temp[0]) > int(temp[1]):
            board[int(temp[1])] = int(temp[0])
        elif int(temp[0]) < int(temp[1]):
            board[int(temp[0])] = int(temp[1])
    print(board)

    def findmax(k):
        from_mirror = False
        mx = 0
        mx_ind = -1
        next6 = board[k + 1:k + 1 + 6]
        for i, x in enumerate(next6):
            if x != '+' and x != '-' and x > mx:
                mx = x
                mx_ind = i + 1
                from_mirror = False
            if x == '+':
                for j, y in enumerate(board[i + k + 1:i + k + 1 + 6]):
                    if y != '+' and y != '-' and y > mx:
                        print(y)
                        mx = y
                        mx_ind = j
                        prev_ind = i + 1
                        from_mirror = True

        if from_mirror:
            return [[prev_ind, mx_ind], mx]
        else:
            return [[mx_ind], mx]

    def findmin(k):
        mn = 100000
        mn_ind = 0
        for i, x in enumerate(board[k + 1:k + 1 + 6]):
            if x != '+' and x != '-' and x < mn:
                mn = x
                mn_ind = i + 1
        return [[mn_ind], mn]

    x = 1
    y = 1
    shortest_path = []

    while x != boardSize:
        best_choice_l = findmin(y)
        for _ in range(player - 1):
            shortest_path.extend(best_choice_l[0])
        y = best_choice_l[1]

        best_choice = findmax(x)
        shortest_path.extend(best_choice[0])
        x = best_choice[1]
        ans.append(x)
    print(ans)
    return shortest_path

    # board = [0 for i in range(boardSize+1)]
    #
    # for jump in jumps:
    #     temp = jump.split(":")
    #     if int(temp[0]) == 0:
    #         board[int(temp[1])] = float("inf")
    #     elif int(temp[1]) == 0:
    #         board[int(temp[0])] = -float("inf")
    #     else:
    #         board[int(temp[0])] = int(temp[1]) - int(temp[0])
    #
    # rolls = []
    # positions = [1 for i in range(players)]
    #
    # while positions[-1] != boardSize:
    #     for i in range(players-1):
    #         die = 1
    #         while die <= 6:
    #             if positions[i] + die > boardSize:
    #                 break
    #             value = board[positions[i] + die]
    #             if value > 0:
    #                 die += 1
    #                 continue
    #             elif value == -float("inf"):
    #                 rolls.append(die)
    #                 rolls.append(6)
    #                 positions[i] += die
    #                 positions[i] -= 6
    #                 break
    #             elif value < 0:
    #                 rolls.append(die)
    #                 positions[i] += die
    #                 positions[i] -= value
    #                 break
    #             else:
    #                 rolls.append(die)
    #                 positions[i] += die
    #                 break
    #
    #     max_jump = -1
    #     max_die = 1
    #     mirror = False
    #     smoke = False
    #     for die in range(1,7):
    #         if positions[-1] + die > boardSize:
    #             break
    #         value = board[positions[-1] + die]
    #         if value <= 0:
    #             if value != -float("inf"):
    #                 if die + value > max_jump:
    #                     max_jump = die + value
    #                     max_die = die
    #                     mirror = False
    #                     smoke = False
    #             else:
    #                 if die - 1 > max_jump:
    #                     max_jump = die - 1
    #                     max_die = die
    #                     mirror = False
    #                     smoke = True
    #         elif value > 0:
    #             if value != float("inf"):
    #                 if die + value > max_jump:
    #                     max_jump = die + value
    #                     max_die = die
    #                     mirror = False
    #                     smoke = False
    #             else:
    #                 if die + 6 > max_jump:
    #                     max_jump = die + 6
    #                     max_die = die
    #                     mirror = True
    #                     smoke = False
    #
    #     if not mirror and not smoke:
    #         rolls.append(max_die)
    #         positions[-1] += max_jump
    #     elif smoke:
    #         rolls.append(max_die)
    #         rolls.append(1)
    #         positions[-1] += max_jump
    #     elif mirror:
    #         rolls.append(max_die)
    #         rolls.append(6)
    #         positions[-1] += max_jump
    #
    # return rolls

@app.route('/slsm', methods=['POST'])
def evaluateSlsm():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    boardSize = data.get("boardSize")
    players = data.get("players")
    jumps = data.get("jumps")
    result = slsm(boardSize, players, jumps)
    logging.info("My result :{}".format(result))
    return jsonify(result)



