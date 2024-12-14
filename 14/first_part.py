import sys
import re


def parse_input(input_string: str) -> list:
    # split into lines
    lines = input_string.strip().split("\n")

    # parse the position and velocity
    # of each robot
    robots = []
    for line in lines:
        position = re.search(r"p=(-?\d{1,3}),(-?\d{1,3})", line)
        velocity = re.search(r"v=(-?\d{1,3}),(-?\d{1,3})", line)
        if position and velocity:
            x, y = map(int, position.groups())
            dx, dy = map(int, velocity.groups())
            robots.append({"position": (x, y), "velocity": (dx, dy)})

    return robots


def move_robot(robot, seconds, grid_sizes):
    x, y = robot["position"]
    dx, dy = robot["velocity"]

    x = x + dx * seconds
    y = y + dy * seconds

    x = x % grid_sizes[0]
    y = y % grid_sizes[1]

    if x < 0:
        x += grid_sizes[0]
    if y < 0:
        y += grid_sizes[1]

    return {"position": (x, y), "velocity": (dx, dy)}


def compute_final_positions(robots, seconds, grid_sizes):
    return [move_robot(robot, seconds, grid_sizes) for robot in robots]


def assign_quadrant(position, grid_sizes):
    x, y = position
    half_x, half_y = grid_sizes[0] // 2, grid_sizes[1] // 2
    if x < half_x and y < half_y:
        return 1
    elif x > half_x and y < half_y:
        return 2
    elif x < half_x and y > half_y:
        return 3
    elif x > half_x and y > half_y:
        return 4
    return None


def compute_quadrants(robots, grid_sizes):
    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        position = robot["position"]
        quadrant = assign_quadrant(position, grid_sizes)
        if quadrant:
            quadrants[quadrant] += 1
    return list(quadrants.values())


def compute_safety_score(quadrants):
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def print_grid(robots, grid_sizes):
    grid = [["." for _ in range(grid_sizes[0])] for _ in range(grid_sizes[1])]
    # count the number of robot in each position
    positions = {}
    for robot in robots:
        x, y = robot["position"]
        positions[(x, y)] = positions.get((x, y), 0) + 1
    for position, count in positions.items():
        x, y = position
        grid[y][x] = str(count)
    for row in grid:
        print("".join(row))


test_input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

test_quadrants = [1, 3, 4, 1]
test_answer = 12
test_grid_sizes = (11, 7)

test_robots = parse_input(test_input)
my_robots = compute_final_positions(test_robots, 100, test_grid_sizes)
my_quadrants = compute_quadrants(my_robots, test_grid_sizes)
my_score = compute_safety_score(my_quadrants)

if my_quadrants == test_quadrants and my_score == test_answer:
    print("Test passed")
else:
    print(f"Test failed: {my_quadrants} != {test_quadrants}")
    print(f"Test failed: {my_score} != {test_answer}")


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_grid_sizes = (101, 103)
my_robots = parse_input(my_string)
my_robots = compute_final_positions(my_robots, 100, my_grid_sizes)
my_quadrants = compute_quadrants(my_robots, my_grid_sizes)

my_score = compute_safety_score(my_quadrants)
print(my_score)
