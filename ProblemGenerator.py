import random

class ProblemGenerator:

    def __init__(self, ops, val_range, n):
        self.operators = {key: ops[key][0]/float(ops[key][1]) for key in ops}
        self.min_val = val_range[0]
        self.max_val = val_range[1]
        self.n = n

    def getProblems(self, ops, min_val, max_val, n):
        problems = []
        for i in range(self.n):
            operator = random.choice(self.ops.keys())
            a = random.randint(self.min_val, self.max_val)
            b = random.randint(self.min_val, self.max_val)
            problem = str(a) + operator + str(b)
            problems.append(problem)
        return problems
