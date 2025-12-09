import unittest
from typing import Callable, List
from operator import add, mul
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip()


def parse_operators(lines: List[str]) -> List[Callable[[int, int], int]]:
    operators = []
    for operator in lines.pop().split():
        operators.append(add if operator == "+" else mul)
    return operators


def part1(input_str: str) -> int:
    lines = input_str.splitlines()
    operators = parse_operators(lines)

    values = [int(v) for v in lines.pop().split()]
    for line in lines:
        operands = [int(v) for v in line.split()]
        for i, operand in enumerate(operands):
            values[i] = operators[i](values[i], operand)

    return sum(values)


def part2(input_str: str) -> int:
    lines = input_str.splitlines()
    operators = parse_operators(lines)
    # TODO :)
    return 1


class Day05Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 4277556)
        self.assertEqual(part1(INPUT), 4412382293768)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 3263827)
        self.assertEqual(part2(INPUT), 0)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    # print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
