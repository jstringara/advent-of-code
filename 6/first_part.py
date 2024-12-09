import re
import sys


def process_input(input_string: str) -> list[str]:
    # break the input into lines
    map = input_string.strip().split("\n")

    return map


def initial_direction_and_position(map: list[str]) -> tuple[tuple, str]:
    # find the position of the guard
    for i, line in enumerate(map):
        guard_search = re.search(r"\^|v|<|>", line)
        if guard_search:
            # find its position
            j = guard_search.start()
            position = (i, j)
            # find the direction of the guard
            character_at_position = line[j]
            match character_at_position:
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


def find_next_move(
    map: list[str], position: tuple[int, int], direction: str
) -> tuple[tuple, str]:
    # find the next position of the guard if it goes straight
    match direction:
        case "up":
            next_position = (position[0] - 1, position[1])
        case "down":
            next_position = (position[0] + 1, position[1])
        case "left":
            next_position = (position[0], position[1] - 1)
        case "right":
            next_position = (position[0], position[1] + 1)
        case _:
            raise ValueError("Invalid direction")

    # check if going straight is valid (we are not out-of-bounds and there is not a wall)
    if (
        not is_out_of_bounds(map, next_position)
        and map[next_position[0]][next_position[1]] == "#"
    ):
        # turn the direction 90 degrees to the right
        match direction:
            case "up":
                next_direction = "right"
            case "down":
                next_direction = "left"
            case "left":
                next_direction = "up"
            case "right":
                next_direction = "down"
        return find_next_move(map, position, next_direction)

    # we are going straight, no change in direction
    return next_position, direction


def move_guard(
    map: list[str], position: tuple[int, int], direction: str
) -> tuple[list[str], tuple, str]:
    # find the next position of the guard
    next_position, next_direction = find_next_move(map, position, direction)
    # put an X in the current position
    map[position[0]] = "".join(
        [
            map[position[0]][: position[1]],
            "X",
            map[position[0]][position[1] + 1 :],
        ]
    )
    # if the next position is out of bounds
    if is_out_of_bounds(map, next_position):
        return map, next_position, next_direction
    # put the guard in the next position
    char = "G"
    if next_direction == "up":
        char = "^"
    if next_direction == "down":
        char = "v"
    if next_direction == "left":
        char = "<"
    if next_direction == "right":
        char = ">"
    map[next_position[0]] = "".join(
        [
            map[next_position[0]][: next_position[1]],
            char,
            map[next_position[0]][next_position[1] + 1 :],
        ]
    )

    return map, next_position, next_direction


def is_out_of_bounds(map: list[str], position) -> bool:
    return (
        position[0] < 0
        or position[1] < 0
        or position[0] >= len(map)
        or position[1] >= len(map[0])
    )


def distance(point_1: tuple[int, int], point_2: tuple[int, int]) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def find_all_positions(map: list[str]):
    # get the initial position
    position, direction = initial_direction_and_position(map)
    # list to keep track of the 'nodes' of the graph
    turning_points = [position]
    # list to keep track of the points we visited
    visited_points = [position]
    # adjacency matrix to map how turning points relate to one another
    adjacency_matrix = []
    while not is_out_of_bounds(map, position):
        map, next_position, next_direction = move_guard(map, position, direction)
        # check if there was a change in direction and save the new direction
        if next_direction != direction:
            turning_points.append(position)
        if position:
            visited_points.append(position)
        # update
        position, direction = next_position, next_direction

    return map, turning_points, visited_points


test_string = """....#.....
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

my_map, my_turning_points, my_visited_points = find_all_positions(test_map)

my_answer = "\n".join(my_map)
my_sum = len(set(my_visited_points))

if my_answer == test_answer and my_sum == test_sum:
    print("Test passed")
else:
    print(f"Test failed: {my_answer} != {test_answer}")
    print(f"Test failed: {my_sum} != {test_sum}")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_map = process_input(my_string)

(
    my_map,
    my_turning_points,
    my_visited_points,
) = find_all_positions(my_map)
my_sum = len(set(my_visited_points))

print(my_sum)
