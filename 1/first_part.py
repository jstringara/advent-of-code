import sys


def find_paired_differences(input_string: str) -> list[int]:
    lines = input_string.strip().split("\n")

    left_list = [int(x.split()[0]) for x in lines]
    right_list = [int(x.split()[1]) for x in lines]

    left_list.sort()
    right_list.sort()

    return [abs(x - y) for x, y in zip(left_list, right_list)]


test_input = """3   4
4   3
2   5
1   3
3   9
3   3"""

test_output = [2, 1, 0, 1, 2, 5]

if test_output == find_paired_differences(test_input):
    print("Test passed")
else:
    print("Test failed")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(sum(find_paired_differences(my_string)))
