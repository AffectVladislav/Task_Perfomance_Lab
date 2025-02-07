"""
На вход в качестве аргументов программы поступают три пути к файлу (в приложении
к заданию находятся примеры этих файлов):
● values.json содержит результаты прохождения тестов с уникальными id
● tests.json содержит структуру для построения отчета на основе прошедших
тестов (вложенность может быть большей, чем в примере)
● report.json - сюда записывается результат.
Напишите программу, которая формирует файл report.json с заполненными полями
value для структуры tests.json на основании values.json.
Структура report.json такая же, как у tests.json, только заполнены поля “value”.

На вход программы передается три пути к файлу!
"""
import os
import json
import argparse
from dataclasses import dataclass


@dataclass
class ReportGenerator:
    """
    Класс для генерации отчета на основе тестов и значений.
    """
    values_path: str
    tests_path: str
    report_path: str
    values: dict[int, str] = None  # Используем int для id
    tests_structure: list[dict] = None

    def __post_init__(self) -> None:
        self.values = {}  # Инициализация словаря значений
        self.tests_structure = []  # Инициализация структуры тестов

    def load_json(self, file_path: str) -> dict:
        """
        Загружает JSON-данные из указанного файла.

        :param file_path: Путь к файлу.
        :return: Данные в формате словаря.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Ошибка: Не удалось декодировать JSON из файла {file_path}.")
            exit(1)

    def fill_report_structure(self, tests_structure: list[dict]) -> None:
        """
        Заполняет структуру отчета на основе тестов.

        :param tests_structure: Список тестов.
        """
        # Сортируем тесты по id
        tests_structure.sort(key=lambda x: x['id'])

        for test in tests_structure:
            test_id = test.get('id')
            if test_id in self.values:
                test['value'] = self.values[test_id]

            # Если есть вложенные значения, рекурсивно заполняем их
            if 'values' in test:
                self.fill_report_structure(test['values'])

                # Сортируем вложенные значения по id
                test['values'].sort(key=lambda x: x['id'])

    def generate_report(self) -> None:
        """
        Генерирует отчет и записывает его в файл.
        """
        values_data = self.load_json(self.values_path)
        tests_data = self.load_json(self.tests_path)

        # Преобразуем values в словарь для быстрого доступа
        self.values = {item['id']: item['value'] for item in values_data['values']}

        self.tests_structure = tests_data['tests']
        self.fill_report_structure(self.tests_structure)

        try:
            with open(self.report_path, 'w', encoding='utf-8') as f:
                json.dump({'tests': self.tests_structure}, f, ensure_ascii=False, indent=4)
        except IOError:
            print(f"Ошибка: Не удалось записать в файл {self.report_path}.")
            exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description='Генерация отчета на основе тестов.')
    parser.add_argument('values_file', type=str, help='Путь к файлу values.json')
    parser.add_argument('tests_file', type=str, help='Путь к файлу tests.json')
    parser.add_argument('report_file', type=str, help='Путь к файлу report.json')

    args = parser.parse_args()

    # Проверяем, что файлы существуют
    if not all(os.path.isfile(file) for file in [args.values_file, args.tests_file]):
        print("Ошибка: Один или несколько файлов не найдены.")
        exit(1)

    report_generator = ReportGenerator(args.values_file, args.tests_file, args.report_file)
    report_generator.generate_report()


if __name__ == "__main__":
    main()
