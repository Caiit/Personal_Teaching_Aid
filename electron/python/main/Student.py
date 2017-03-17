class Student(object):

    def __init__(self, name, studentID):
        self.name = name
        self.studentID = studentID
        # Student start with only + as operator and range 0 - 10
        self.operators = {'+': {'level': [0,0], 'range':[0,10], 'lastIncrement':0}}
        # self.operators = {'+': [0,0], '-': [0,0]}

    def getName(self):
        return self.name

    def getID(self):
        return self.studentID

    def initialiseOperator(self, op):
        self.operators[op] = {'level': [0,0], 'range':[0,10], 'lastIncrement':0}

    def getOperators(self):
        return self.operators

    def updateOperators(self, op, correct):
        if op in self.operators:
            self.operators[op]['level'][0] += correct
            self.operators[op]['level'][1] += 1
        else:
            self.operators[op]['level'] = [correct, 1]

    def getCorrectness(self, op):
        correct = self.operators[op]['level'][0]
        total = self.operators[op]['level'][1]
        if total == 0:
            return 0
        else:
            return correct/float(total)

    def getCombinables(self):
        combinables = []
        for op in self.operators:
            if self.getCorrectness(op)>=0.8 and self.operators[op]['lastIncrement']>=80:
                combinables.append(op)
        if len(combinables) > 1:
            for op in self.operators:
                self.setMax(op, 10)
        return combinables

    def getLastIncrement(self,op):
        return self.operators[op]['lastIncrement']

    def updateIncrement(self, op):
        self.operators[op]['lastIncrement'] += 1

    def resetIncrement(self,op):
        self.operators[op]['lastIncrement'] = 0

    def getMin(self, op):
        return self.operators[op]['range'][0]

    def getMax(self, op):
        return self.operators[op]['range'][1]

    def setMin(self, op, min_val):
        self.operators[op]['range'][0] = min_val

    def setMax(self, op, max_val):
        self.operators[op]['range'][1]  = max_val

    def incrementMin(self, op, i):
        self.setMin(op, self.getMin(op)+i)

    def incrementMax(self, op, i):
        self.setMax(op, self.getMax(op)+i)
