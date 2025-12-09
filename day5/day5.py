import bisect
import unittest
from pathlib import Path
from typing import List, Tuple
from collections import deque

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()


def parse_fresh(lines: deque[str]) -> List[Tuple[int, int]]:
    ordered = []
    while line := lines.popleft():
        start, end = line.split("-", maxsplit=1)
        r = (int(start), int(end))
        bisect.insort(ordered, r)

    # Merge overlapping ranges.
    fresh = [ordered.pop(0)]
    for start, end in ordered:
        prev_start, prev_end = fresh[-1]
        if start <= prev_end:
            fresh[-1] = (prev_start, max(prev_end, end))
        else:
            fresh.append((start, end))

    return fresh


def part1(input_str: str) -> int:
    lines = deque(input_str.splitlines())
    fresh_ranges = parse_fresh(lines)

    num_fresh = 0
    for line in lines:
        ingredient = int(line)
        idx = bisect.bisect(fresh_ranges, (ingredient, 0))
        if idx == 0:
            continue
        start, end = fresh_ranges[idx - 1]
        if start <= ingredient <= end:
            num_fresh += 1

    return num_fresh


def part2(input_str: str) -> int:
    lines = deque(input_str.splitlines())
    fresh_ranges = parse_fresh(lines)
    # + 1 since ranges are inclusive.
    return sum(1 + end - start for (start, end) in fresh_ranges)


class Day05Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 3)
        self.assertEqual(part1(INPUT), 782)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 14)
        self.assertEqual(part2(INPUT), 353863745078671)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
