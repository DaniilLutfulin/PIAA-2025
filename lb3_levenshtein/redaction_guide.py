def redaction_guide(replace_cost, insert_cost, delete_cost, A, B):
    n, m = len(A), len(B)
    distance_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    operation_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    # Редакционное расстояние с пустой строкой
    for i in range(1, n + 1):
        distance_matrix[i][0] = i * delete_cost #d(S, '') = |S|
        operation_matrix[i][0] = 'D'  # Чтобы из S получить '' нужно все удалить
    for j in range(1, m + 1):
        distance_matrix[0][j] = j * insert_cost #d('', S) = |S|
        operation_matrix[0][j] = 'I'  # Чтобы из '' получить S нужно вставить символы

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1] # буквы совпадают -> ничего не делаем
                operation_matrix[i][j] = 'M'
            else:
                best_way = min(
                    distance_matrix[i - 1][j - 1] + replace_cost,  # замена
                    distance_matrix[i][j - 1] + insert_cost,       # вставка
                    distance_matrix[i - 1][j] + delete_cost        # удаление
                )
                if best_way == distance_matrix[i - 1][j - 1] + replace_cost:
                    operation_matrix[i][j] = 'R'
                elif best_way == distance_matrix[i][j - 1] + insert_cost:
                    operation_matrix[i][j] = 'I'
                else:
                    operation_matrix[i][j] = 'D'
                distance_matrix[i][j] = best_way
    return get_redaction_path(n , m , operation_matrix)

def get_redaction_path(n,m,operation_matrix):
    i, j = n, m
    guide = ''
    while i!= 0 or j != 0:
        op = operation_matrix[i][j]
        if op == 'M' or op == 'R':  # Совпадение/замена - значит пришли слева сверху
            i -= 1
            j -= 1
        elif op == 'I': # Вставка - пришли слева
            j -= 1
        elif op == 'D': # Удаление - пришли сверху
            i -= 1
        guide += op
    return guide[::-1]

replace_cost, insert_cost, delete_cost = map(int, input().split())
A = input().strip()
B = input().strip()
print(redaction_guide(replace_cost, insert_cost, delete_cost, A, B))