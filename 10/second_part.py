import sys


def process_input(input_string: str) -> list[list[int]]:
    # break the input into lines
    lines = input_string.strip().split("\n")

    map = []
    for line in lines:
        map.append([int(x) for x in line])

    return map


def find_all_trailheads(map: list[list[int]]) -> list[tuple[int, int]]:
    trailheads = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def find_trail_recurse(trail: list[tuple[int, int]], map: list[list[int]]):
    i, j = trail[-1]
    # return case
    if map[i][j] == 9:
        return trail
    # explore the adjacent cells
    up_trail = []
    down_trail = []
    left_trail = []
    right_trail = []
    if not i - 1 < 0 and map[i - 1][j] == map[i][j] + 1:
        up_trail = find_trail_recurse(trail + [(i - 1, j)], map)
    if not i + 1 >= len(map) and map[i + 1][j] == map[i][j] + 1:
        down_trail = find_trail_recurse(trail + [(i + 1, j)], map)
    if not j - 1 < 0 and map[i][j - 1] == map[i][j] + 1:
        left_trail = find_trail_recurse(trail + [(i, j - 1)], map)
    if not j + 1 >= len(map[0]) and map[i][j + 1] == map[i][j] + 1:
        right_trail = find_trail_recurse(trail + [(i, j + 1)], map)

    trails = [
        trail for trail in [up_trail, down_trail, left_trail, right_trail] if trail
    ]

    # make into a list of lists
    trails = sum(trails, [])

    return trails


def find_trails_from_head(
    trailhead: tuple[int, int], map: list[list[int]]
) -> list[list[tuple[int, int]]]:
    trails = []
    trails += find_trail_recurse([trailhead], map)
    # chunk the trails into a list of lists
    trail_length = 10
    trails = [trails[i : i + trail_length] for i in range(0, len(trails), trail_length)]
    return trails


def compute_rating(trails: list[list[tuple[int, int]]]) -> int:
    # find all the distinct final points
    return len(trails)


test_input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
test_num_trailheads = 81
test_scores = [20, 24, 10, 4, 1, 4, 5, 8, 5]
test_sum = sum(test_scores)

my_map = process_input(test_input)
my_trailheads = find_all_trailheads(my_map)

my_trails = {
    trailhead: find_trails_from_head(trailhead, my_map) for trailhead in my_trailheads
}
my_scores = [compute_rating(trail) for trail in my_trails.values()]

my_sum = sum(my_scores)
my_num_trailheads = len(my_trailheads)

if (
    my_sum == test_sum
    and my_scores == test_scores
    and test_num_trailheads == my_num_trailheads
):
    print("Test passed")
else:
    print(f"""Test failed.
Found {my_sum}. Expected {test_sum}.
Found {my_scores}. Expected {test_scores}.
Trailheads: {my_num_trailheads}. Expected {test_num_trailheads}
    {my_trailheads}
""")
    # find all the trails
    for trailhead, trails in my_trails.items():
        print(f" ---- TrailHead {trailhead} ----")
        for trail in trails:
            print(f""" Trail: {trail}
Values: {[my_map[i][j] for i, j in trail]}""")


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_map = process_input(my_string)

my_trailheads = find_all_trailheads(my_map)

my_trails = {
    trailhead: find_trails_from_head(trailhead, my_map) for trailhead in my_trailheads
}

my_scores = [compute_rating(trail) for trail in my_trails.values()]

my_sum = sum(my_scores)
print(my_sum)
