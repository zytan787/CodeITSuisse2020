import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def compare(a, b):
    num_first = 0
    num_different = 0
    ag, bg = a["genome"].replace("-", ""), b["genome"].replace("-", "")
    for i, (x, y) in enumerate(zip(ag, bg)):
        if x != y:
            num_different += 1
            if i % 3 == 0:
                num_first += 1
    return a["name"], b["name"], num_different, num_first


@app.route('/contact_trace', methods=['POST'])
def contactTracing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    infected = data.get("infected")
    origin = data.get("origin")
    cluster = data.get("cluster")

    pp = list()

    iname, oname, d, f = compare(infected, origin)
    origin_linked = False
    if len(cluster) > 0:
        if d == 0:
            pp.append(iname + " -> " + oname)
            origin_linked = True
    else:
        if f > 1:
            pp.append(iname + "* -> " + oname)
        else:
            pp.append(iname + " -> " + oname)

    cpaths = dict()
    opaths = dict()
    for c in cluster:
        _, cname, d, f = compare(infected, c)
        if d in cpaths:
            cpaths[d][cname] = f
        else:
            cpaths[d] = {cname: f}
        if not origin_linked:
            cname, _, d, f = compare(c, origin)
            if d in opaths:
                opaths[d][cname] = f
            else:
                opaths[d] = {cname: f}

    if not origin_linked:
        min_c = cpaths[min(cpaths.keys())]
        min_o = opaths[min(opaths.keys())]
        involved_c = set(min_c.keys()).intersection(set(min_o.keys()))
        for cname in involved_c:
            path = ""
            if min_c[cname] > 1:
                path += iname + "* -> "
            else:
                path += iname + " -> "
            if min_o[cname] > 1:
                path += cname + "* -> " + oname
            else:
                path += cname + " -> " + oname
            pp.append(path)
    else:
        min_c = cpaths[min(cpaths.keys())]
        for cname, f in min_c.items():
            if f > 1:
                pp.append(iname + "* -> " + cname)
            else:
                pp.append(iname + " -> " + cname)

    logging.info("My result :{}".format(pp))
    return json.dumps(pp)



