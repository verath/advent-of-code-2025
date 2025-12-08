import unittest
from pathlib import Path
from typing import Tuple, Set, Generator, List

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()

Coordinate = Tuple[int, int]


def build_paper_coords(input_str: str) -> Tuple[Set[Coordinate], Coordinate]:
    paper_coords: Set[Coordinate] = set()
    for y, line in enumerate(input_str.splitlines()):
        for x, char in enumerate(line):
            if char == "@":
                paper_coords.add((x, y))

    bounds = (x, y)
    return paper_coords, bounds


def adjacent_eight(
    c: Coordinate, bounds: Coordinate
) -> Generator[Coordinate, None, None]:
    x_bounds, y_bounds = bounds
    x_mid, y_mid = c
    x_low = max(0, x_mid - 1)
    x_high = min(x_bounds, x_mid + 1)
    y_low = max(0, y_mid - 1)
    y_high = min(y_bounds, y_mid + 1)

    for x in range(x_low, x_high + 1):
        for y in range(y_low, y_high + 1):
            if (x, y) == (x_mid, y_mid):
                continue
            yield (x, y)


def count_adjacent_eight(
    paper_coords: Set[Coordinate], bounds: Coordinate, c: Coordinate
) -> int:
    return sum(1 if (x, y) in paper_coords else 0 for x, y in adjacent_eight(c, bounds))


def can_remove(
    paper_coords: Set[Coordinate], bounds: Coordinate, c: Coordinate
) -> bool:
    return count_adjacent_eight(paper_coords, bounds, c) < 4


def part1(input_str: str) -> int:
    paper_coords, bounds = build_paper_coords(input_str)
    return sum(1 if can_remove(paper_coords, bounds, c) else 0 for c in paper_coords)


def part2(input_str: str) -> int:
    paper_coords, bounds = build_paper_coords(input_str)
    num_removed = 0

    to_remove: Set[Coordinate] = {
        c for c in paper_coords if can_remove(paper_coords, bounds, c)
    }
    while to_remove:
        paper_coords.difference_update(to_remove)
        num_removed += len(to_remove)
        to_remove = {c for c in paper_coords if can_remove(paper_coords, bounds, c)}

    return num_removed


class Day04Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 13)
        self.assertEqual(part1(INPUT), 1428)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 43)
        self.assertEqual(part2(INPUT), 8936)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
