def prefix_func(s):
    p_arr = [0] * len(s)
    print(f"Префиксный массив для паттерна '{s}':")
    for i in range(1, len(s)):
        k = p_arr[i - 1]
        while k > 0 and s[i] != s[k]:
            k = p_arr[k - 1]
        if s[i] == s[k]:
            k += 1
        p_arr[i] = k
        print(f"строка: {s[:i+1]} i: {i}, k: {k}, префиксный массив: {p_arr}")
    return p_arr

def kmp(pattern, text):
    k = 0
    ans = []
    prefixes = prefix_func(pattern)
    print(f"Префиксный массив для паттерна '{pattern}': {prefixes}\n")

    for i in range(len(text)):
        print(f"Текущий индекс i: {i}, символ в тексте: '{text[i]}', индекс в паттерне k: {k}")
        print(f"Текст:   {text}")
        shift_start = max(0, i - k)
        print(f"Паттерн: {' ' * shift_start + pattern[:k+1]}")
        if i - k + len(pattern) > len(text):
            print("Паттерн больше не влезает в текст, выходим.")
            break
        while k > 0 and text[i] != pattern[k]:
            print(f"Не совпадает, возврат к k = {k - 1} по префиксному массиву (prefixes[k - 1] == {prefixes[k - 1]})")
            k = prefixes[k - 1]
            print(f"Текст:   {text}")
            shift_start = max(0, i - k)
            print(f"Паттерн: {' ' * shift_start + pattern[:k+1]}")

        if text[i] == pattern[k]:
            print(f"Совпадение! Увеличиваем k до {k + 1}")
            k += 1

        if k == len(pattern):
            print(f"Найдено полное совпадение на позиции {i - len(pattern) + 1}")
            ans.append(i - len(pattern) + 1)
            k = prefixes[k - 1]  # Возвращаемся к предыдущему состоянию в паттерне для поиска новых совпадений

    if not ans:
        return '-1'
    return ",".join(map(str, ans))


def is_shift(pattern, text):
    if len(pattern) != len(text):
        print("Длины не совпадают — сдвиг невозможен.")
        return -1

    k = 0
    n = len(text)
    prefixes = prefix_func(pattern)
    print(f"Префиксный массив для паттерна '{pattern}': {prefixes}\n")

    for i in range(n * 2 - 1):
        cur_char = text[i % n]
        print(f"Индекс i: {i}, символ в тексте (i % {n}): '{cur_char}', индекс в паттерне k: {k}")
        print(f"Текст:    {text + text[:n - 1] }")
        start = i - k
        if start >= 0:
            print(f"Паттерн:  {' ' * start}{pattern[:k+1]}")

        while k > 0 and cur_char != pattern[k]:
            print(f"Несовпадение: pattern[{k}] = '{pattern[k]}' != '{cur_char}'")
            k = prefixes[k - 1]
            print(f"Возврат по префиксу, k = {k}")
            start = i - k
            if start >= 0:
                print(f"Паттерн:  {' ' * start}{pattern}")

        if cur_char == pattern[k]:
            print(f"Совпадение: pattern[{k}] = '{pattern[k]}' == '{cur_char}', увеличиваем k до {k + 1}")
            k += 1

        if k == n:
            shift_pos = i - n + 1
            print(f"\nПОЛНОЕ СОВПАДЕНИЕ! Паттерн найден со сдвигом {shift_pos}")
            return shift_pos

    print("Совпадение не найдено — строки не являются сдвигами.")
    return -1
