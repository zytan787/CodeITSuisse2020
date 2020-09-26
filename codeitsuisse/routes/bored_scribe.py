import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def decrypt(s):
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

    else:
        ans = s

    return ans

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
        result.append({"id": el.get("id"), "encryptionCount":el.get("id"), "originalText":decrypt(el.get("encryptedText"))})
    logging.info("My result :{}".format(result))
    return json.dumps(result)


