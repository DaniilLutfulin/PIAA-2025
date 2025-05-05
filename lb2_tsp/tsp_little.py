from math import inf

class Graph():

    def __init__(self, arr, d = 0, paths = [], steps = 0):
        self.m = arr        # Матрица смежностей
        self.d = d          # Нижняя граница пути
        self.paths = paths[:]  # Массив включённых в решение путей
        self._n = len(self.m)
        self.steps = steps

    def __len__(self):
        return self._n

    def make_copy(self):
        copy_matrix = [row[:] for row in self.m]
        copy_paths = [row[:] for row in self.paths]
        return Graph(copy_matrix, self.d, copy_paths, self.steps)

    def reduction(self):
        n = len(self.m)
        d = 0
        for i in range(n):
            min_path = min(self.m[i])
            if min_path != 0 and min_path < inf:
                for j in range(n):
                    self.m[i][j] -= min_path
                self.d += min_path

        for j in range(n):
            min_path = min(self.m[i][j] for i in range(n))
            if min_path != 0 and min_path < inf:
                for i in range(n):
                    self.m[i][j] -= min_path
                self.d += min_path

    def most_expensive_zero(self):

        max_cost = -1
        row = col = None
        for i in range(self._n):
            for j in range(self._n):
                if self.m[i][j] == 0:
                    row_cost = min(self.m[i][x] for x in range(self._n) if x != j)
                    col_cost = min(self.m[x][j] for x in range(self._n) if x != i)
                    cost = row_cost + col_cost
                    if cost > max_cost:
                        max_cost, row, col = cost, i, j
        return row, col, max_cost

    def connect_paths(self, i, j):
        start_path = -1
        end_path = -1

        for k, path in enumerate(self.paths):
            if path[-1] == i:
                start_path = k
                path.append(j)
                self.m[path[-1]][path[0]] = inf

            elif j == path[0]:
                end_path = k
                path.insert(0, i)
                self.m[path[-1]][path[0]] = inf
        if start_path != -1 or end_path != -1:
            if start_path != -1 and end_path != -1:
                self.paths[start_path].extend(self.paths[end_path][2:])  # слияние start и end
                end = self.paths[start_path][-1]
                start = self.paths[start_path][0]
                self.m[end][start] = inf
                self.paths.pop(end_path)
        else:
            self.paths.append([i, j])
            self.m[j][i] = inf
    def include_path(self, i, j):

        new_graph = self.make_copy()
        new_graph.steps += 1
        for k in range (len(new_graph)):
            new_graph.m[i][k] = inf
            new_graph.m[k][j] = inf
        new_graph.connect_paths(i,j)
        return new_graph

    def exclude_path(self, i, j):
        new_graph = self.make_copy()
        new_graph.m[i][j] = inf
        return new_graph


def find_min_path(graph: Graph):
    solution_len = inf
    solution = None

    solution_len = inf
    def make_branch(start_graph: Graph):
        nonlocal solution_len, solution

        start_graph.reduction()
        if start_graph.steps == len(start_graph) - 2:

            for i in range(len(start_graph)):
                for j in range(len(start_graph)):
                    if start_graph.m[i][j] == 0:
                        start_graph.connect_paths(i,j)
            if start_graph.d < solution_len:
                solution_len = start_graph.d
                solution = start_graph.paths[0][:]
            return

        i, j, d = start_graph.most_expensive_zero()
        include_branch = start_graph.include_path(i,j)
        if include_branch.d <= solution_len:
            make_branch(include_branch)
        if start_graph.d + d <= solution_len: # start_graph.d + d == exclude_branch.d
            exclude_branch = start_graph.exclude_path(i,j)
            make_branch(exclude_branch)


    make_branch(graph)
    return solution,solution_len


def create_graph_from_input():
    n = int(input())
    matrix = []

    for i in range(n):
        row = list(map(int, input().split()))
        for j in range(n):
            if i == j:
                row[j] = inf
        matrix.append(row)

    return Graph(matrix)

graph = create_graph_from_input()

path, ans = find_min_path(graph)
while path[0]!=0:
    path.append(path[0])
    path.pop(0)
print(*path)
print(float(round(ans,3)))