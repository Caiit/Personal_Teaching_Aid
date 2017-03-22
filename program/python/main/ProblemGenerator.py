import copy
import math
import random
from numpy.random import choice

class ProblemGenerator:

    def __init__(self, student):
        self.student = student
        self.operators = copy.deepcopy(student.getOperators())
        self.calculateOperatorProportion()

    def calculateOperatorProportion(self):
        totalPercentage = 0
        for op in self.operators:
            correct, total = self.operators[op]['level']
            # Small percentage if all correct
            percentage = 0.000001 if total == 0 else (correct / float(total))
            self.operators[op]['level'] = self.operators[op]['level'] + [percentage]
            totalPercentage += 1 / percentage
        for op in self.operators:
            self.operators[op]['level'] = self.operators[op]['level'] + [((1 / self.operators[op]['level'][2]) / totalPercentage)]
        # self.operators[op]['level'] = self.operators[op]['level'] + [((1 / self.operators[op]['level']][2]) / totalPercentage)] for op in self.operators
        #.operators = {op: [self.operators[op]['level'][0], self.operators[op]['level'][1], self.operators[op]['level'][2], ((1 / self.operators[oper][2]) / totalPercentage)] for op in self.operators}

    def getCombinatedProblem(self, operator, problem, combinables):
        ops = []
        min_val = self.student.getMin(operator)
        max_val = self.student.getMax(operator)
        n = int(math.floor(self.operators[operator]['lastIncrement']/60))
        for i in range(n):
            operator = choice(combinables)
            c = random.randint(min_val, max_val)
            if operator == '/':
                problem = self.preventFractions(operator,problem,c)
            elif operator == '-':
                problem = self.preventNegatives(operator,problem,c)
            else:
                problem += operator + str(c)
            ops.append(operator)
        return problem, ops

    def preventFractions(self, operator, problem, b):
        min_val = self.student.getMin(operator)
        max_val = self.student.getMax(operator)
        if type(problem) is str:
            a = eval(problem)
        else:
            a = problem
        if a==0 and b!=0:
            problem = str(problem) + operator + str(b)
        elif b==0 and a!=0:
            problem = str(b) + operator + str(problem)
        elif a==0 and b==0:
            b = random.randint(1, max_val)
            problem = str(problem) + operator + str(b)
        elif a%b == 0:
            problem = str(problem) + operator + str(b)
        elif b%a == 0:
            problem = str(b) + operator + str(problem)
        else:
            while(a%b!=0):
                b = random.randint(1, max_val)
            problem = str(problem) + operator + str(b)
        return problem
        # if a==0 and b!=0:
        #     problem = str(a) + operator + str(b)
        # elif b==0 and a!=0:
        #     problem = str(b) + operator + str(a)
        # elif a==0 and b==0:
        #     b = random.randint(1, max_val)
        #     problem = str(a) + operator + str(b)
        # elif a%b == 0:
        #     problem = str(a) + operator + str(b)
        # elif b%a == 0:
        #     problem = str(b) + operator + str(a)
        # else:
        #     while(a%b!=0):
        #         b = random.randint(1, max_val)
        #     problem = str(a) + operator + str(b)
        # return problem

    def preventNegatives(self, operator, problem, b):
        if type(problem) is str:
            a = eval(problem)
            problem = '('+problem+')'
        else:
            a = problem
        if a > b:
            problem = str(problem) + operator + str(b)
        else:
            problem = str(b) + operator + str(problem)
        return problem

    def getProblems(self, n):
        pees = []
        problems = []
        combinables = self.student.getCombinables()
        i = 0
        while(i<n):
            # Get operator
            operator = choice(self.operators.keys(), p=[values['level'][3] for values in self.operators.values()])
            min_val = self.student.getMin(operator)
            max_val = self.student.getMax(operator)
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            # composes initial problem
            if operator == '/':
                problem = self.preventFractions(operator,a,b)
            elif operator == '-':
                problem = self.preventNegatives(operator,a,b)
            else:
                problem = str(a) + operator + str(b)
            ops = [operator]
            # combines operators if allowed
            if operator in combinables and len(combinables)>1:
                problem, operators = self.getCombinatedProblem(operator, problem, combinables)
                ops += operators
            # extends problem with same operator if allowed
            elif self.student.getCorrectness(operator)>0.8 and self.operators[operator]['lastIncrement']>=60:
                m = int(math.floor(self.operators[operator]['lastIncrement']/60))
                for j in range(m):
                    c = random.randint(min_val, max_val)
                    if operator == '/':
                        problem = self.preventFractions(operator,problem,c)
                    elif operator == '-':
                        problem = self.preventNegatives(operator,problem,c)
                    else:
                        problem += operator + str(c)
            if not problem in pees:
                pees.append(problem)
                problems.append((problem, ops))
                i += 1
        return problems
