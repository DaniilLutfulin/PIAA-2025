from time import time
import matplotlib.pyplot as plt

def get_factor(n): # получение наименьшего делителя. Если число простое - вернет само число
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return i
    return n

def fill_square(n, squares): # рисует квадраты на матрице
    sq = []
    for i in range(n):
        sq.append([0] * n)
    for x, y, w in squares:
        for i in range(w):
            for j in range(w):
                sq[y + i][x + j] = 1
    return sq

def draw_square(n, squares, answer_mode=False): # рисует квадраты на матрице, но отображает их не единицей а размером квадрата
    sq = []
    for i in range(n):
        sq.append([0] * n)
    for x, y, w in squares:
        if answer_mode:
            x -= 1
            y -= 1
        for i in range(w):
            for j in range(w):
                sq[y + i][x + j] = w
    return sq

def quilts(n, debug=False): # функция разбиения квадрата на маленькие квадраты

    best_solution = None
    cur_squares = []
    sq = []
    for i in range(n):
        sq.append([0] * n) # пустой квадрат n*n
    if debug:
        print(f"Создание пустого квадрата {n}*{n}:")
        print(*sq, sep='\n')

    def find_first_empty(x, y): #поиск следующей пустой точки
        while y < n:
            while x < n:
                if sq[y][x] == 0:
                    return x, y
                x += 1
            y += 1
            x = 0

    def can_place(w, x, y): #проверка того можно ли поставить квадрат
        if x + w > n or y + w > n:
            return False
        for i in range(y, y + w):
            for j in range(x, x + w):
                if sq[i][j] != 0:
                    return False
        return True

    def place_square(w, x, y): # ставит квадрат на матрицу sq
        for i in range(y, y + w):
            for j in range(x, x + w):
                sq[i][j] = 1

    def remove_square(w, x, y): # удаляет квадрат из матрицы
        for i in range(y, y + w):
            for j in range(x, x + w):
                sq[i][j] = 0

    def backtrack(empty, x, y): # рекурсивная функция поиска разбиения квадрата
        nonlocal best_solution # массив с наилучшим решением, глобальный для вложенных функций

        if best_solution is not None and len(cur_squares) >= len(best_solution):
            if debug:
                print(f"Длина набора превысила длину лучшего решения")
            return

        if empty == 0: # не осталось места в квадрате
            if debug:
                print(f"Квадрат заполнен полностью. Количество квадратов: {len(cur_squares)}")
            if best_solution is None or len(cur_squares) < len(best_solution):
                best_solution = cur_squares.copy()
                if debug:
                    print("Принимаем решение за наилучшее")
                    print(*draw_square(n, best_solution + pants, answer_mode=False), sep='\n')
            return

        x, y = find_first_empty(x, y)
        max_w = min([n - x, n - y, n - 1])
        for w in range(max_w, 0, -1):
            if empty < w*w:
                continue
            if debug:
                print(f"Проверяем квадрат {x, y, w}")
            if can_place(w, x, y):
                place_square(w, x, y)
                cur_squares.append([x, y, w])
                backtrack(empty - w * w, x, y)
                if debug:
                    print(f"Удаляем квадрат {x, y, w}")
                remove_square(w, x, y)
                cur_squares.pop()

    first_factor = get_factor(n)
    scale = n // first_factor
    n = first_factor
    if debug:
        print(f"Попытка свести решение к меньшему квадрату. Наименьший делитель: {first_factor}, масштаб: {scale}")
    not_filled = n * n

    pants = []
    pants.append([0, 0, (n + 1) // 2])
    pants.append([(n + 1) // 2, 0, n // 2])
    pants.append([0, (n + 1) // 2, n // 2])
    not_filled -= sum(square[2] ** 2 for square in pants)
    sq = fill_square(n, pants)

    backtrack(not_filled, 0, 0)
    best_solution = pants + best_solution
    for i in range(len(best_solution)): # масштабирование и форматирование ответа
        x, y, w = best_solution[i]
        x = x * scale + 1
        y = y * scale + 1
        w = w * scale
        best_solution[i] = [x, y, w]
    return best_solution

def draw_time():
    times = []

    n_values = [i for i in range(2,30)]

    for n in n_values:
        start_time = time()
        quilts(n, debug=False)
        end_time = time()
        times.append(end_time - start_time)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, marker='o', linestyle='-', label="Время выполнения (сек)")
    plt.xlabel("Размер квадрата (n)")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Зависимость времени выполнения от размера квадрата")
    plt.legend()
    plt.grid(True)
    plt.show()

    prime_times = []
    n_values = [i for i in range(2, 40)]
    primes = [n for n in n_values if get_factor(n) == n]
    for n in primes:
        start_time = time()
        quilts(n, debug=False)
        end_time = time()
        prime_times.append(end_time - start_time)

    plt.figure(figsize=(10, 6))
    plt.xticks(primes)
    plt.plot(primes, prime_times, marker='o', linestyle='-', color='red', label="Время выполнения (сек)")
    plt.xlabel("Простые числа (n)")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Зависимость времени выполнения от размера квадрата (только простые n)")
    plt.legend()
    plt.grid(True)
    plt.show()


# n = int(input())
# a = quilts(n, debug=0)
# print(len(a))
# for row in a:
#     print(" ".join(map(str, row)))

draw_time()