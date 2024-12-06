import re
import sys


def find_sum_of_multiplications(input_string):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, input_string)
    result = 0
    for match in matches:
        result += int(match[0]) * int(match[1])
    return result


def find_blocks(input_string):
    # collate all lines
    input_string = input_string.replace("\n", " ")

    first_block_pattern = r"(.*?)don't\(\)"
    block_pattern = r"do\(\)(.*?)(?:don't\(\))"
    last_block_pattern = r"do\(\)(.*?)\Z"
    valid_blocks = []

    # find the first block, ignoring the first 'do()' if present
    first_match = re.match(first_block_pattern, input_string)
    if first_match:
        valid_blocks += [first_match.group(0)]
        input_string = input_string[first_match.span(0)[1] :]
    # add the in-between blocks start with do() and end in don't()
    inbetween_matches = list(re.finditer(block_pattern, input_string))
    if inbetween_matches:
        valid_blocks += [match.group(0) for match in inbetween_matches]
        input_string = input_string[inbetween_matches[-1].span(0)[1] :]
    # find the last block
    last_match = re.search(last_block_pattern, input_string)
    if last_match:
        valid_blocks += [last_match.group(0)]

    result = 0

    for block in valid_blocks:
        if block:
            result += find_sum_of_multiplications(block)

    return result


test_string = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)
test_answer = 48

if find_blocks(test_string) == test_answer:
    print("Test passed")
else:
    print("Test failed")
    print(find_blocks(test_string))

# read input
# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(find_blocks(my_string))
