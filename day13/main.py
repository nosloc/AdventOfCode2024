import sys
import re

class Equation():
    def __init__(self, a1, b1, c1, a2, b2, c2):
        self.a1 = a1
        self.b1 = b1
        self.c1 = c1
        self.a2 = a2
        self.c2 = c2
        self.b2 = b2
    def __repr__(self):
        return f"Equation: {self.a1}A + {self.b1}B = {self.c1} and {self.a2}A + {self.b2}B = {self.c2}"

    def solve(self):    
        coef_det = self.a1*self.b2-self.a2*self.b1
        det_a = self.c1*self.b2-self.c2*self.b1
        det_b = self.a1*self.c2-self.a2*self.c1
        if (coef_det != 0):
            if (det_a%coef_det == 0 and det_b%coef_det==0):
                a, b = det_a//coef_det, det_b//coef_det
                return a, b
        else :
            if (det_a ==0 and det_b ==0 and self.c1%self.b1==0):
                return 0, self.c1//self.b1 if self.b1 != 0 else 0
            else :
                return None

def parse(inputName):
    buttonAFormat = r"Button A: X\+(\d+), Y\+(\d+)"
    buttonBFormat = r"Button B: X\+(\d+), Y\+(\d+)"
    resFormat = r"Prize: X=(\d+), Y=(\d+)"
    equations = []
    with open(inputName) as file:
        lines = list(map(lambda s : s.replace("\n", "").strip(), file.readlines()))
        i = 0
        curr_equation = Equation(0,0,0,0,0,0)
        for s in lines:
            if i % 4 ==0:
                for e in re.finditer(buttonAFormat, s):
                    curr_equation.a1 = int(e.group(1))
                    curr_equation.a2 = int(e.group(2))
                    break
            elif i % 4 ==1:
                for e in re.finditer(buttonBFormat, s):
                    curr_equation.b1 = int(e.group(1))
                    curr_equation.b2 = int(e.group(2))
                    break
            elif i % 4 ==2:
                for e in re.finditer(resFormat, s):
                    curr_equation.c1 = int(e.group(1))
                    curr_equation.c2 = int(e.group(2))
                    equations.append(curr_equation)
                    curr_equation = Equation(0,0,0,0,0,0)
                    break
            i += 1
        return equations
            
def solve1(equations):
    counter = 0
    for e in equations :
        res = e.solve()
        if res!=None:
            a, b = res
            if (a <= 100 and b<=100 and a>=0 and b>=0):
                counter += a*3 + b
    return counter

def solve2(equations):
    counter = 0
    for e in equations :
        e.c1 = 10000000000000 + e.c1
        e.c2 = 10000000000000 + e.c2
        res = e.solve()
        if res!=None:
            a, b = res
            if (a>=0 and b>=0):
                counter += a*3 + b
    return counter


# Main 
inputFile = "input.txt"
if "-t" in sys.argv:
    inputFile = "test.txt"
equations = parse(inputFile)
answer1 = solve1(equations)
print(f"Answer1: {answer1}")
answer2 = solve2(equations)
print(f"Answer2: {answer2}")