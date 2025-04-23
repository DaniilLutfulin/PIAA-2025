def prefix_func(str):
    prefixes = [0] * len(str)

    for i in range(1, len(str)):
        k = prefixes[i - 1]

        while k > 0 and str[i] != str[k]:
            k = prefixes[k - 1]

        if str[i] == str[k]:
            k += 1

        prefixes[i] = k
    return prefixes

def kmp(pattern, text):
    k = 0
    ans = []
    prefixes = prefix_func(pattern)

    for i in range(0,len(text)):
        # k == prefixes[i-1]
        if i - k + len(pattern) > len(text):
            break

        while k > 0 and text[i] != pattern[k]:
            k = prefixes[k-1]

        if text[i] == pattern[k]:
            k+=1

        if k == len(pattern):
            ans.append(i - len(pattern) + 1)
            k = prefixes[k-1]

    if not ans:
        return '-1'
    return ",".join(map(str, ans))

def find_shift(pattern, text):
    if len(pattern) != len(text):
        return -1
    k = 0
    n = len(text)
    prefixes = prefix_func(pattern)

    for i in range(n * 2 - 1):
        cur_char = text[i % n]

        while k > 0 and cur_char != pattern[k]:
            k = prefixes[k - 1]

        if pattern[k] == cur_char:
            k += 1

        if k == n:
            return i - n + 1

    return -1
