import sys


def is_couple_safe(first_num: int, second_num: int, sign) -> bool:
    """
    Check if a couple is safe.
    """
    if sign * (second_num - first_num) > 3:
        return False
    if sign * (second_num - first_num) < 1:
        return False
    if sign * (second_num - first_num) < 0:
        return False

    return True


def is_report_safe(report: list[int]) -> bool:
    """
    A report is safe if it is all increasin or all decreasing.
    And if the variation is between 1 and 3.
    """

    sign = 1 if (report[1] - report[0]) > 0 else -1

    for i in range(1, len(report)):
        if not is_couple_safe(report[i - 1], report[i], sign):
            return False

    return True


def count_safe_reports(reports: str) -> list[bool]:
    """
    Count the number of safe reports.
    """

    lines = reports.strip().split("\n")
    lines = [list(map(int, x.split())) for x in lines]

    output = [is_report_safe(x) for x in lines]

    return output


test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

test_output = [True, False, False, False, False, True]

if test_output == count_safe_reports(test_input):
    print("Test passed")
else:
    print("Test failed")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(sum(count_safe_reports(my_string)))
