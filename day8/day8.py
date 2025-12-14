import math
import unittest
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Generator, Iterable, List, Set, Tuple

SCRIPT_DIR = Path(__file__).parent
INPUT = (SCRIPT_DIR / "input.txt").read_text()
TEST_INPUT = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()


JunctionBox = Tuple[int, int, int]
Circuit = Set[JunctionBox]


def parse(lines: Iterable[str]) -> List[JunctionBox]:
    boxes = []
    for line in lines:
        x, y, z = line.split(",", maxsplit=2)
        pos = (int(x), int(y), int(z))
        boxes.append(pos)
    return boxes


def straight_line_distance(box_a: JunctionBox, box_b: JunctionBox) -> float:
    return math.hypot(
        (box_a[0] - box_b[0]),
        (box_a[1] - box_b[1]),
        (box_a[2] - box_b[2]),
    )


def find_closest(
    boxes: List[JunctionBox],
) -> Generator[Tuple[JunctionBox, JunctionBox], None, None]:
    distances: List[Tuple[float, JunctionBox, JunctionBox]] = []
    while boxes:
        box_a = boxes.pop()
        for box_b in boxes:
            d = straight_line_distance(box_a, box_b)
            distances.append((d, box_a, box_b))

    for _, box_a, box_b in sorted(distances, key=lambda x: x[0]):
        yield (box_a, box_b)


def merge_circuits(
    circuits: List[Circuit], box_a: JunctionBox, box_b: JunctionBox
) -> None:
    idx_a = next(idx for idx, c in enumerate(circuits) if box_a in c)
    idx_b = next(idx for idx, c in enumerate(circuits) if box_b in c)
    if idx_a == idx_b:
        return  # Already same circuit.

    # Combine circuits a and b into a, drop circuit b.
    circuits[idx_a].update(circuits[idx_b])
    circuits[idx_b] = circuits[-1]
    circuits.pop()


def part1(input_str: str, num_connections: int) -> int:
    boxes = parse(input_str.splitlines())
    closest_gen = find_closest(boxes.copy())

    circuits: List[Circuit] = [set((box,)) for box in boxes]
    for _ in range(num_connections):
        box_a, box_b = next(closest_gen)
        merge_circuits(circuits, box_a, box_b)

    circuit_sizes = [len(circuit) for circuit in circuits]
    three_largest = sorted(circuit_sizes, reverse=True)[:3]
    return reduce(mul, three_largest)


def part2(input_str: str) -> int:
    boxes = parse(input_str.splitlines())
    closest_gen = find_closest(boxes.copy())

    circuits: List[Circuit] = [set((box,)) for box in boxes]
    for box_a, box_b in closest_gen:
        merge_circuits(circuits, box_a, box_b)
        if len(circuits) == 1:
            return box_a[0] * box_b[0]

    raise RuntimeError("No solution")


class Day08Test(unittest.TestCase):

    def test_part1(self) -> None:
        self.assertEqual(part1(TEST_INPUT, 10), 40)
        self.assertEqual(part1(INPUT, 1000), 42840)

    def test_part2(self) -> None:
        self.assertEqual(part2(TEST_INPUT), 25272)
        self.assertEqual(part2(INPUT), 170629052)


def main() -> None:
    unittest.main(exit=False)
    print("part1:", part1(INPUT, 1000))
    print("part2:", part2(INPUT))


if __name__ == "__main__":
    main()
