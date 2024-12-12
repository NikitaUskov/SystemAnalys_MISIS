import json
import numpy as np
import argparse


def parse_clusters(json_string):
    """
    Преобразует JSON-строку в кластеры целых чисел.
    Каждый кластер представлен либо списком чисел, либо одним числом.
    Функция гарантирует, что все кластеры представлены списками для унификации обработки.
    """
    return [cluster if isinstance(cluster, list) else [cluster] for cluster in json.loads(json_string)]


def construct_matrix(clusters):
    """
    Создаёт бинарную матрицу на основе заданных кластеров.
    Бинарная матрица отражает отношения между элементами в кластерах,
    где 1 означает наличие связи, а 0 — её отсутствие.
    """
    n = sum(len(cluster) for cluster in clusters)  # Общее количество элементов во всех кластерах
    matrix = [[1] * n for _ in range(n)]  # Инициализация матрицы единицами

    preceding_elements = []  # Хранит элементы, обработанные ранее
    for cluster in clusters:
        for previous in preceding_elements:  # Перебираем элементы из предыдущих кластеров
            for current in cluster:  # Перебираем элементы текущего кластера
                matrix[current - 1][previous - 1] = 0  # Устанавливаем значение 0 для отсутствия предшествия
        preceding_elements.extend(cluster)  # Обновляем список обработанных элементов

    return np.array(matrix)  # Преобразуем матрицу в формат NumPy


def cluster_elements(matrix, estimates_1, estimates_2):
    """
    Группирует элементы в кластеры на основе бинарной матрицы и оценок.
    Оценки используются для сравнения кластеров и определения их отношений.
    """
    clusters = {}  # Словарь для хранения кластеров
    excluded = set()  # Множество для отслеживания исключённых строк

    # Шаг 1: Создание начальных кластеров на основе матрицы
    for row_index in range(len(matrix)):
        if row_index + 1 in excluded:
            continue

        current_cluster = [row_index + 1]  # Создаём новый кластер
        clusters[row_index + 1] = current_cluster

        for col_index in range(row_index + 1, len(matrix[0])):
            if matrix[row_index][col_index] == 0:  # Проверяем наличие связи
                current_cluster.append(col_index + 1)
                excluded.add(col_index + 1)  # Добавляем строку в исключения

    final_clusters = []  # Список для хранения окончательных кластеров

    # Шаг 2: Уточнение кластеров на основе оценок
    for key, elements in clusters.items():
        inserted = False

        for idx, existing in enumerate(final_clusters):
            # Сравниваем суммы оценок для существующих и текущих кластеров
            sum_existing_1 = np.sum(estimates_1[existing[0] - 1])
            sum_existing_2 = np.sum(estimates_2[existing[0] - 1])
            sum_key_1 = np.sum(estimates_1[key - 1])
            sum_key_2 = np.sum(estimates_2[key - 1])

            if sum_existing_1 == sum_key_1 and sum_existing_2 == sum_key_2:
                final_clusters[idx].extend(elements)  # Объединяем кластеры
                inserted = True
                break
            elif sum_existing_1 < sum_key_1 or sum_existing_2 < sum_key_2:
                final_clusters.insert(idx, elements)  # Вставляем в нужную позицию
                inserted = True
                break

        if not inserted:
            final_clusters.append(elements)  # Добавляем как новый кластер

    # Упрощаем кластеры: одновершинные кластеры представляются их элементом, а не списком
    return [cluster[0] if len(cluster) == 1 else cluster for cluster in final_clusters]


def process_inputs(input_1, input_2):
    """
    Обрабатывает две JSON-строки, представляющие кластеры, и вычисляет результирующие кластеры.
    Объединяет два входных массива в одну структуру и применяет логику кластеризации.
    """
    clusters_1 = parse_clusters(input_1)  # Разбираем первый ввод
    clusters_2 = parse_clusters(input_2)  # Разбираем второй ввод

    matrix_1 = construct_matrix(clusters_1)  # Создаём матрицу для первого ввода
    matrix_2 = construct_matrix(clusters_2)  # Создаём матрицу для второго ввода

    # Комбинируем матрицы с использованием побитовых операций
    combined_matrix = np.maximum(
        np.multiply(matrix_1, matrix_2),  # Побитовое И
        np.multiply(matrix_1.T, matrix_2.T)  # Побитовое И для транспонированных матриц
    )

    return cluster_elements(combined_matrix, matrix_1, matrix_2)  # Вычисляем кластеры


def main():
    """
    Основная функция для обработки аргументов командной строки, обработки входных файлов
    и вывода полученных кластеров.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", type=str, help="Путь к первому входному файлу")
    parser.add_argument("file2", type=str, help="Путь ко второму входному файлу")
    args = parser.parse_args()

    with open(args.file1, "r") as file1:
        input_1 = file1.read().strip()  # Читаем и удаляем лишние пробелы из первого файла

    with open(args.file2, "r") as file2:
        input_2 = file2.read().strip()  # Читаем и удаляем лишние пробелы из второго файла

    results = process_inputs(input_1, input_2)  # Обрабатываем вводные данные
    print(results)  # Выводим полученные кластеры


if __name__ == "__main__":
    main()
