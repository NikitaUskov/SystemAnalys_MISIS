import json
import numpy as np

def build_matrix(order_json: str) -> np.ndarray:
    groups = json.loads(order_json)
    elements = order_json.replace("[", "").replace("]", "").split(',')
    size = len(elements)

    matrix = np.zeros((size, size), dtype=int)

    for i in range(size):
        current_index = int(elements[i])
        for j in range(i, size):
            matrix[current_index - 1, int(elements[j]) - 1] = 1

    for group in groups:
        if isinstance(group, list):
            for index_1 in range(len(group)):
                for index_2 in range(index_1, len(group)):
                    matrix[int(group[index_1]) - 1, int(group[index_2]) - 1] = 1
                    matrix[int(group[index_2]) - 1, int(group[index_1]) - 1] = 1

    return matrix

def task(order_1: str, order_2: str) -> str:

    matrix_1 = build_matrix(order_1)
    matrix_2 = build_matrix(order_2)

    collision_matrix = (matrix_1 * matrix_2) + (matrix_1.T * matrix_2.T)

    collision_indices = np.where(collision_matrix == 0)
    collisions = []
    for i in range(len(collision_indices[0]) // 2):
        collisions.append([int(collision_indices[0][i]) + 1, int(collision_indices[1][i]) + 1])

    return json.dumps(collisions)

if __name__ == "__main__":
    with open('A.json', 'r') as file:
        order_A = file.read()
    with open('B.json', 'r') as file:
        order_B = file.read()

    # Выводим результат определения столкновений
    print(task(order_A, order_B))
