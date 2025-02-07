"""
Напишите программу, которая рассчитывает положение точки относительно
окружности.
Координаты центра окружности и его радиус считываются из файла 1.
Пример:
1 1
5
Координаты точек считываются из файла 2.
Пример:
0 0
1 6
6 6

Вывод для данных примеров файлов:
1
0
2

Пути к файлам передаются программе в качестве аргументов!
● файл с координатами и радиусом окружности - 1 аргумент;
● файл с координатами точек - 2 аргумент;
● координаты - рациональные числа в диапазоне от 10^-38 до 10^38;
● количество точек от 1 до 100;
● вывод каждого положения точки заканчивается символом новой строки;
● соответствия ответов:
○ 0 - точка лежит на окружности
○ 1 - точка внутри
○ 2 - точка снаружи.
Вывод программы в консоль.
"""
import sys
from dataclasses import dataclass


@dataclass
class Point:
    """
    Класс для представления точки в 2D пространстве.
    """
    x: float
    y: float


@dataclass
class Circle:
    """
    Класс для представления окружности.
    """
    center: Point
    radius: float

    def point_position(self, point: Point) -> int:
        """
        Определяет положение точки относительно окружности.

        :param point: Точка, положение которой нужно определить.
        :return: 1, если точка внутри окружности; 0, если на окружности; 2, если снаружи.
        """
        dx = point.x - self.center.x
        dy = point.y - self.center.y
        distance_squared = dx ** 2 + dy ** 2
        radius_squared = self.radius ** 2

        if distance_squared < radius_squared:
            return 1  # Точка внутри окружности
        elif distance_squared == radius_squared:
            return 0  # Точка на окружности
        else:
            return 2  # Точка снаружи окружности


def read_circle_data(file_path: str) -> Circle:
    """
    Читает данные окружности из файла.

    :param file_path: Путь к файлу с данными окружности.
    :return: Объект Circle.
    """
    with open(file_path, 'r') as file:
        center_x, center_y = map(float, file.readline().strip().split())
        radius = float(file.readline().strip())
    return Circle(Point(center_x, center_y), radius)


def read_points(file_path: str) -> list[Point]:
    """
    Читает точки из файла.

    :param file_path: Путь к файлу с данными точек.
    :return: Список объектов Point.
    """
    points: list[Point] = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split())
            points.append(Point(x, y))
    return points


def main(circle_file: str, points_file: str) -> None:
    """
    Главная функция для чтения данных окружности и точек, а также определения положения точек.

    :param circle_file: Путь к файлу с данными окружности.
    :param points_file: Путь к файлу с данными точек.
    """
    try:
        circle = read_circle_data(circle_file)
        points = read_points(points_file)

        for point in points:
            position = circle.point_position(point)
            print(position)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{circle_file}' или '{points_file}' не найден.")
    except ValueError:
        print("Ошибка: Неверный формат данных в файле.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: py task_2.py <путь_к_файлу_окружности> <путь_к_файлу_точек>")
    else:
        circle_file = sys.argv[1]
        points_file = sys.argv[2]
        main(circle_file, points_file)
