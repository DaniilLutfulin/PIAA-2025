def min_edit_cost(replace_cost, insert_cost, delete_cost, A, B):
    n, m = len(A), len(B)
    distance_matrix = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        distance_matrix[i][0] = i * delete_cost
    for j in range(1, m + 1):
        distance_matrix[0][j] = j * insert_cost

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
            else:
                distance_matrix[i][j] = min(
                    distance_matrix[i-1][j-1] + replace_cost,  # замена
                    distance_matrix[i][j - 1] + insert_cost,       # вставка
                    distance_matrix[i - 1][j] + delete_cost        # удаление
                )
    return distance_matrix

def min_cost_A_to_BC(replace_cost, insert_cost, delete_cost, A, B, C):
    n = len(A)
    m, k = len(B), len(C)

    # Расстояние от префиксов A и B
    cost_A_B = min_edit_cost(replace_cost, insert_cost, delete_cost, A, B)
    # Расстояние суффиксов A к суффиксам C (то есть префиксов развернутых A,C)
    cost_revA_C = min_edit_cost(replace_cost, insert_cost, delete_cost, A[::-1], C[::-1])

    best = float('inf')
    for i in range(n + 1):
        #cost_A_B[i][m] == расстояние от A[0:i] до B
        #cost_revA_C[i][m] == расстояние от A[i+1:n] до B
        cost = cost_A_B[i][m] + cost_revA_C[n-i][k]
        best = min(best, cost)

    return best

replace_cost, insert_cost, delete_cost = map(int, input().split())
A = input().strip()
B = input().strip()
C = input().strip()
# c = min_edit_cost(replace_cost, insert_cost, delete_cost, A, B)[-1][-1]
# for i in range(0,len(B)+1):
#     cost = min_cost_A_to_BC(replace_cost,insert_cost,delete_cost,A, B[:i], B[i:])
#     print(A, B[:i], B[i:], cost)
#     if cost!=c:
#         print("Неверное решение")

c = min_cost_A_to_BC(replace_cost, insert_cost, delete_cost, A, B, C)
print(c)
