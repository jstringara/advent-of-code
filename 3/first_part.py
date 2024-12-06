import re
import sys


def find_sum_of_multiplications(input_string):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, input_string)
    result = 0
    for match in matches:
        result += int(match[0]) * int(match[1])
    return result


test_string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
test_answer = 161

if find_sum_of_multiplications(test_string) == test_answer:
    print("Test passed")
else:
    print("Test failed")
    print(find_sum_of_multiplications(test_string))

# read input
# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(find_sum_of_multiplications(my_string))
