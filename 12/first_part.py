import sys


def process_input(input_string: str) -> list:
    """Convert the input string into a list of lists"""
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


def find_area_and_perimeter(matrix, starting_point):
    area = 0
    perimeter = 0
    queue = [starting_point]
    visited = [starting_point]
    while queue:
        # add the item to the visited list
        visited.append(queue.pop(0))
        point = visited[-1]
        # find adjacent points
        adjacent_points = find_adjacent_points(matrix, point)
        # compute the area and perimeter
        area += 1
        perimeter += 4 - len(adjacent_points)
        # update the queue
        queue += [
            neighbor for neighbor in adjacent_points if neighbor not in visited + queue
        ]
    return area, perimeter, visited


def prices(matrix: list[list[str]]):
    visited = []
    total_price = 0
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    for i in range(num_rows):
        for j in range(num_cols):
            point = (i, j)
            if point not in visited:
                # explore the area
                area, perimeter, new_visited = find_area_and_perimeter(matrix, point)
                visited += new_visited
                total_price += area * perimeter
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
test_answer = 1930


test_price = prices(process_input(test_input))

if test_price == test_answer:
    print("Test passed")
else:
    print("Test failed")

with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

total_price = prices(process_input(my_string))

print(total_price)
