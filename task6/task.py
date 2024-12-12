import json
import numpy as np
from collections import defaultdict


def parse_reviews(review_str):
    """
    Преобразует строку с отзывами из формата JSON в список Python.
    """
    return json.loads(review_str)


def create_template(args):
    """
    Создаёт шаблон для сопоставления элементов отзывов с их индексами.

    Параметры:
    - args: список строк JSON, содержащих отзывы.

    Возвращает:
    - template: словарь, где ключи — элементы отзывов, значения — их индексы.
    - reviews_count: общее количество элементов.
    """
    template = defaultdict(int)
    reviews_count = 0

    for el in json.loads(args[0]):  # Первый набор отзывов для создания шаблона
        if isinstance(el, list):
            for elem in el:
                template[elem] = reviews_count
                reviews_count += 1
        else:
            template[el] = reviews_count
            reviews_count += 1

    return template, reviews_count


def create_matrix(template, *reviews):
    """
    Создаёт матрицу оценок на основе шаблона и предоставленных отзывов.

    Параметры:
    - template: словарь сопоставления элементов и их индексов.
    - reviews: произвольное количество строк JSON с отзывами.

    Возвращает:
    - matrix: двумерный список, где каждая строка соответствует отзывам одного эксперта.
    """
    matrix = []
    for reviews_str in reviews:
        reviews = parse_reviews(reviews_str)  # Преобразуем строку JSON в список
        reviews_list = [0] * len(template)  # Инициализируем строку матрицы нулями

        for i, review in enumerate(reviews):
            if isinstance(review, list):
                for elem in review:
                    reviews_list[template[elem]] = i + 1  # Устанавливаем оценку для каждого элемента
            else:
                reviews_list[template[review]] = i + 1  # Устанавливаем оценку для одиночного элемента

        matrix.append(reviews_list)

    return matrix


def calculate(matrix, reviews_count, experts_count):
    """
    Вычисляет коэффициент согласованности на основе матрицы оценок.

    Параметры:
    - matrix: двумерный массив оценок.
    - reviews_count: общее количество элементов.
    - experts_count: количество экспертов (отзывов).

    Возвращает:
    - Коэффициент согласованности в виде числа с плавающей точкой.
    """
    sums = np.sum(np.array(matrix), axis=0)  # Суммы оценок для каждого элемента
    D = np.var(sums) * reviews_count / (reviews_count - 1)  # Дисперсия оценок
    D_max = experts_count ** 2 * (reviews_count ** 3 - reviews_count) / 12 / (reviews_count - 1)  # Максимальная дисперсия

    return D / D_max  # Отношение фактической дисперсии к максимальной


def task(*args):
    """
    Основная функция для обработки входных данных и вычисления результата.

    Параметры:
    - args: произвольное количество строк JSON с отзывами.

    Возвращает:
    - Коэффициент согласованности в виде числа с плавающей точкой.
    """
    template, reviews_count = create_template(args)  # Создаём шаблон и определяем количество элементов
    matrix = create_matrix(template,  *args)  # Создаём матрицу оценок
    result = calculate(matrix, reviews_count, len(args))  # Вычисляем коэффициент согласованности

    return result


if __name__ == '__main__':
    # Примеры входных данных
    range_1 = '["1", ["2", "3"], "4", ["5", "6", "7"], "8", "9", "10"]'
    range_2 = '[["1", "2"], ["3", "4", "5"], "6", "7", "9", ["8", "10"]]'
    range_3 = '["3", ["1", "4"], "2", "6", ["5", "7", "8"], ["9", "10"]]'

    # Вывод результата с точностью до двух знаков
    print(format(task(range_1, range_2, range_3), '.2f'))