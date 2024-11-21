import numpy as np
import csv
import io
import math

def edges_to_matrix(edges, n):
    """
    Преобразование списка рёбер в матрицу смежности.
    edges: список кортежей (узел_родитель, узел_ребенок)
    n: количество узлов
    """
    matrix = np.zeros((n, n), dtype=int)
    for parent, child in edges:
        matrix[parent][child] = 1
    return matrix

def task(csv_or_edges, is_edges=False, num_nodes=None):
    """
    Вычисление энтропии структуры графа. Принимает либо CSV строку, либо список рёбер.
    csv_or_edges: строка с матрицей или список рёбер [(1, 2), (2, 3)].
    is_edges: флаг, который указывает, является ли вход списком рёбер.
    num_nodes: количество узлов, необходимо для списка рёбер.
    """
    
    if is_edges:
        if not num_nodes:
            raise ValueError("Необходимо указать количество узлов (num_nodes) для списка рёбер.")
        matrix = edges_to_matrix(csv_or_edges, num_nodes)
    else:
        # Преобразование CSV-строки в матрицу экстенсиональных длин
        matrix = []
        csv_reader = csv.reader(io.StringIO(csv_or_edges), delimiter=' ')
        
        for row in csv_reader:
            matrix.append(list(map(int, row)))
        
        matrix = np.array(matrix)
    
    n = len(matrix)  # Количество узлов (n)
    if n <= 1:
        return 0.0  # Если меньше одного узла, энтропия не считается
    
    entropy = 0.0

    # Двойное суммирование по всем узлам и связям
    for j in range(n):
        for i in range(n):
            l_ij = matrix[i, j]  # Значение экстенсиональной длины для узла i по отношению j
            if l_ij > 0:
                # Рассчитываем вклад по формуле H(m, r)
                probability = l_ij / (n - 1)
                entropy -= probability * math.log2(probability)

    # Округление до 1 знака после запятой
    return round(entropy, 1)

# Пример данных: CSV строки
strings = [
    "0 1 1 1 1 1\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0",
    "0 1 0 0 0 0\n1 0 1 0 0 0\n0 1 0 1 0 0\n0 0 1 0 1 0\n0 0 0 1 0 1\n0 0 0 0 1 0",
    "0 1 0 0 1 0\n1 0 1 1 0 0\n0 1 0 0 0 0\n0 1 0 0 0 0\n1 0 0 0 0 1\n0 0 0 0 1 0",
    "0 1 0 0 0 0\n1 0 1 0 1 0\n0 1 0 1 0 0\n0 0 1 0 0 0\n0 1 0 0 0 1\n0 0 0 0 1 0"
]

# Пример вызова для матриц
for i, csv_data in enumerate(strings, start=1):
    entropy_value = task(csv_data)
    print(f"Entropy for matrix #{i}: {entropy_value}")

# Пример данных: список рёбер
edges_list = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)] #random
num_nodes = 6
entropy_value_edges = task(edges_list, is_edges=True, num_nodes=num_nodes)
print(f"Entropy for edges list: {entropy_value_edges}")
