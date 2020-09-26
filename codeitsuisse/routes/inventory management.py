import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluateInventoryManagement():
    datas = request.get_json()
    logging.info("data sent for evaluation {}".format(datas))
    result = []
    for data in datas:
        name = data.get("searchItemName")
        items = data.get("items")
        items.sort()
        dct = {}

        for item in items:
            lst = [[1000 for x in range(len(name)+1)] for y in range(len(item)+1)]

            for i in range(0,len(item)+1):
                lst[i][0] = i
            for j in range(0,len(name)+1):
                lst[0][j] = j

            for i in range(1,len(item)+1):
                for j in range(1,len(name)+1):
                    lst[i][j] = min(lst[i][j-1]+1, lst[i-1][j]+1, lst[i-1][j-1] if item[i-1].lower() == name[j-1].lower() else lst[i-1][j-1]+1)
                    
            ans = []
            i, j = len(item), len(name)
            while i >= 1 and j >= 1:
                if item[i-1].lower() == name[j-1].lower():
                    ans.insert(0, name[j-1])
                    i -= 1
                    j -= 1
                else:
                    temp = [[i,j-1],[i-1,j],[i-1,j-1]]
                    min_value = float("inf")
                    min_coord = [i,j-1]
                    for el in temp:
                        if lst[el[0]][el[1]] < min_value:
                            min_value = lst[el[0]][el[1]]
                            min_coord = el[:]
                    if min_coord[0] == i-1 and min_coord[1] == j-1:
                        ans.insert(0, item[i-1])
                        i -= 1
                        j -= 1
                    elif min_coord[0] == i and min_coord[1] == j-1:
                        ans.insert(0, "-" + name[j-1])
                        j -= 1
                    elif min_coord[0] == i-1 and min_coord[1] == j:
                        ans.insert(0, "+" + item[i-1])
                        i -= 1

            while i >= 1:
                ans.insert(0, "+" + item[i-1])
                i -= 1
            while j >= 1:
                ans.insert(0, "-" + name[j-1])
                j -= 1

            if lst[len(item)][len(name)] in dct:
                dct[lst[len(item)][len(name)]].append("".join(ans))
            else:
                dct[lst[len(item)][len(name)]] = ["".join(ans)]

        searchResult = []
        dct = {k:v for k,v in sorted(dct.items())}
        for value in dct.values():
            if len(searchResult) >= 10:
                break
            searchResult.extend(value)
        
        searchResult = searchResult[:10]

        result.append({"searchItemName":name, "searchResult":searchResult})

    logging.info("My result :{}".format(result))
    return jsonify(result)



