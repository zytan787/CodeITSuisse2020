import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def maxBook(books, days, time_left, no_books, no_days, i, dp):  

    # Base case  
    if i == no_books: 
        return 0

    temp = dp[i]
    for k in range(no_days-1):
        temp = temp[time_left[k]]

    if temp[time_left[no_days-1]] != -1:  
        return temp[time_left[no_days-1]]
   
    fills = [0 for t in range(no_days)]
    fill_none = 0

    for k in range(no_days):
        if time_left[k] >= books[i]:
            fills[k] = 1 + maxBook(books, days, time_left[:k] + [time_left[k]-books[i]] + time_left[k+1:], no_books, no_days, i + 1, dp)  
  
    fill_none = maxBook(books, days, time_left[:], no_books, no_days, i+1, dp)  
  
    temp[time_left[no_days-1]] = max(fill_none, max(fills))  
      
    return temp[time_left[no_days-1]]

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateBabylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    no_books = data.get("numberOfBooks")
    no_days = data.get("numberOfDays")
    books = data.get("books")
    days = data.get("days")

    dp = -1
    for j in range(no_days):
        dp = [dp for i in range(200)]

    dp = [dp for i in range(200)]

    result = {"optimalNumberOfBooks": maxBook(books, days, days, no_books, no_days, 0, dp)}

    logging.info("My result :{}".format(result))
    return jsonify(result)



