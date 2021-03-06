import logging
import json
# import enchant
# d = enchant.Dict("en_US")
# import nltk
# nltk.data.path.append('D:\CodeIT Suisse 2020\CodeITSuisse2020\nltk_data')
# from nltk.corpus import wordnet

with open("word_list.txt") as f:
    content = f.readlines()
words = [x.strip().lower() for x in content]

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def decrypt(s):
    # print(words)

    ans = s
    real_ans = ""
    encryption_count = 0

    word = False
    for i in range(len(ans)):
        for j in range(len(ans),3,-1):
            if len(ans[i:i+j]) >= 4  and ans[i:i+j] in words:
                print(ans[i:i+j])
                word = True
                break
            if len(ans[i:i+j]) <= 3:
                break
        if word:
            break

    if not word:
        real_ans = ""
    else:
        # i = 0
        # while i < len(ans):
        #     for k in range(2, len(ans)-i):
        #         if ans[i:i+k] in words:
        #             real_ans += ans[i:i+k] + " "
        #             i += k
    
        # real_ans = real_ans.strip()
        real_ans = ans
        return real_ans, encryption_count

    while not real_ans and encryption_count < 6:
        encryption_count += 1
        s = ans
        palindromes = set()
        for i in range(len(s)):
            palindromes = expandAroundCenter(s, i, i, palindromes)
            palindromes = expandAroundCenter(s, i, i+1, palindromes)

        palindromes = list(palindromes)
        palindromes = sorted(palindromes, key=lambda x:len(x), reverse=True)

        if palindromes:
            for i in range(26):
                shift = 0
                ori_string = ""
                alpha = ord(palindromes[0][0]) - 97
                diff = alpha - i
                diff = diff if diff >= 0  else 26+diff
                for char in palindromes[0]:
                    code = (ord(char) - 97 + diff) % 26 + 97
                    ori_string += chr(code)
                    shift += code
                shift += len(palindromes)
                
                found = True
                for j in range(len(ori_string)):
                    if chr((ord(ori_string[j]) - 97 + shift) % 26 + 97) != palindromes[0][j]:
                        found = False
                        break

                if found:
                    break

            ans = ""

            for char in s:
                ans += chr((ord(char) - 97 + diff) % 26 + 97)

        word = False
        for i in range(len(ans)):
            for j in range(len(ans),3,-1):
                if len(ans[i:i+j]) >= 4  and ans[i:i+j] in words:
                    print(ans[i:i+j])
                    word = True
                    break
                if len(ans[i:i+j]) <= 3:
                    break
            if word:
                break

        if not word:
            real_ans = ""
        else:
            # i = 0
            # while i < len(ans):
            #     for k in range(2, len(ans)-i):
            #         if ans[i:i+k] in words:
            #             real_ans += ans[i:i+k] + " "
            #             i += k
        
            # real_ans = real_ans.strip()
            real_ans = ans
            return real_ans, encryption_count

    if encryption_count == 6 and not real_ans:
        real_ans = ans
    return real_ans, encryption_count

def expandAroundCenter(s, l, r, palindromes):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        if len(s[l:r+1]) > 1:
            palindromes.add(s[l:r+1])
        l -= 1
        r += 1
    
    return palindromes

@app.route('/bored-scribe', methods=['POST'])
def evaluateBoredScribe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for el in data:
        originalText, encryptionCount = decrypt(el.get("encryptedText"))
        result.append({"id": el.get("id"), "encryptionCount":encryptionCount, "originalText":originalText})
    logging.info("My result :{}".format(result))
    return jsonify(result)



