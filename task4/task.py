import numpy as np

def main():
    def build_relation_matrix(ranking, n):
        Y = np.zeros((n, n), dtype=int)
        np.fill_diagonal(Y, 1)

        for idx, cluster in enumerate(ranking):
            if isinstance(cluster, int):
                cluster = [cluster]

            for i in cluster:
                for j in cluster:
                    Y[i - 1][j - 1] = 1

            for i in cluster:
                for prev_cluster in ranking[:idx]:
                    if isinstance(prev_cluster, int):
                        prev_cluster = [prev_cluster]
                    for j in prev_cluster:
                        Y[j - 1][i - 1] = 1
        return Y

    def conflict_core(A_matrix, B_matrix):
        # Шаг 1: Логическое умножение A и B
        step1 = np.logical_and(A_matrix, B_matrix)

        # Шаг 2: Логическое умножение транспонированных матриц
        step2 = np.logical_and(A_matrix.T, B_matrix.T)

        # Шаг 3: Логическое сложение результатов шагов 1 и 2
        result_matrix = np.logical_or(step1, step2)
        return result_matrix.astype(int)

    A = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
    B = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]
    S = {8, 9}  # Ядро противоречий
    n = 10  # Общее количество элементов

    A_matrix = build_relation_matrix(A, n)
    B_matrix = build_relation_matrix(B, n)

    core_matrix = conflict_core(A_matrix, B_matrix)

    # Вывод результатов
    print("Матрица отношений для A:")
    print(A_matrix)
    print("\nМатрица отношений для B:")
    print(B_matrix)
    print("\nЯдро противоречий:")
    print(core_matrix)
