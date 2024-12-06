import re
import sys


def find_occurences(input_string: str) -> int:
    """
    Find all crosses of the shape:
        M.S
        .A.
        M.S
    """

    pattern = r"(MAS|SAM)"

    input_string = input_string.strip()

    input_lines = input_string.split("\n")
    length = len(input_lines)

    count = 0

    # find all 3x3 submatrices
    for i in range(length - 2):
        for j in range(length - 2):
            # find the two diagonals of the submatrix
            diagonal = "".join([input_lines[i + k][j + k] for k in range(3)])
            diagonal_match = bool(re.match(pattern, diagonal))
            anti_diagonal = "".join([input_lines[i + 2 - k][j + k] for k in range(3)])
            anti_diagonal_match = bool(re.match(pattern, anti_diagonal))

            # submatrix = "\n".join([input_lines[i + k][j : j + 3] for k in range(3)])
            #
            #             print(f"""Submatrix:
            # {submatrix}
            # First diagonal: {diagonal}
            # Second diagonal: {anti_diagonal}
            # Is_match: {diagonal_match and anti_diagonal_match}
            # """)

            count += int(diagonal_match and anti_diagonal_match)

    return count


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

test_answer = 9

if find_occurences(test_string) == test_answer:
    print("Test passed")
else:
    print("Test failed")
    print(find_occurences(test_string))

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(find_occurences(my_string))
