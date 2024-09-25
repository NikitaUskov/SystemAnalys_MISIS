import csv
import argparse

# Функция для чтения конкретной ячейки из CSV файла
def get_value_from_csv(csv_file_path, row_num, col_num):
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader, start=1):  # Нумерация строк начинается с 1
            if i == row_num:  # Если это нужная строка
                try:
                    value = row[col_num - 1]  # Вычитаем 1 для корректной работы с индексом столбца
                    if value.strip() == '':  # Если значение пустое, возвращаем None
                        return None
                    return value  # Возвращаем значение как есть (строка или число)
                except IndexError:
                    return f"Ошибка: Номер столбца {col_num} выходит за пределы."
    return f"Ошибка: Номер строки {row_num} выходит за пределы."

# Основной блок для работы с командной строкой
if __name__ == '__main__':
    # Используем argparse для получения пути к файлу и индексов строки и столбца через командную строку
    parser = argparse.ArgumentParser(description='Получить значение из CSV файла по строке и столбцу.')
    parser.add_argument('filepath', type=str, help='Путь к CSV файлу')
    parser.add_argument('row', type=int, help='Номер строки (начиная с 1)')
    parser.add_argument('col', type=int, help='Номер столбца (начиная с 1)')

    # Получаем аргументы
    args = parser.parse_args()

    # Вызов функции с переданными аргументами
    value = get_value_from_csv(args.filepath, args.row, args.col)

    # Вывод результата (None будет отображен как None)
    print(value)
