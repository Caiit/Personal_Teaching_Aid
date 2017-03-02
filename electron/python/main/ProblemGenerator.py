import random

class ProblemGenerator:

    def __init__(self, student):
        ops = student.getOperators()
        self.operators = {key:0 if ops[key][0]==0
            else ops[key][0]/float(ops[key][1]) for key in ops}
        self.min_val = student.getMin()
        self.max_val = student.getMax()

    def getProblems(self, n):
        problems = []
        for i in range(n):
            operator = random.choice(self.operators.keys())
            a = random.randint(self.min_val, self.max_val)
            b = random.randint(self.min_val, self.max_val)
            if a > b:
                problem = str(a) + operator + str(b)
            else:
                problem = str(b) + operator + str(a)
            problems.append((problem, operator))
        return problems
