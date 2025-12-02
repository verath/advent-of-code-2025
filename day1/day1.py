import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip()


def part1(input_str: str) -> int:
    dial = 50
    num_zero = 0
    for rotation in input_str.splitlines():
        sign = +1 if rotation[0] == "R" else -1
        change = sign * int(rotation[1:])
        dial = (dial + change) % 100
        if dial == 0:
            num_zero += 1

    return num_zero


def part2(input_str: str) -> int:
    dial = 50
    num_zero = 0
    for rotation in input_str.splitlines():
        sign = +1 if rotation[0] == "R" else -1
        change = sign * int(rotation[1:])
        while change != 0:
            dial = (dial + sign) % 100
            change -= sign
            if dial == 0:
                num_zero += 1

    return num_zero


class Day01Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 3)
        self.assertEqual(part1(INPUT), 1029)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 6)
        self.assertEqual(part2(INPUT), 5892)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
