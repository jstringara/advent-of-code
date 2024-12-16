import sys


def parse_input(input_string: str):
    map, moves = input_string.strip().split("\n\n")

    # make the map into a matrix of strings (according with the new rules)
    map = [
        list(
            line.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )
        for line in map.split()
    ]

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


def find_neighbors(position, map, direction):
    """
    Find all neighbors of a given point in a given direction
    according to the lanternfish map
    """

    i, j = position
    neighbors = []
    # it's the guard, just the one right in front
    if map[i][j] == "@":
        neighbors = [add_direction(position, direction)]
    # left element of the block, also add the one to the right
    if map[i][j] == "[":
        neighbors = [(i, j + 1), add_direction(position, direction)]
    # flipped image of the block
    if map[i][j] == "]":
        neighbors = [(i, j - 1), add_direction(position, direction)]

    return list(set(neighbors))


def move_guard(position, direction, map):
    # list to keep track of all old and new positions
    visited = []
    queue = [position]

    # apply a kind of flood fill algorithm
    while queue:
        # move from the queue to visited
        visited.append(queue.pop(0))
        # find its neighbors and add to the queue
        neighbors = find_neighbors(visited[-1], map, direction)
        # filter out the already visited neighbors
        neighbors = [
            neighbor for neighbor in neighbors if neighbor not in visited + queue
        ]
        queue += neighbors

    # filter out the final nodes
    leaves = [
        position for position in visited if map[position[0]][position[1]] in ("#", ".")
    ]
    # filter out the non final nodes
    old_positions = [
        position
        for position in visited
        if map[position[0]][position[1]] not in ("#", ".")
    ]

    # check if all leaves are valid
    if all([is_valid(leaf, map) for leaf in leaves]):
        new_positions = [
            add_direction(position, direction) for position in old_positions
        ]
    else:
        # otherwise, don't move
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
            if map[i][j] == "[":
                score += 100 * i + j
    return score


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

# setup the problem
map, moves = parse_input(my_string)
position = get_initial_position(map)

# print the first 10 moves
for move in moves:
    # get the old and new positions
    old_positions, new_positions = move_guard(position, move, map)
    # update the position
    position = new_positions[0]
    # update the map
    map = update_map(map, old_positions, new_positions)

score = compute_score(map)
print(score)
