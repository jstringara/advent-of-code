import sys


def parse_input(input_string: str):
    map, moves = input_string.strip().split("\n\n")

    # make the map into a matrix of strings
    map = [list(line) for line in map.split()]

    moves_to_vector = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}

    moves = [moves_to_vector[char] for char in "".join(moves).replace("\n", "")]

    return map, moves


def get_initial_position(map):
    num_rows = len(map)
    num_cols = len(map[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if map[i][j] == "@":
                return (i, j)
    raise ValueError("No initial position found")


def add_direction(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def is_valid(position, map):
    i, j = position
    # is out of bound
    if i < 0 or i >= len(map):
        return False
    if j < 0 or j >= len(map[0]):
        return False
    # the position is occupied by an unmovable object
    if map[i][j] == "#":
        return False
    return True


def is_final(position, map):
    i, j = position
    if map[i][j] == ".":
        return True
    return False


def move_guard(position, direction, map):
    old_positions = [position]
    new_positions = [add_direction(old_positions[-1], direction)]

    while is_valid(new_positions[-1], map) and not is_final(new_positions[-1], map):
        old_positions.append(new_positions[-1])
        new_positions.append(add_direction(new_positions[-1], direction))

    # check if the last position was invalid
    if not new_positions or not is_valid(new_positions[-1], map):
        new_positions = old_positions

    return old_positions, new_positions


def update_map(map, old_positions, new_positions):
    moves = list(zip(old_positions, new_positions))
    for old_position, new_position in moves[::-1]:
        if old_position == new_position:
            break
        i, j = old_position
        k, h = new_position
        # invert the elements
        map[i][j], map[k][h] = map[k][h], map[i][j]
    return map


def compute_score(map):
    score = 0
    num_rows = len(map)
    num_cols = len(map[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if map[i][j] == "O":
                score += 100 * i + j
    return score


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

# setup the problem
map, moves = parse_input(my_string)
position = get_initial_position(map)

for move in moves:
    # get the old and new positions
    old_positions, new_positions = move_guard(position, move, map)
    # update the position
    position = new_positions[0]
    # update the map
    map = update_map(map, old_positions, new_positions)


score = compute_score(map)
print(score)
