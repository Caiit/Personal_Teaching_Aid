import random
from numpy.random import choice

class ProblemGenerator:

    def __init__(self, student):
        self.operators = student.getOperators()
        # TODO: check if necessary here
        # self.operators = {key:0 if ops[key][0]==0 else ops[key][0] / float(ops[key][1]) for key in ops}
        self.min_val = student.getMin()
        self.max_val = student.getMax()
        self.calculateOperatorProportion()

    def calculateOperatorProportion(self):
        ''' Calculate the proportion of each operator. '''
        self.operators = {'+': [1, 5], '-': [1, 4], '*': [6, 6]}
        totalPercentage = 0
        for oper in self.operators:
            correct, total = self.operators[oper]
            # Small percentage if all correct
            percentage = 0.000001 if total == 0 else (correct / float(total))
            self.operators[oper] = self.operators[oper] + [percentage]
            totalPercentage += 1 / percentage
        # operatorProportion = 1 - (operatorPercentage / totalOperatorPercentage)
        self.operators = {oper: [self.operators[oper][0], self.operators[oper][1], self.operators[oper][2], ((1 / self.operators[oper][2]) / totalPercentage)] for oper in self.operators}
        print self.operators

    def getProblems(self, n):
        problems = []
        for i in range(n):
            # Get operator
            operator = choice(self.operators.keys(), p=[values[3] for values in self.operators.values()])
            a = random.randint(self.min_val, self.max_val)
            b = random.randint(self.min_val, self.max_val)
            problem = str(a) + operator + str(b)
            problems.append((problem, operator))
        return problems
