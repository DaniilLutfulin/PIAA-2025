
def read_input():
    start = int(input())
    matrix = [[float(x) for x in input().split()]]
    for _ in range(len(matrix[0]) - 1):
        matrix.append([float(x) for x in input().split()])
    return start,matrix

def prim_mst(matrix, start):

    def heapify_up(heap, i):
        while i > 0:
            p = (i - 1) // 2
            if heap[i][0] < heap[p][0]:
                heap[i], heap[p] = heap[p], heap[i]
                i = p
            else:
                break

    def heapify_down(heap, i):
        n = len(heap)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i
            if l < n and heap[l][0] < heap[smallest][0]:
                smallest = l
            if r < n and heap[r][0] < heap[smallest][0]:
                smallest = r
            if smallest != i:
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
            else:
                break

    n = len(matrix)
    visited = [False] * n
    visited[start] = True
    adj = [[] for _ in range(n)]
    heap = []

    for v in range(n):
        if matrix[start][v] >= 0:
            heap.append((matrix[start][v], start, v))

    for i in range(len(heap)):
        heapify_up(heap, i)

    while heap and False in visited:
        weight, u, v = heap[0]
        heap[0] = heap[-1]
        heap.pop()
        heapify_down(heap, 0)
        if visited[v]:
            continue

        visited[v] = True
        adj[u].append(v)
        adj[v].append(u)

        for w in range(n):
            if not visited[w] and matrix[v][w] >= 0:
                heap.append((matrix[v][w], v, w))
                heapify_up(heap, len(heap) - 1)
    return adj


def mst_tour(mst, matrix, start):
    n = len(mst)
    visited = [False] * n
    path = []

    def dfs(u):
        visited[u] = True
        path.append(u)
        neighbors = sorted((v for v in mst[u] if not visited[v]), key=lambda v: matrix[u][v])
        for v in neighbors:
            dfs(v)

    dfs(start)
    path.append(start)
    return path

def compute_length(path, matrix):
    total = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        w = matrix[u][v]

        total += w
    return total

start, matrix = read_input()
mst = prim_mst(matrix, start)
tour = mst_tour(mst, matrix, start)
length = compute_length(tour, matrix)
print("%.2f" % length)
print(" ".join(str(v) for v in tour))

