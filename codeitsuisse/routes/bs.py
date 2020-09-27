import logging
import json
import time

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def shift(string, sft):
    new = [(ord(char) - 97 + sft) % 26 + 97 for char in string]
    return "".join([chr(i) for i in new])


def expand_around_center(s, l, r, palindromes):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        if len(s[l:r + 1]) > 1:
            palindromes.add((l, r + 1))
        l -= 1
        r += 1
    return palindromes


def all_palindromes(s):
    palindromes = set()
    for i in range(len(s)):
        palindromes = expand_around_center(s, i, i, palindromes)
        palindromes = expand_around_center(s, i, i + 1, palindromes)

    palindromes = list(palindromes)
    n = len(palindromes)
    if n > 0:
        longest_p = max(palindromes, key=lambda x: x[1] - x[0])
        longest_p = longest_p[1] - longest_p[0]
        return [p for p in palindromes if p[1] - p[0] == longest_p], n
    else:
        return [], 0


def decrypt(s, p_start, p_end, n, done, level=1):
    total_shift = list()
    for i in range(1, 26):
        shift_amount = n + sum([
            (ord(s[ind]) - 97 + i) % 26 + 97 for ind in range(p_start, p_end)
        ])
        if shift_amount % 26 == -i % 26:
            shift_amount = shift_amount % 26
            new_s = shift(s, -shift_amount)
            if new_s in done:
                continue
            done.add(new_s)
            total_shift.append((new_s, level))
    if len(total_shift) == 0:
        return []
    else:
        new_total_shift = total_shift.copy()
        for res in total_shift:
            decrypted = decrypt(res[0], p_start, p_end, n, done, level=level + 1)
            new_total_shift += decrypted
        return new_total_shift


with open("word_list.txt") as f:
    content = f.readlines()
words = sorted([x.strip().lower() for x in content], key=lambda x: len(x), reverse=True)


def split_words(s):
    for w in words:
        if w in s:
            return True, len(w)
    return False, None


@app.route('/bs', methods=['POST'])
def boredScribe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    i = 1
    start_time = time.time()
    for el in data:
        print(i)
        text = el.get("encryptedText")
        p, n = all_palindromes(text)
        if n == 0:
            el_decrypt = decrypt(text, 0, 1, n, {text})
        else:
            el_decrypt = list()
            for pi in p:
                s, e = pi
                el_decrypt += decrypt(text, s, e, n, {text})
        probable = list()
        for eld, lvl in el_decrypt:
            is_word, l_word = split_words(eld)
            if is_word:
                probable.append((eld, lvl, l_word))
        if len(probable) > 0:
            eld, lvl, _ = max(probable, key=lambda x: (x[-1], -x[-2]))
        elif len(el_decrypt) > 0:
            eld, lvl = min(el_decrypt, key=lambda x: x[-1])
        else:
            eld, lvl = text, 0
        result.append({
            "id": el.get("id"),
            "encryptionCount": lvl,
            "originalText": eld
        })
        i += 1
    print("Time taken:", time.time() - start_time)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
