import random
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
        #print("A = A >> combo(op)")
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.A = res
        self.PC += 2
    def bxl(self, op):
        # Equivalent to B = B XOR op
        #print("B = B XOR op")
        self.B = self.B ^ op
        self.PC += 2
    def bst(self, op):
        # Equivalent to B = last 3 bits of combo(op)
        #print("B = last 3 bits of combo(op)")
        op = self.combo_value(op)
        self.B = op%8
        self.PC += 2
    def jnz(self, op):
        #print("Jump if A != 0")
        if self.A != 0:
            self.PC = op
        else :
            self.PC += 2
    def bxc(self, op):
        # Equivalent to B = B XOR C
        #print("B = B XOR C")
        self.B = self.B ^ self.C
        self.PC += 2
    def out(self, op, expected_output = []):
        # Equivalent to output += last 3 bits of combo(op)
        #print("output += last 3 bits of combo(op)")
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
        #print("B = A >> combo(op)")
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.B = res
        self.PC += 2
    def cdv(self, op):
        # Equivalent to C = A >> combo(op)
        #print("C = A >> combo(op)")
        op = self.combo_value(op)
        deno = 2**op
        res = self.A/deno
        res = int(str(res).split(".")[0])
        self.C = res
        self.PC += 2


    def run_single_instruction(self, debug = False, expected_output = [], one_loop = False):
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
                    if (one_loop):
                        return True
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
    def run_all_program(self, p = None, debug=False, expected_output = [], one_loop = False):
        if p != None:
            self.program = p
        if p == []:
            print(f"Error program is empty")
            exit(1)
        else:
            end = False
            while(not end):
                end = self.run_single_instruction(debug, expected_output, one_loop)
            #print(f"Output is : {self.output}")
        return self.output
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
    c.run_all_program(debug=False)
    answer1 = ""
    for i in c.output:
        answer1 += str(i)
        answer1 += ","
    return answer1[:-1]

# This overfit my input
def solve2(c, program = []):
    a = 1
    working_values = []
    #First loop of the program
    # Each iteration only care about 10 first bits of a
    for a in range(2**10):
        res, _ = quick_solver_one_loop(a)
        if res == program[0]:
            working_values.append(a)
    print(f"Loop 0 : {len(working_values)}")
    #for w in working_values:
        #print(f"{bin(w):>32}")
        #print(f"{quick_solver(w)}")
    # Next loops of the program
    for loop in range(1, len(program)):
        print()
        new_working_values = []
        for a in working_values:
            for i in range(8):
                new_a = (i << 7) | (a >> (3*loop))
                res, _ = quick_solver_one_loop(new_a)
                if res == program[loop]:
                    new_working_values.append(new_a << (3*loop) | (a & (2**(3*loop) -1)))
        working_values = new_working_values
        print(f"Loop {loop} : {len(working_values)}")
        #for w in working_values:
            #print(f"{bin(w):>32}")
            #print(f"{quick_solver(w)}")
    return min(working_values)

def solve2BruteForce(program):
    loop = len(program)
    working_values = []
    for a in range(2**(10+3*(loop))):
        print(f"Progress : {a/(2**(10+3*(loop)))*100:.2f}%", end="\r")
        res= quick_solver(a)
        if len(res) < loop:
            continue
        if res[0:loop+1] == program[0:loop+1]:
            working_values.append(a)
    print()
    print(f"Loop {loop} : {len(working_values)}")

    #for w in working_values:
        #print(f"{bin(w):>32}")
        #print(f"{quick_solver(w)}")
    
    return 0

            
def more_generic_solve2(c, program, prefix = 0, loop_number = 0):
    #print(f"Prefix {prefix}, loop_number {loop_number}")
    prefix = prefix << 3
    for i in range(8):
        c.reset()
        val =  prefix + i
        c.A = val
        res = c.run_all_program(one_loop = True)[0]
        #print(f"\t A = {bin(val)}, res = {res}, expected {program[len(program) - loop_number -1]}")
        if (res == program[len(program) - loop_number -1]):
            #print("\t", quick_solver(val))
            if (loop_number == len(program)):
                return c.A
            res2 = more_generic_solve2(c, program, val, loop_number + 1)
            if res2!=None:
                return res2
    return None
        
    

# this overfit my input
def quick_solver_one_loop(a):
    A = a
    A1 = A >> 3
    temp = A >> ((A & 7) ^ 5)
    B1 = ((A & 7) ^ 3) ^ temp
    res = B1 & 7
    
    A = A1
    return res, A

def quick_solver(a):
    output = []
    while a != 0:
        res, a = quick_solver_one_loop(a)
        output.append(res)
    return output
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
c.reset()
#answer2 = solve2(c, c.program)
#print(bin(answer2))
#answer2 = solve2BruteForce(c.program)
answer2 = more_generic_solve2(c, c.program)
print(f"Answer2 : {answer2}")
