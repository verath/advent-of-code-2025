import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""".strip()


def part1(input_str: str) -> int:
    def is_invalid(id_num: int) -> bool:
        id_str = str(id_num)
        a, b = id_str[: len(id_str) // 2], id_str[len(id_str) // 2 :]
        return a == b

    invalid_ids = 0
    ranges = input_str.split(",")
    for r in ranges:
        start, end = r.split("-", maxsplit=1)
        id_range = range(int(start), int(end) + 1)
        invalid_ids += sum(i if is_invalid(i) else 0 for i in id_range)
    return invalid_ids


def part2(input_str: str) -> int:
    def is_invalid(id_num: int) -> bool:
        """
        Now, an ID is invalid if it is made only of some sequence of digits
        repeated at least twice. So, 12341234 (1234 two times), 123123123
        (123 three times), 1212121212 (12 five times), and 1111111 (1 seven
        times) are all invalid IDs.
        """
        id_str = str(id_num)
        for split_pos in range(1, len(id_str) // 2 + 1):
            src = id_str[: split_pos]
            expected = src * (len(id_str) // split_pos)
            if id_str == expected:
                return True
        return False

    invalid_ids = 0
    ranges = input_str.split(",")
    for r in ranges:
        start, end = r.split("-", maxsplit=1)
        id_range = range(int(start), int(end) + 1)
        invalid_ids += sum(i if is_invalid(i) else 0 for i in id_range)
    return invalid_ids


class Day02Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 1227775554)
        self.assertEqual(part1(INPUT), 40055209690)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 4174379265)
        self.assertEqual(part2(INPUT), 50857215650)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
