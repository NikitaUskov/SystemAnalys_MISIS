import csv
import argparse

# Функция для чтения конкретной ячейки из CSV файла
def main(csv_file_path, row_num, col_num):
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader, start=1):
            if i == row_num:
                try:
                    value = row[col_num - 1]
                    if value.strip() == '':
                        return None
                    return value
                except IndexError:
                    return f"Ошибка: Номер столбца {col_num} выходит за пределы."
    return f"Ошибка: Номер строки {row_num} выходит за пределы."

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Получить значение из CSV файла по строке и столбцу.')
    parser.add_argument('filepath', type=str, help='Путь к CSV файлу')
    parser.add_argument('row', type=int, help='Номер строки (начиная с 1)')
    parser.add_argument('col', type=int, help='Номер столбца (начиная с 1)')

    args = parser.parse_args()

    value = main(args.filepath, args.row, args.col)

    print(value)
