import logging
import json

from flask import request, jsonify

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def cluster():
    grid = request.get_json()
    logging.info("data sent for evaluation {}".format(grid))
    ans = {}
    def count_cluster(a):
        ct = 0
        direction = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        while a:
            x = 0
            stack = [a[x]]
            while stack:
                ptr = stack.pop(-1)
                if ptr in a:
                    a.remove(ptr)
                for d in direction:
                    x1 = ptr[0] + d[0]
                    y1 = ptr[1] + d[1]
                    if [x1, y1] in a:
                        stack.append([x1, y1])
                        a.remove([x1, y1])
            ct += 1
        return ct

    q = []
    uninfected = 0
    new_infected = []
    direction = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            if y == '1':
                q.append([i, j])

            elif y == '0':
                uninfected += 1
    if not uninfected:
        ans["answer"] = len(q)
        logging.info("My result :{}".format(ans))
        return jsonify(ans)

    while q:
        ptr = q.pop(0)
        new_infected.append(ptr)
        for d in direction:
            x = ptr[0] + d[0]
            y = ptr[1] + d[1]
            # print(x,y)
            if x >= len(grid) or x < 0 or y >= len(grid[0]) or y < 0 or grid[x][y] != '0':
                continue
            q.append([x, y])
            grid[x][y] = '1'

    for x in grid:
        print(x)
    ans["answer"] = count_cluster(new_infected)

    logging.info("My result :{}".format(ans))
    return jsonify(ans)