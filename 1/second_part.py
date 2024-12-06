import sys


def find_similarity_scores(input_string: str) -> list[int]:
    lines = input_string.strip().split("\n")

    left_list = [int(x.split()[0]) for x in lines]
    right_list = [int(x.split()[1]) for x in lines]

    similarity_scores = [entry * right_list.count(entry) for entry in left_list]

    return similarity_scores


test_input = """3   4
4   3
2   5
1   3
3   9
3   3"""

test_output = [9, 4, 0, 0, 9, 9]

if test_output == find_similarity_scores(test_input):
    print("Test passed")
else:
    print(f"Test failed: {find_similarity_scores(test_input)}")

# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

print(sum(find_similarity_scores(my_string)))
