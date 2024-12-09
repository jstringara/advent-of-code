import re
import sys


def process_input(input_string: str) -> list[str]:
    # break the input into lines
    map = input_string.strip().split("\n")

    return map


def initial_direction_and_position(map: list[str]) -> tuple[tuple[int, int], str]:
    # find the position of the guard
    for i, line in enumerate(map):
        guard_search = re.search(r"\^|v|<|>", line)
        if guard_search:
            # find its position
            j = guard_search.start()
            position = (i, j)
            match line[j]:
                case "^":
                    direction = "up"
                case "v":
                    direction = "down"
                case "<":
                    direction = "left"
                case ">":
                    direction = "right"
                case _:
                    raise ValueError("Invalid direction")
            return position, direction

    raise ValueError("No guard found")


def turn(direction: str) -> str:
    match direction:
        case "up":
            return "right"
        case "down":
            return "left"
        case "left":
            return "up"
        case "right":
            return "down"
        case _:
            raise ValueError("Invalid direction")


def find_next_turning_point(
    map: list[str], position: tuple[int, int], direction: str
) -> tuple[tuple[int, int], str]:
    # vertical search
    if direction == "up":
        for i in range(position[0] - 1, -1, -1):
            if map[i][position[1]] == "#":
                # return the turning points coordinates and turn 90 degrees
                return (i + 1, position[1]), turn(direction)
        # we reached the top of the map
        return (-1, position[1]), direction
    if direction == "down":
        for i in range(position[0] + 1, len(map)):
            if map[i][position[1]] == "#":
                return (i - 1, position[1]), turn(direction)
        return (len(map), position[1]), direction
    # horizontal search
    if direction == "left":
        for j in range(position[1] - 1, -1, -1):
            if map[position[0]][j] == "#":
                return (position[0], j + 1), turn(direction)
        return (position[0], -1), direction
    if direction == "right":
        for j in range(position[1] + 1, len(map[0])):
            if map[position[0]][j] == "#":
                return (position[0], j - 1), turn(direction)
        return (position[0], len(map[0])), direction
    # invalid direction
    # should never reach here
    raise ValueError("Invalid direction")


def in_between_points(starting_point: tuple[int, int], arrival_point: tuple[int, int]):
    # if they are the same point
    if starting_point == arrival_point:
        return []

    # check that at least one of the coordinates is the same
    if starting_point[0] != arrival_point[0] and starting_point[1] != arrival_point[1]:
        raise ValueError("Points are not in a straight line")

    # we go left to right
    if starting_point[0] == arrival_point[0] and starting_point[1] < arrival_point[1]:
        return [
            ((starting_point[0], j), "->")
            for j in range(starting_point[1] + 1, arrival_point[1])
        ]
    # we go right to left
    if starting_point[0] == arrival_point[0] and starting_point[1] > arrival_point[1]:
        return list(
            reversed(
                [
                    ((starting_point[0], j), "<-")
                    for j in range(arrival_point[1] + 1, starting_point[1])
                ]
            )
        )
    # if we go from top to bottom
    if starting_point[1] == arrival_point[1] and starting_point[0] < arrival_point[0]:
        return [
            ((i, starting_point[1]), "v")
            for i in range(starting_point[0] + 1, arrival_point[0])
        ]
    # if we go from bottom to top
    if starting_point[1] == arrival_point[1] and starting_point[0] > arrival_point[0]:
        return list(
            reversed(
                [
                    ((i, starting_point[1]), "^")
                    for i in range(arrival_point[0] + 1, starting_point[0])
                ]
            )
        )

    # should never reach here
    raise ValueError("Invalid points")


def move_guard(
    map: list[str],
    visited_points: list[tuple[tuple[int, int], str]],
    position: tuple[int, int],
    direction: str,
) -> tuple[list[tuple[tuple[int, int], str]], tuple[int, int], str]:
    # find the next turning point
    next_position, next_direction = find_next_turning_point(map, position, direction)

    # add the points in between to the visited points
    visited_points += in_between_points(position, next_position)
    if not is_out_of_bounds(map, next_position):
        visited_points.append((next_position, "+"))

    return visited_points, next_position, next_direction


def is_out_of_bounds(map: list[str], position: tuple[int, int]) -> bool:
    return (
        position[0] < 0
        or position[1] < 0
        or position[0] >= len(map)
        or position[1] >= len(map[0])
    )


def find_all_positions(map: list[str]):
    # get the initial position
    position, direction = initial_direction_and_position(map)
    # list to keep track of the points where we turned
    turning_points = []
    # list to keep track of the points we visited
    visited_points = [(position, "X")]
    # until we are out of bounds
    while not is_out_of_bounds(map, position):
        visited_points, next_position, next_direction = move_guard(
            map, visited_points, position, direction
        )
        # check if there was a change in direction, save the new direction
        if next_direction != direction:
            turning_points.append(next_position)
        # update
        position, direction = next_position, next_direction

    return turning_points, visited_points


def unique_points(visited_points):
    return set([point[0] for point in visited_points])


test_string = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

test_answer = """....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X.."""
test_sum = 41

test_map = process_input(test_string)

my_turning_points, my_visited_points = find_all_positions(test_map)

my_unique_points = unique_points(my_visited_points)

my_sum = len(my_unique_points)

if my_sum == test_sum:
    print("Test passed")
else:
    print(f"Test failed: {my_sum} != {test_sum}")
    print(my_visited_points)


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_map = process_input(my_string)

my_turning_points, my_visited_points = find_all_positions(my_map)

my_unique_points = unique_points(my_visited_points)

my_sum = len(my_unique_points)

print(my_sum)
