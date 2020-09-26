import logging
import json

from flask import request, jsonify
import math
from codeitsuisse import app
from itertools import combinations as C

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def revisitGeo():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    horizontal = False
    d_shape = data.get('shapeCoordinates')
    d_line = data.get('lineCoordinates')
    if d_line[0]['x']==d_line[1]['x']:
        horizontal = True
    m_line = ((d_line[0]['y']-d_line[1]['y'])/(d_line[0]['x']-d_line[1]['x']))
    c_line = d_line[1]['y'] - (m_line * d_line[1]['x'])
    print('line', m_line,c_line)

    def find_intercept(c):
        if d_shape[c[0]]['x'] != d_shape[c[1]]['x']:
            m_shape = (d_shape[c[0]]['y']-d_shape[c[1]]['y'])/(d_shape[c[0]]['x']-d_shape[c[1]]['x'])
            if m_shape == m_line:
                return
            c_shape = d_shape[c[0]]['y'] - m_shape * d_shape[c[0]]['x']

            if horizontal:
                x_cood = d_line[0]['x']
                y_cood = m_shape * x_cood + c_shape
            else:
                x_cood = -(c_shape - c_line) / (m_shape - m_line)
                y_cood = m_line * x_cood + c_line

        else:
            x_cood = d_shape[c[0]]['x']
            y_cood = m_line * x_cood + c_line

        if not min(d_shape[c[0]]['x'],d_shape[c[1]]['x']) <= x_cood <= max(d_shape[c[0]]['x'],d_shape[c[1]]['x']):
            return
        if not min(d_shape[c[0]]['y'], d_shape[c[1]]['y']) <= y_cood <= max(d_shape[c[0]]['y'],d_shape[c[1]]['y']):
            return

        if math.floor(x_cood) == math.ceil(x_cood):
            x_cood = int(x_cood)
        if math.floor(y_cood) == math.ceil(y_cood):
            y_cood = int(y_cood)

        return {'x':round(x_cood, 2), 'y':round(y_cood, 2)}

    for c in [(x,x+1)for x in range(len(d_shape)-1)]+[(0, len(d_shape)-1)]:
        a = (find_intercept(c))
        if a:
            print(c)
            ans.append(a)

    logging.info("My result :{}".format(ans))
    return json.dumps(ans)
