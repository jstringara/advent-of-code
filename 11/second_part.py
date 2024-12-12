import sys


def process_input(input_string: str) -> list[str]:
    numbers = input_string.strip().split()
    return numbers


def blink_stone(visited) -> dict[str, int]:
    new_visited = {}
    for stone in list(visited.keys()):
        if stone == "0":
            new_visited["1"] = new_visited.get("1", 0) + visited["0"]
        elif len(stone) % 2 == 0:
            first_half = stone[: len(stone) // 2]
            new_visited[first_half] = new_visited.get(first_half, 0) + visited[stone]

            second_half = stone[len(stone) // 2 :].lstrip("0")
            second_half = "0" if not second_half else second_half
            new_visited[second_half] = new_visited.get(second_half, 0) + visited[stone]
        else:
            new_stone = str(int(stone) * 2024)
            new_visited[new_stone] = new_visited.get(new_stone, 0) + visited[stone]

    return new_visited


def blink(stones: list[str], blinks: int) -> dict[str, int]:
    visited = {stone: stones.count(stone) for stone in stones}
    for _ in range(blinks):
        visited = blink_stone(visited)

    return visited


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_stones = process_input(my_string)

my_visited = blink(my_stones, 75)

my_sum = sum(my_visited.values())

print(my_sum)
