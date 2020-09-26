import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# def maxBook(books, days, time_left, no_books, no_days, i, dp):  

#     # Base case  
#     if i == no_books: 
#         return 0

#     temp = dp[i]
#     for k in range(no_days-1):
#         temp = temp[time_left[k]]

#     if temp[time_left[-1]] != -1:  
#         return temp[time_left[-1]]
   
#     fills = [0 for t in range(no_days)]
#     fill_none = 0

#     for k in range(no_days):
#         if time_left[k] >= books[i]:
#             fills[k] = 1 + maxBook(books, days, time_left[:k] + [time_left[k]-books[i]] + time_left[k+1:], no_books, no_days, i + 1, dp)  
  
#     fill_none = maxBook(books, days, time_left[:], no_books, no_days, i+1, dp)  
  
#     temp[time_left[-1]] = max(fill_none, max(fills))  
      
#     return temp[time_left[-1]]

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateBabylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    no_books = data.get("numberOfBooks")
    no_days = data.get("numberOfDays")
    ori_books = data.get("books")
    days = data.get("days")

    max_ans = -1

    lst = [i for i in range(no_days)]
    big_lst = []
    for i in range(len(lst)):
        big_lst.append(lst[i:] + lst[:i])

    for seq in big_lst:
        books = ori_books[:]
        ans = 0
        for k in seq:
            dp = [[[0,[]] for i in range(days[k]+1)] for j in range(len(books)+1)]

            for i in range(1, len(books)+1):
                for j in range(1, days[k]+1):
                    if j >= books[i-1]:
                        if (1 + dp[i-1][j-books[i-1]][0]) > dp[i-1][j][0]:
                            dp[i][j] = [1 + dp[i-1][j-books[i-1]][0], dp[i-1][j-books[i-1]][1][:] + [i-1]]
                        else:
                            dp[i][j] = dp[i-1][j][:]

            ans += dp[-1][-1][0]
            dp[-1][-1][1].sort(reverse=True)
            for to_drop in dp[-1][-1][1]:
                books.pop(to_drop)

        max_ans = max(max_ans, ans)

    result = {"optimalNumberOfBooks": max_ans}

    logging.info("My result :{}".format(result))
    return jsonify(result)



