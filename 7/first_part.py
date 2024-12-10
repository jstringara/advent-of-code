import sys


def process_input(input_string: str) -> list:
    # break the input into lines
    lines = input_string.strip().split("\n")

    # turn into a dictionary
    return [
        (int(line.split(":")[0]), [int(i) for i in line.split(":")[1].split()])
        for line in lines
    ]


def is_equation_possible(result, numbers, string=""):
    if string == "":
        string = str(numbers[0])
    if len(numbers) == 1:
        # Base case: if only one number is left, check if it equals the result
        print(f"{string} = {numbers[0]} -> {result}")
        return numbers[0] == result

    add_result = numbers[0] + numbers[1]
    mul_result = numbers[0] * numbers[1]

    # Left-to-right means we reduce the list step-by-step
    return is_equation_possible(
        result, [add_result] + numbers[2:], f"{string} + {numbers[1]}"
    ) or is_equation_possible(
        result, [mul_result] + numbers[2:], f"{string} * {numbers[1]}"
    )


test_string = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

test_answer = [
    True,  #  190: 10 19
    True,  #  3267: 81 40 27
    False,  # 83: 17 5
    False,  # 156: 15 6
    False,  # 7290: 6 8 6 15
    False,  # 161011: 16 10 13
    False,  # 192: 17 8 14
    False,  # 21037: 9 7 18 13
    True,  #  292: 11 6 16 20
]
test_sum = sum([190, 3267, 292])

my_input = process_input(test_string)

my_answer = [is_equation_possible(key, value) for key, value in my_input]
my_correct_equations = [
    key for key, value in my_input if is_equation_possible(key, value)
]
my_sum = sum(set(my_correct_equations))

if my_answer == test_answer and my_sum == test_sum:
    print("Test passed")
    print(my_sum)
else:
    print("Test failed")
    print(my_answer)

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_input = process_input(my_string)

my_correct_equations = [
    key for key, value in my_input if is_equation_possible(key, value)
]

print(sum(set(my_correct_equations)))
