import sys
import re

class Computer():

    def __init__(self, A, B, C, PC):
        self.A = A
        self.initial_A = A
        self.B = B
        self.initial_B = B
        self.C = C
        self.initial_C = C
        self.PC = PC
        self.output = []
        self.program = []
    
    def combo_value(self, op):
        if op <= 3:
            return op
        if op == 4:
            return self.A
        if op == 5:
            return self.B
        if op == 6:
            return self.C
        if op >= 7:
            print(f"Error op combo is bigger than 6: {op}")
            exit(1)
    def adv(self, op):
        # Equivalent to A = A >> combo(op)
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.A = res
        self.PC += 2
    def bxl(self, op):
        # Equivalent to B = B XOR op
        self.B = self.B ^ op
        self.PC += 2
    def bst(self, op):
        # Equivalent to B = last 3 bits of combo(op)
        op = self.combo_value(op)
        self.B = op%8
        self.PC += 2
    def jnz(self, op):
        if self.A != 0:
            self.PC = op
        else :
            self.PC += 2
    def bxc(self, op):
        # Equivalent to B = B XOR C
        self.B = self.B ^ self.C
        self.PC += 2
    def out(self, op, expected_output = []):
        # Equivalent to output += last 3 bits of combo(op)
        op = self.combo_value(op)
        self.output.append(op%8)
        if len(expected_output) > 0:
            if len(self.output) - 1 >= len(expected_output):
                return True
            else:
                if self.output[-1] != expected_output[len(self.output) - 1]:
                    return True
            self.PC += 2
            return False
        self.PC+=2
    def bdv(self, op):
        # Equivalent to B = A >> combo(op)
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.B = res
        self.PC += 2
    def cdv(self, op):
        # Equivalent to C = A >> combo(op)
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.C = res
        self.PC += 2


    def run_single_instruction(self, debug = False, expected_output = []):
        if self.program == []:
            print("Error program is empty")
            exit(1)
        else:
            if self.PC > (len(self.program) -2):
                return True
            else:
                opcode = self.program[self.PC]
                op = self.program[self.PC + 1]
                if opcode == 0:
                    self.adv(op)
                elif opcode == 1:
                    self.bxl(op)
                elif opcode == 2:
                    self.bst(op)
                elif opcode == 3:
                    self.jnz(op)
                elif opcode == 4:
                    self.bxc(op)
                elif opcode == 5:
                    res = self.out(op, expected_output)
                    
                    if debug:
                        print(f"Doing opcode : {opcode} with operand {op}")
                        print(self.get_status()) 
                    if len(expected_output) > 0:
                        return res
                elif opcode == 6:
                    self.bdv(op)
                elif opcode == 7:
                    self.cdv(op)
                if debug:
                    print(f"Doing opcode : {opcode} with operand {op}")
                    print(self.get_status()) 
                return False
    def run_all_program(self, p = None, debug=False, expected_output = []):
        if p != None:
            self.program = p
        if p == []:
            print(f"Error program is empty")
            exit(1)
        else:
            end = False
            while(not end):
                end = self.run_single_instruction(debug, expected_output)
            #print(f"Output is : {self.output}")
    def load_program(self, program):
        self.program = program
    def get_status(self):
        return f"A: {self.A}\nB: {self.B}\nC: {self.C}\nPC: {self.PC}\nout: {self.output}"
        
    def reset(self):
        self.A = self.initial_A
        self.B = self.initial_B
        self.C = self.initial_C
        self.PC = 0
        self.output = []

def parse(input_file_name):
    program = []
    with open(input_file_name) as file:
        # Register A 
        l = file.readline()
        A = int(re.findall(r"\d+", l)[0])
        # Register B
        l = file.readline()
        B = int(re.findall(r"\d+", l)[0])
        # Register C
        l = file.readline()
        C = int(re.findall(r"\d+", l)[0])
        # Empty line
        file.readline()
        # Program
        l = file.readline()
        program = [int(n) for n in re.findall(r"[0-8]", l)]
        c = Computer(A, B, C, 0)
        c.load_program(program)

    return c

def solve1(c):
    c.run_all_program(debug=True)
    answer1 = ""
    for i in c.output:
        answer1 += str(i)
        answer1 += ","
    return answer1[:-1]
def solve2(c):
    c.reset()
    c.run_all_program(debug=False)
    expected_res = c.program
    c.reset()
    for i in range(2147483648):
        c.reset()
        c.A = i
        c.run_all_program(expected_output=expected_res)
        print(f"Try with A = {i}, progress : {i/2147483648*100:.2f}%, last output = {c.output}" + " "*10, end="\r")
        if (c.output == expected_res):
            print()
            return i 


#Main 

input_file = "input.txt"
if len(sys.argv)>=2:
    if (sys.argv[1] == "-t"):
        test = 1
        if len(sys.argv) == 3:
            test = sys.argv[2]
        input_file = f"test{test}.txt"
c = parse(input_file)
answer1 = solve1(c)
print(f"Answer1 : {answer1}")
answer2 = solve2(c)
print(f"Answer2 : {answer2}")
