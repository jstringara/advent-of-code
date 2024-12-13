import sys


def process_input(input_string: str) -> list:
    return [list(row) for row in input_string.strip().split("\n")]


def find_adjacent_points(matrix, point):
    """Return the adjacent points to the given point"""

    adjacent_points = []
    i, j = point
    # up case
    if i > 0 and matrix[i - 1][j] == matrix[i][j]:
        adjacent_points.append((i - 1, j))
    # down
    if i < len(matrix) - 1 and matrix[i + 1][j] == matrix[i][j]:
        adjacent_points.append((i + 1, j))
    # left
    if j > 0 and matrix[i][j - 1] == matrix[i][j]:
        adjacent_points.append((i, j - 1))
    # right
    if j < len(matrix[0]) - 1 and matrix[i][j + 1] == matrix[i][j]:
        adjacent_points.append((i, j + 1))

    return adjacent_points


def is_in_bounds(matrix, point):
    i, j = point
    return 0 <= i < len(matrix) and 0 <= j < len(matrix[0])


def check_direction(point, matrix, direction):
    """
    There is an angle in a certain direction if either both adjacent points are different from the origin
    or both are the same and the diagonal is different from the origin.
    i.e. for the top_left direction:
        . O .    O X .
        O X . or X X .
        . . .    . . .
    """
    i, j = point
    origin = matrix[i][j]

    point_1 = (point[0] + direction[0][0], point[1] + direction[0][1])
    point_2 = (point[0] + direction[1][0], point[1] + direction[1][1])
    diagonal = (point_1[0] + direction[1][0], point_1[1] + direction[1][1])

    point_1 = matrix[point_1[0]][point_1[1]] if is_in_bounds(matrix, point_1) else ""
    point_2 = matrix[point_2[0]][point_2[1]] if is_in_bounds(matrix, point_2) else ""
    diagonal = (
        matrix[diagonal[0]][diagonal[1]] if is_in_bounds(matrix, diagonal) else ""
    )

    # both different
    if point_1 != origin and point_2 != origin:
        return 1

    if point_1 == origin and point_2 == origin and diagonal != origin:
        return 1

    return 0


def compute_corners(matrix, point):
    """Return the number of corners of the given point"""

    num_corners = 0

    directions = [
        [(-1, 0), (0, -1)],  # top_left
        [(-1, 0), (0, 1)],  # top_right
        [(1, 0), (0, -1)],  # bottom_left
        [(1, 0), (0, 1)],  # bottom_right
    ]

    num_corners = sum(
        check_direction(point, matrix, direction) for direction in directions
    )

    return num_corners


def find_area_and_sides(matrix, i, j):
    area = 0
    queue = [(i, j)]
    visited = [(i, j)]
    corners = 0
    while queue:
        # add the item to the visited list
        visited.append(queue.pop(0))
        point = visited[-1]
        # find adjacent points
        adjacent_points = find_adjacent_points(matrix, point)
        # compute area and number of sides
        area += 1
        corners += compute_corners(matrix, point)
        # update the queue
        queue += [
            neighbor for neighbor in adjacent_points if neighbor not in visited + queue
        ]
    return area, corners, visited


def prices(matrix: list[list[str]]):
    visited = []
    total_price = 0
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if (i, j) not in visited:
                # explore the area
                area, num_sides, new_visited = find_area_and_sides(matrix, i, j)
                visited += new_visited
                total_price += area * num_sides
    return total_price


test_input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
test_answer = 1206


test_price = prices(process_input(test_input))

if test_price == test_answer:
    print("Test passed")
else:
    print("Test failed")

with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

total_price = prices(process_input(my_string))

print(total_price)
