def min_edit_cost(replace_cost, insert_cost, delete_cost, A, B):
    n, m = len(A), len(B)
    distance_matrix = [[0] * (m + 1) for _ in range(n + 1)]

    # Редакционное расстояние с пустой строкой
    for i in range(1, n + 1):
        distance_matrix[i][0] = i * delete_cost  #d(S, '') = |S|
    for j in range(1, m + 1):
        distance_matrix[0][j] = j * insert_cost  #d('', S) = |S|

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1]  # буквы совпадают -> ничего не делаем
            else:
                distance_matrix[i][j] = min(
                    distance_matrix[i - 1][j - 1] + replace_cost, # замена
                    distance_matrix[i][j - 1] + insert_cost,      # вставка
                    distance_matrix[i - 1][j] + delete_cost       # удаление
                )

    return distance_matrix[n][m]

replace_cost, insert_cost, delete_cost = map(int, input().split())
A = input().strip()
B = input().strip()
print(min_edit_cost(replace_cost, insert_cost, delete_cost, A, B))

