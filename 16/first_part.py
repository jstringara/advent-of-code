import sys


def parse_input(input_string):
    map = [list(line) for line in input_string.strip().split("\n")]

    return map


def initial_position_and_direction(map):
    for i, line in enumerate(map):
        for j, char in enumerate(line):
            if char == "S":
                return (i, j), (0, 1)
    raise ValueError("No starting position found")


def final_position(map):
    for i, line in enumerate(map):
        for j, char in enumerate(line):
            if char == "E":
                return (i, j)
    raise ValueError("No starting position found")


def clockwise(direction):
    turn = {
        # right -> down
        (0, 1): (1, 0),
        # down -> left
        (1, 0): (0, -1),
        # left -> up
        (0, -1): (-1, 0),
        # up -> right
        (-1, 0): (0, 1),
    }

    return turn[direction]


def counterclockwise(direction):
    turn = {
        # right -> up
        (0, 1): (-1, 0),
        # down -> right
        (1, 0): (0, 1),
        # left -> down
        (0, -1): (1, 0),
        # up -> left
        (-1, 0): (0, -1),
    }

    return turn[direction]


def go_straight(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def is_valid_move(position, map):
    i, j = position
    if map[i][j] != "#":
        return True
    return False


def possible_moves(position, direction, map):
    available_moves = []

    straight = go_straight(position, direction)
    if is_valid_move(straight, map):
        available_moves.append(straight)

    clockwise_move = go_straight(position, clockwise(direction))
    if is_valid_move(clockwise_move, map):
        available_moves.append(clockwise_move)

    counterclockwise_move = go_straight(position, counterclockwise(direction))
    if is_valid_move(counterclockwise_move, map):
        available_moves.append(counterclockwise_move)

    return available_moves


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

# setup the problem
map = parse_input(my_string)
position, direction = initial_position_and_direction(map)
