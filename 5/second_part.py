import sys


def process_input(input_string: str) -> tuple[dict[int, list], list]:
    # break the input into two parts
    rules, manuals = input_string.strip().split("\n\n")

    # process the rules into a dictionary
    rules_dict = {}
    for rule in rules.split("\n"):
        key, value = rule.split("|")
        key = int(key)
        value = int(value)
        rules_dict[key] = rules_dict.get(key, []) + [value]

    manuals = [list(map(int, manual.split(","))) for manual in manuals.split("\n")]

    return rules_dict, manuals


def is_ordered(manual: list[int], rules_dict: dict[int, list[int]]) -> bool:
    # iterate over all elements
    for i in range(len(manual) - 1):
        # check that all following items appear in the list
        if not set(manual[i + 1 :]).issubset(set(rules_dict.get(manual[i], []))):
            return False

    return True


def reorder(manual: list[int], rules_dict: dict[int, list[int]]):
    """
    Reorder the manuals to conform to the gives rules.
    The key must appear before all the values in its list
    """
    for i in range(len(manual) - 1):
        # check that all following items appear in the list
        # if not, move the key to the end of the list
        # and repeat the process
        if not set(manual[i + 1 :]).issubset(set(rules_dict.get(manual[i], []))):
            manual.append(manual.pop(i))
            return reorder(manual, rules_dict)
    return manual


test_string = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

test_answer = [True, True, True, False, False, False]
test_middle_pages = [47, 29, 47]
test_sum = 123

test_rules_dict, test_manuals = process_input(test_string)

my_answer = [is_ordered(manual, test_rules_dict) for manual in test_manuals]
unorderd_manuals = [
    manual for answer, manual in zip(my_answer, test_manuals) if not answer
]
# reorder the manuals
unordered_manuals = [reorder(manual, test_rules_dict) for manual in unorderd_manuals]

my_middle_pages = [manual[len(manual) // 2] for manual in unordered_manuals]
my_sum = sum(my_middle_pages)

if (
    my_answer == test_answer
    and my_middle_pages == test_middle_pages
    and my_sum == test_sum
):
    print("Test passed")
else:
    print(f"Test failed: {my_answer} != {test_answer}")
    print(f"Test failed: {my_middle_pages} != {test_middle_pages}")
    print(f"Test failed: {my_sum} != {test_sum}")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

my_rules_dict, my_manuals = process_input(my_string)

my_answer = [is_ordered(manual, my_rules_dict) for manual in my_manuals]
# find the unordered manuals
my_unordered_manuals = [
    manual for answer, manual in zip(my_answer, my_manuals) if not answer
]
# reorder the manuals
my_unordered_manuals = [
    reorder(manual, my_rules_dict) for manual in my_unordered_manuals
]

my_middle_pages = [manual[len(manual) // 2] for manual in my_unordered_manuals]

my_sum = sum(my_middle_pages)

print(my_sum)
