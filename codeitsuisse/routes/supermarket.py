import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def solve_maze(m, s, e, r, c, steps=1):
    if s == e:
        return steps
    elif m[s[0]][s[1]] == 'X':
        return None
    m[s[0]][s[1]] = steps
    above, below, left, right = None, None, None, None
    if s[0] > 0 and m[s[0] - 1][s[1]] != 'X' and m[s[0] - 1][s[1]] == 0:
        above = solve_maze(m, (s[0] - 1, s[1]), e, r, c, steps=steps + 1)
    if s[0] < r - 1 and m[s[0] + 1][s[1]] != 'X' and m[s[0] + 1][s[1]] == 0:
        below = solve_maze(m, (s[0] + 1, s[1]), e, r, c, steps=steps + 1)
    if s[1] > 0 and m[s[0]][s[1] - 1] != 'X' and m[s[0]][s[1] - 1] == 0:
        left = solve_maze(m, (s[0], s[1] - 1), e, r, c, steps=steps + 1)
    if s[1] < c - 1 and m[s[0]][s[1] + 1] != 'X' and m[s[0]][s[1] + 1] == 0:
        right = solve_maze(m, (s[0], s[1] + 1), e, r, c, steps=steps + 1)
    if above is not None:
        return above
    elif below is not None:
        return below
    elif left is not None:
        return left
    elif right is not None:
        return right
    else:
        return None

@app.route('/supermarket', methods=['POST'])
def supermarketMaze():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    ans = {
        'answers': dict()
    }
    for k, test in tests.items():
        maze = test['maze']
        row = len(maze)
        col = len(maze[0])
        for i in range(row):
            for j in range(col):
                if maze[i][j] == 1:
                    maze[i][j] = 'X'
        start = tuple(test['start'][::-1])
        end = tuple(test['end'][::-1])
        res = solve_maze(maze, start, end, row, col)
        ans['answers'][k] = res if res is not None else -1
    logging.info("My result :{}".format(ans))
    return json.dumps(ans)



