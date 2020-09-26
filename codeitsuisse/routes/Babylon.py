import logging
import json

from flask import request, jsonify

from codeitsuisse import app

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


def num_books_for_min(books_left, minute, books_read):
    if len(books_left) == 1:
        if books_left[0] > minute:
            return [books_read]
        else:
            return [books_read + books_left]
    if books_left[0] <= minute < books_left[1]:
        return [books_read + books_left[:1]]
    all_books_sets = [books_read]
    max_books = len(books_read)
    for i in range(len(books_left) - 1):
        if books_left[i] <= minute:
            books = num_books_for_min(books_left[i + 1:], minute - books_left[i], books_read + [books_left[i]])
            if len(books[0]) > max_books:
                max_books = len(books[0])
                all_books_sets = books
            elif len(books[0]) == max_books:
                all_books_sets += books
    return all_books_sets


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateBabylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    no_books = data.get("numberOfBooks")
    no_days = data.get("numberOfDays")
    # ori_books = data.get("books")
    # days = data.get("days")

    books_left = sorted(data.get("books"))
    max_ans = 0
    days = sorted(data.get("days"))

    for minute in days:
        books = num_books_for_min(books_left, minute, [])
        max_books = max(books, key=lambda x: sum(x))
        max_ans += len(max_books)
        for i in max_books:
            books_left.remove(i)

    # max_ans = -1
    #
    # lst = [i for i in range(no_days)]
    # first_lst = []
    # for i in range(len(lst)):
    #     first_lst.append(lst[i:] + lst[:i])
    # second_lst = []
    # for i in range(len(lst)-1):
    #     second_lst.append(lst[i:i+1] + lst[i+2:] + lst[:i] + [lst[i+1]])
    # third_lst = []
    # for i in range(len(lst)-2):
    #     third_lst.append(lst[i:i+2] + lst[i+3:] + lst[:i] + [lst[i+2]])
    # forth_lst = []
    # for i in range(len(lst)-3):
    #     forth_lst.append(lst[i:i+3] + lst[i+4:] + lst[:i] + [lst[i+3]])
    # big_lst = [first_lst, second_lst, third_lst, forth_lst]
    #
    # for small_lst in big_lst:
    #     for seq in small_lst:
    #         books = ori_books[:]
    #         ans = 0
    #         for k in seq:
    #             print(books)
    #             dp = [[[0,[]] for i in range(days[k]+1)] for j in range(len(books)+1)]
    #
    #             for i in range(1, len(books)+1):
    #                 for j in range(1, days[k]+1):
    #                     if j >= books[i-1]:
    #                         if (1 + dp[i-1][j-books[i-1]][0]) > dp[i-1][j][0]:
    #                             dp[i][j] = [1 + dp[i-1][j-books[i-1]][0], dp[i-1][j-books[i-1]][1][:] + [i-1]]
    #                         else:
    #                             dp[i][j] = dp[i-1][j][:]
    #
    #             ans += dp[-1][-1][0]
    #             dp[-1][-1][1].sort(reverse=True)
    #             for to_drop in dp[-1][-1][1]:
    #                 books.pop(to_drop)
    #
    #         max_ans = max(max_ans, ans)

    result = {"optimalNumberOfBooks": max_ans}

    logging.info("My result :{}".format(result))
    return jsonify(result)



