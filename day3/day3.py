import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()


def max_joltage(bank: str, num_batteries: int) -> int:
    nums = ""
    for battery_index in range(num_batteries - 1, -1, -1):
        search_space = bank[:-battery_index] if battery_index > 0 else bank
        max_index, max_num = max(enumerate(search_space), key=lambda x: x[1])
        bank = bank[max_index + 1 :]
        nums += max_num

    return int(nums)


def part1(input_str: str) -> int:
    return sum(max_joltage(bank, 2) for bank in input_str.splitlines())


def part2(input_str: str) -> int:
    return sum(max_joltage(bank, 12) for bank in input_str.splitlines())


class Day03Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 357)
        self.assertEqual(part1(INPUT), 17432)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 3121910778619)
        self.assertEqual(part2(INPUT), 173065202451341)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
