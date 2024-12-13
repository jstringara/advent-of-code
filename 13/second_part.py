import sys
import re


def process_input(input_string: str) -> list[dict]:
    systems_strings = re.split(r"\n\n", input_string)

    systems = []
    for system_string in systems_strings:
        # match the values using regex
        button_A = re.search(r"Button A: X\+(\d{2}), Y\+(\d{2})", system_string)
        button_B = re.search(r"Button B: X\+(\d{2}), Y\+(\d{2})", system_string)
        solution = re.search(r"Prize: X=(\d*), Y=(\d*)", system_string)
        if button_A and button_B and solution:
            systems.append(
                {
                    "button_A": map(int, button_A.groups()),
                    "button_B": map(int, button_B.groups()),
                    "solution": map(int, solution.groups()),
                }
            )

    return systems


def solve_system(system: dict) -> tuple:
    a, c = system["button_A"]
    b, d = system["button_B"]
    z_1, z_2 = system["solution"]
    # add the value for part 2
    conversion_error = 10000000000000
    z_1 += conversion_error
    z_2 += conversion_error

    # solve the systme of equations
    y = (z_2 - c * z_1 / a) / (d - c * b / a)
    x = (z_1 - b * y) / a

    return x, y


def is_integer(value: float) -> bool:
    """Check if a float value is an integer"""
    difference = abs(value - int(value + 0.5))
    epsilon = 1e-3

    return difference < epsilon


def compute_solution(system: dict) -> tuple[int, int]:
    # get the real valued solution
    x_real, y_real = solve_system(system)
    # check if the solutions is an integer
    if is_integer(x_real) and is_integer(y_real):
        return int(x_real + 0.5), int(y_real + 0.5)
    return (0, 0)


def solve_systems(systems: list[dict]) -> list[tuple]:
    solutions = []
    for system in systems:
        solution = compute_solution(system)
        if solution:
            solutions.append(solution)
    return solutions


def compute_price(solutions: list[tuple]) -> int:
    return sum(x * 3 + y for x, y in solutions)


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_systems = process_input(my_string)
my_solutions = solve_systems(my_systems)
my_price = compute_price(my_solutions)
print(my_price)
