import pickle
from Student import Student
from ProblemGenerator import ProblemGenerator
from imageRecognition import recognizeStudent
import os
import zerorpc

class Api(object):
    def recognizeStudent(self):
        recognizedStudent, firstName, lastName = recognizeStudent()
        return recognizedStudent


    def echo(self, text):
        """echo any text"""
        return text

    # def loadDatabase():
    #     try:
    #         database = pickle.load(open("StudentDatabase.pkl", "rb" ))
    #     except EOFError:
    #         database = {}
    #     except IOError:
    #         database = {}
    #     return database
    #
    #
    # def storeDatabase(database):
    #     pickle.dump(database,open("StudentDatabase.pkl", "wb"))
    #
    #
    # def getStudentInfo(studentID, firstName, lastName):
    #     database = loadDatabase()
    #     if not studentID in database:
    #         studentName = firstName + " " + lastName
    #         database[studentID] = Student(studentName, studentID)
    #         storeDatabase(database)
    #     student = database[studentID]
    #     return student
    #
    #
    # def getPersonalProblems(student):
    #     pg = ProblemGenerator(student)
    #     n = int(raw_input('Enter number of problems to be solved: '))
    #     problems = pg.getProblems(n)
    #     return problems
    #
    #
    # def checkAnswers(student, problems):
    #     print(student.getOperators())
    #     for p in problems:
    #         problem = p[0]
    #         operator = p[1]
    #         print(problem)
    #         correctAnswer = eval(problem)
    #         givenAnswer = int(raw_input('What is your answer to this problem?: '))
    #         student.updateOperators(operator, givenAnswer==correctAnswer)
    #     print(student.getOperators())
    #
    #
    # def saveStudent(student):
    #     database = loadDatabase()
    #     studentID = student.getID()
    #     database[studentID] = student
    #     storeDatabase(database)



# if __name__== '__main__':
#     recognizedStudent, firstName, lastName = recognizeStudent()
#     student = getStudentInfo(recognizedStudent, firstName, lastName)
#     print "Hello, " + student.getName() + "!"
#     problems = getPersonalProblems(student)
#     checkAnswers(student, problems)
#     saveStudent(student)


def parse_port():
    return 4242


def main():
    # Api().recognizeStudent()
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(Api())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
