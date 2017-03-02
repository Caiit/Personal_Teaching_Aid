class Student(object):

    def __init__(self, name, studentID):
        self.name = name
        self.studentID = studentID
        # Student start with only + as operator and range 0 - 10
        self.val_range = [0,10]
        self.operators = {'+': [0,0]}
        # self.operators = {'+': [0,0], '-': [0,0]}

    def getName(self):
        return self.name

    def getID(self):
        return self.studentID

    def getOperators(self):
        return self.operators

    def updateOperators(self, op, correct):
        if op in self.operators:
            self.operators[op][0] += correct
            self.operators[op][1] += 1
        else:
            self.operators[op] = [correct, 1]

    def getMin(self):
        return self.val_range[0]
    
    def getMax(self):
        return self.val_range[1]

    def setMin(self, min_val):
        self.val_range[0] = min_val

    def setMax(self, max_val):
        self.val_range[1] = max_val
