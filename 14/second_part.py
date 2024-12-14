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


def get_grid(robots, grid_sizes):
    grid = [[0 for _ in range(grid_sizes[0])] for _ in range(grid_sizes[1])]
    # count the number of robot in each position
    for robot in robots:
        x, y = robot["position"]
        if grid[y][x] == 0:
            grid[y][x] = 1

    return grid


def has_horizontal_bar(grid):
    for row in grid:
        # check if there is a continguous horizontal bar
        num_ones = 8
        if sum(row) > num_ones:
            # find all the ones in the row and their next num_ones elements
            ones = [sum(row[i : i + num_ones]) for i in range(len(row) - num_ones)]
            # check if they are continguous
            return any([one == num_ones for one in ones])

    return False


def has_vertical_bar(grid):
    # rotate the grid 90 degrees clockwise
    rotated_grid = [list(row) for row in zip(*grid[::-1])]

    return has_horizontal_bar(rotated_grid)


def plot_grid(grid):
    for row in grid:
        print("".join(["#" if cell == 1 else "." for cell in row]))


def find_tree(robots, grid_sizes):
    # iterate moving the robots
    count = 0
    grid = get_grid(robots, grid_sizes)
    while not has_horizontal_bar(grid) and not has_vertical_bar(grid):
        robots = compute_final_positions(robots, 1, grid_sizes)
        grid = get_grid(robots, grid_sizes)
        count += 1
    plot_grid(grid)
    return count


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()
my_grid_sizes = (101, 103)
my_robots = parse_input(my_string)
count = find_tree(my_robots, my_grid_sizes)
print(count)
