"""
Дан массив целых чисел nums.
Напишите программу, выводящую минимальное количество ходов, требуемых для
приведения всех элементов к одному числу.
За один ход можно уменьшить или увеличить число массива на 1.
Пример:
nums = [1, 2, 3]
Решение: [1, 2, 3] => [2, 2, 3] => [2, 2, 2].
Минимальное количество ходов: 2.

Элементы массива читаются из файла, переданного в качестве аргумента
командной строки!
Пример:
На вход подаётся файл с содержимым:
1
10
2
9
Вывод в консоль: 16
"""

import sys
from typing import List


class MedianMovesCalculator:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def quickselect(self, nums: List[int], k: int) -> int:
        if len(nums) == 1:
            return nums[0]

        pivot = nums[len(nums) // 2]
        lows = [x for x in nums if x < pivot]
        highs = [x for x in nums if x > pivot]
        pivots = [x for x in nums if x == pivot]

        if k < len(lows):
            return self.quickselect(lows, k)
        elif k < len(lows) + len(pivots):
            return pivots[0]
        else:
            return self.quickselect(highs, k - len(lows) - len(pivots))

    def min_moves(self) -> int:
        n = len(self.nums)
        median = self.quickselect(self.nums, n // 2)
        count = sum(abs(num - median) for num in self.nums)
        return count


def read_numbers_from_file(file_path: str) -> List[int]:
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: py task_4.py <путь_к_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    nums = read_numbers_from_file(file_path)

    calculator = MedianMovesCalculator(nums)
    result = calculator.min_moves()
    print(f"Минимальное количество ходов: {result}")
