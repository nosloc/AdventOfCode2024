import unittest
import sys
from day6 import parse, solve1, solve2

class TestSolutions(unittest.TestCase):

    def test_part_one(self):
        input_data = (
            "....#.....\n"
            ".........#\n"
            "..........\n"
            "..#.......\n"
            ".......#..\n"
            "..........\n"
            ".#..^.....\n"
            "........#.\n"
            "#.........\n"
            "......#..."
        ).split("\n")
        self.assertEqual(solve1(input_data)[0], 41)

    def test_part_one_2(self):
        input_data = (
            ".#................\n"
            "..#...............\n"
            "..................\n"
            ".^................\n"
            ".................."
        ).split("\n")
        self.assertEqual(solve1(input_data)[0], 4)

    def test_part_two(self):
        input_data = (
            "....#.....\n"
            ".........#\n"
            "..........\n"
            "..#.......\n"
            ".......#..\n"
            "..........\n"
            ".#..^.....\n"
            "........#.\n"
            "#.........\n"
            "......#..."
        ).split("\n")
        self.assertEqual(solve2(input_data), 6)

    def test_part_two_2(self):
        input_data = (
            ".#..\n"
            "....\n"
            "#..#\n"
            ".^#."
        ).split("\n")
        self.assertEqual(solve2(input_data), 2)

    def test_part_two_3(self):
        input_data = (
            ".#....\n"
            ".....#\n"
            "..#...\n"
            "#.....\n"
            "....#.\n"
            "#.....\n"
            "..^#.."
        ).split("\n")
        self.assertEqual(solve2(input_data), 1)

    def test_part_two_4(self):
        input_data = (
            ".#.\n"
            "...\n"
            "#.#\n"
            "#.#\n"
            "#.#\n"
            "#^#\n"
            ".#."
        ).split("\n")
        self.assertEqual(solve2(input_data), 5)

    def test_part_two_5(self):
        input_data = (
            "########\n"
            "#......#\n"
            "...^...#\n"
            "########"
        ).split("\n")
        self.assertEqual(solve2(input_data), 6)

# Main

print("Running tests...")
#unittest.main(argv=[""], exit=False, defaultTest="TestSolutions.test_part_two_4")
unittest.main(argv=[""], exit=False)
sys.exit(0)
