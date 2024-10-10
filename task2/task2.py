import csv
import argparse
from collections import defaultdict, deque
import io
import sys

# Импортируем парсер из соседней папки
sys.path.append('../SystemAnalys_MISIS/task1/task1.py"')  # путь к папке с вашим парсером
from task1.py import parse_csv_input  # Импортируйте свою функцию парсинга


# Функция для поиска всех потомков (прямых и косвенных) узла
def find_descendants(graph, node):
    descendants = set()
    queue = deque([node])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in descendants:
                descendants.add(neighbor)
                queue.append(neighbor)

    return descendants


# Функция для поиска всех предков (прямых и косвенных) узла
def find_ancestors(reverse_graph, node):
    ancestors = set()
    queue = deque([node])

    while queue:
        current = queue.popleft()
        for neighbor in reverse_graph[current]:
            if neighbor not in ancestors:
                ancestors.add(neighbor)
                queue.append(neighbor)

    return ancestors


# Основная функция для подсчета отношений
def main(filepath: str):
    # Шаг 1: Парсинг данных из CSV файла через внешний модуль
    edges = parse_csv_input(filepath)  # Используем внешний парсер

    # Создаем граф и обратный граф (для предков)
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for edge in edges:
        u, v = edge.split('-')
        u, v = int(u), int(v)
        graph[u].append(v)
        reverse_graph[v].append(u)

    # Шаг 2: Подсчет отношений для каждого узла
    nodes = set(graph.keys()).union(reverse_graph.keys())
    result = []

    for node in nodes:
        # r1 — непосредственное управление: сколько детей у узла
        r1 = len(graph[node])

        # r2 — непосредственное подчинение: сколько родителей у узла
        r2 = len(reverse_graph[node])

        # r3 — опосредованное управление: сколько потомков через несколько уровней
        r3 = len(find_descendants(graph, node)) - r1  # исключаем непосредственных потомков

        # r4 — опосредованное подчинение: сколько предков через несколько уровней
        r4 = len(find_ancestors(reverse_graph, node)) - r2  # исключаем непосредственных предков

        # r5 — соподчинение на одном уровне: узлы с теми же родителями
        r5 = 0
        for parent in reverse_graph[node]:
            siblings = graph[parent]
            r5 += len(siblings) - 1  # исключаем сам узел

        result.append([node, r1, r2, r3, r4, r5])

    # Шаг 3: Преобразование в CSV строку
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(result)

    return output.getvalue()


# Блок для работы с командной строкой
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Подсчет отношений на основе CSV файла.')
    parser.add_argument('filepath', type=str, help='Путь к CSV файлу с данными')

    args = parser.parse_args()

    # Вызов функции main с переданным файлом
    csv_output = main(args.filepath)

    # Вывод результата в консоль
    print(csv_output)
