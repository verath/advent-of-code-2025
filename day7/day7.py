import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def start(line: str) -> int:
    return line.index("S")


def move(line: str, tachyons: Set[int]) -> Tuple[int, Set[int]]:
    num_splits = 0
    next_tachyons: Set[int] = set()
    for t in tachyons:
        if line[t] == "^":
            num_splits += 1
            next_tachyons.add(t - 1)
            next_tachyons.add(t + 1)
        else:
            next_tachyons.add(t)

    return (num_splits, next_tachyons)


def part1(input_str: str) -> int:
    lines = input_str.splitlines()[::2]
    first_line, lines = lines[0], lines[1:]
    tachyons = set([start(first_line)])

    total_splits = 0
    for line in lines:
        num_splits, tachyons = move(line, tachyons)
        total_splits += num_splits

    return total_splits


@dataclass()
class Node:
    index: int
    children: List["Node"] = field(default_factory=list)
    num_paths: Optional[int] = None


def count_paths(node: Node) -> int:
    if not node.children:
        return 1

    if not node.num_paths:
        node.num_paths = sum(count_paths(child) for child in node.children)

    return node.num_paths


def part2(input_str: str) -> int:
    lines = input_str.splitlines()[::2]
    first_line, lines = lines[0], lines[1:]
    start_tachyon = start(first_line)

    root = Node(start_tachyon)
    nodes = [root]
    for line in lines:
        next_nodes: Dict[int, Node] = {}
        for node in nodes:
            child_indexes = []
            if line[node.index] == "^":
                child_indexes = [node.index - 1, node.index + 1]
            else:
                child_indexes = [node.index]

            for index in child_indexes:
                if index not in next_nodes:
                    next_nodes[index] = Node(index)
                node.children.append(next_nodes[index])

        nodes = next_nodes.values()

    return count_paths(root)


class Day07Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT), 21)
        self.assertEqual(part1(INPUT), 1687)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 40)
        self.assertEqual(part2(INPUT), 390684413472684)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
