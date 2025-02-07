"""
Круговой массив - массив из элементов, в котором по достижению конца массива
следующим элементом будет снова первый. Массив задается числом n, то есть
представляет собой числа от 1 до n.
Пример кругового массива для n=3:
"1231231"
Напишите программу, которая выводит путь, по которому, двигаясь интервалом длины
m по заданному массиву, концом будет являться первый элемент.
Началом одного интервала является конец предыдущего.
Путь - массив из начальных элементов полученных интервалов.

Например, для последнего примера на вход подаются аргументы: 5 4, ожидаемый
вывод в консоль: 14253
"""
import argparse
from dataclasses import dataclass


@dataclass
class CircularCounter:
    """
    Класс для реализации кругового счетчика.
    """
    n: int  # Количество элементов
    m: int  # Шаг
    current: int = 1  # Текущий элемент

    def run(self) -> str:
        """
        Запускает круговой счетчик и возвращает последовательность элементов.

        :return: Строка с последовательностью элементов.
        """
        results = []
        while True:
            results.append(self.current)
            self.current = 1 + (self.current + self.m - 2) % self.n
            if self.current == 1:
                break
        return ''.join(map(str, results))


def main() -> None:
    """
    Главная функция для запуска кругового счетчика и записи результата в файл.
    """
    parser = argparse.ArgumentParser(description='Circular Counter')
    parser.add_argument('n', type=int, help='Количество элементов')
    parser.add_argument('m', type=int, help='Шаг')
    parser.add_argument('output_file', type=str, help='Имя выходного файла')

    args = parser.parse_args()

    counter = CircularCounter(args.n, args.m)
    result = counter.run()

    # Запись результата в файл
    with open(args.output_file, 'w') as f:
        f.write(result)


if __name__ == "__main__":
    main()
