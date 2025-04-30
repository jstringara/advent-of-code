import re
import sys


def parse_input(input):
    input = input.strip()

    # get the registers
    register_A = re.search(r"Register A: (\d+)", input)
    register_B = re.search(r"Register B: (\d+)", input)
    register_C = re.search(r"Register C: (\d+)", input)

    registers = {}
    if register_A and register_B and register_C:
        registers["A"] = int(register_A.group(1))
        registers["B"] = int(register_B.group(1))
        registers["C"] = int(register_C.group(1))

    instructions = re.search(r"Program: (\d|,)*", input)
    if instructions:
        instructions = re.findall(r"(\d)", instructions.group(0))
        instructions = [int(i) for i in instructions]

    return instructions, registers


def adv(input, registers, pointer):
    """
    The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
    """
    numerator = registers["A"]
    denominator = 2 ** combo_operand(input, registers)
    result = int(numerator / denominator)

    registers["A"] = result

    return pointer + 2, None


def bxl(input, registers, pointer):
    """
    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
    """
    registers["B"] = input ^ registers["B"]

    return pointer + 2, None


def bst(input, registers, pointer):
    """
    The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
    """

    registers["B"] = combo_operand(input, registers) % 8

    return pointer + 2, None


def jnz(input, registers, pointer):
    """
    The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
    """
    if registers["A"] == 0:
        return pointer + 2, None
    pointer = input

    return pointer, None


def bxc(input, registers, pointer):
    """
    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
    """
    registers["B"] = registers["B"] ^ registers["C"]

    return pointer + 2, None


def out(input, registers, pointer):
    """
    The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
    """
    result = combo_operand(input, registers) % 8

    return pointer + 2, result


def bdv(input, registers, pointer):
    """
    The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
    """
    numerator = registers["A"]
    denominator = 2 ** combo_operand(input, registers)
    result = int(numerator / denominator)

    registers["B"] = result

    return pointer + 2, None


def cdv(input, registers, pointer):
    """
    The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
    """
    numerator = registers["A"]
    denominator = 2 ** combo_operand(input, registers)
    result = int(numerator / denominator)

    registers["C"] = result

    return pointer + 2, None


def combo_operand(value, registers):
    if value in (0, 1, 2, 3):
        return value
    if value == 4:
        return registers["A"]
    if value == 5:
        return registers["B"]
    if value == 6:
        return registers["C"]

    raise ValueError("Invalid combo operand")


def run_program(instructions, registers):
    operations = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    pointer = 0
    outputs = []
    while pointer < len(instructions):
        opcode = instructions[pointer]
        operand = instructions[pointer + 1]

        pointer, output = operations[opcode](operand, registers, pointer)

        if output is not None:
            outputs.append(output)

    return outputs


# open the file in the same directory as the script
with open(sys.path[0] + "/my.txt", "r") as f:
    my_string = f.read()

instructions, registers = parse_input(my_string)
print(instructions)
print(registers)

outputs = run_program(instructions, registers)

print(",".join(map(str, outputs)))
