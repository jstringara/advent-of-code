import re
import sys


def find_line_occurences(list_of_lines: list, pattern: str) -> int:
    forward_count = sum([len(re.findall(pattern, line)) for line in list_of_lines])
    backward_count = sum(
        [len(re.findall(pattern[::-1], line)) for line in list_of_lines]
    )

    return forward_count + backward_count


def find_occurences(input_string: str) -> int:
    """
    Function to find all occurences of the target string inside the input string.
    Occurences may be on the same line, vertical or diagonal, either forwards or backwards
    and even overlapping.
    """

    input_string = input_string.strip()

    pattern = r"XMAS"

    # get the horizontal occurences
    horizontal_lines = input_string.split("\n")
    horizontal_count = find_line_occurences(horizontal_lines, pattern)
    # get the vertical occurences
    vertical_lines = ["".join(col) for col in zip(*horizontal_lines)]
    vertical_count = find_line_occurences(vertical_lines, pattern)
    # diagonal
    length = len(horizontal_lines)
    diagonal_lines = ["".join(horizontal_lines[j][j] for j in range(length))]
    for i in range(1, length):
        # upper diagonal
        diagonal_lines = (
            ["".join(horizontal_lines[j][j + i] for j in range(length - i))]
            + diagonal_lines
            + ["".join(horizontal_lines[j + i][j] for j in range(length - i))]
        )
    diagonal_count = find_line_occurences(diagonal_lines, pattern)
    # anti-diagonal
    anti_diagonal_lines = [
        "".join(horizontal_lines[j][length - 1 - j] for j in range(length))
    ]
    for i in range(1, length):
        anti_diagonal_lines = (
            [
                "".join(
                    horizontal_lines[j][length - 1 - j - i] for j in range(length - i)
                )
            ]
            + anti_diagonal_lines
            + [
                "".join(
                    horizontal_lines[j + i][length - 1 - j] for j in range(length - i)
                )
            ]
        )
    anti_diagonal_count = find_line_occurences(anti_diagonal_lines, pattern)

    return horizontal_count + vertical_count + diagonal_count + anti_diagonal_count


test_string = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

test_answer = 18

if find_occurences(test_string) == test_answer:
    print("Test passed")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(find_occurences(my_string))
