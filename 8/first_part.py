import sys
import itertools


def process_input(input_string: str) -> list:
    # break the input into lines
    lines = input_string.strip().split("\n")

    return lines


def find_antennas_location(input_list):
    # create a dictionary of antennas
    antennas = {}
    for i, line in enumerate(input_list):
        for j, char in enumerate(line):
            if char != ".":
                antennas[char] = antennas.get(char, []) + [(i, j)]
    return antennas


def is_point_valid(point, grid):
    if point[0] < 0 or point[0] >= len(grid):
        return False
    if point[1] < 0 or point[1] >= len(grid[0]):
        return False
    return True


def find_antinodes(loc_1, loc_2, grid):
    # use the taxi cab distance formula to find the antinodes
    x_distance = loc_1[0] - loc_2[0]
    y_distance = loc_1[1] - loc_2[1]

    antinodes = []
    antinode_1 = (loc_1[0] + x_distance, loc_1[1] + y_distance)
    antinode_2 = (loc_2[0] - x_distance, loc_2[1] - y_distance)

    if is_point_valid(antinode_1, grid):
        antinodes += [loc_1]
    if is_point_valid(antinode_2, grid):
        antinodes += [loc_2]

    return antinodes


def find_all_unique_antinodes(grid):
    antennas = find_antennas_location(grid)
    # create a list of antinodes
    unique_antinodes = []
    for _, locations in antennas.items():
        # find all combinations of locations
        for loc_1, loc_2 in itertools.combinations(locations, 2):
            antinodes = find_antinodes(loc_1, loc_2, grid)
            # add the antinodes to the list
            if antinodes:
                unique_antinodes += antinodes

    return list(set(unique_antinodes))


test_input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
test_answer = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
"""
test_sum = 14

my_grid = process_input(test_input)
my_antinodes = find_all_unique_antinodes(my_grid)
my_sum = len(my_antinodes)

if my_sum == test_sum:
    print("Test passed")
else:
    print(f"Test failed. Got {my_sum}. Expected {test_sum}")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_grid = process_input(my_string)

my_antinodes = find_all_unique_antinodes(my_grid)

my_sum = len(my_antinodes)

print(my_sum)
