def process_input(input_string: str) -> list[str]:
    (*character_list,) = input_string.strip()
    return character_list


def write_blocks(disk: list[str]) -> list[str]:
    # loop over the disk
    for i, char in enumerate(disk):
        # we find a block (even numbered index)
        if i % 2 == 0:
            # we write the block
            disk[i] = int(char) * str(i)
        if i % 2 != 0:
            # we write the block
            disk[i] = int(char) * "."
    return disk


def is_empty(block: str) -> bool:
    return block == "." * len(block)


test_string = "2333133121414131402"

my_input = process_input(test_string)
print(my_input)

my_blocks = write_blocks(my_input)

print("".join(my_blocks))
