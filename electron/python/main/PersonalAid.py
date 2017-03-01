import pickle
from Student import Student
from ProblemGenerator import ProblemGenerator
from imageRecognition import recognizeStudent
from imageRecognition import saveNewUser
import os
import zerorpc

class Api(object):

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.dbFile = os.path.join(fileDir, "StudentDatabase.pkl")
        self.loadDatabase()


    def recognizeStudent(self):
        studentID = recognizeStudent()
        name = ""
        if studentID is not "_unknown":
            self.getStudentInfo(studentID)
            name = self.student.getName()
        return name


    def addNewUser(self, firstName, lastName):
        studentID = saveNewUser(firstName, lastName)

        if not studentID in self.database:
            studentName = firstName + " " + lastName
            self.student = Student(studentName, studentID)
            self.database[studentID] = self.student
            self.storeDatabase()


    def getStudentInfo(self, studentID):
        self.student = self.database.get(studentID)
        # TODO: deze vanuit ui krijgen
        n = 1
        self.getPersonalProblems(n)


    def echo(self, text):
        """echo any text"""
        return text


    def loadDatabase(self):
        try:
            self.database = pickle.load(open(self.dbFile, "rb"))
        except EOFError:
            self.database = {}
        except IOError:
            self.database = {}


    def storeDatabase(self):
        pickle.dump(self.database, open(self.dbFile, "wb"))


    def getPersonalProblems(self, n):
        pg = ProblemGenerator(self.student)
        self.problems = pg.getProblems(n)


    def getNewProblem(self):
        if not self.problems:
            return "None"
        return self.problems[0][0]


    def checkAnswer(self, answer):
        if not self.problems:
            return None
        return eval(self.problems.pop()[0]) == int(answer)

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


def main():
    # api = Api()
    # api.getStudentInfo("tirza-soutehakjsdhasdj-0")
    # for i in range(2):
    #     problem = api.getNewProblem()
    #     if problem:
    #         print api.checkAnswer(eval(problem))

    addr = 'tcp://127.0.0.1:' + str(3006)
    s = zerorpc.Server(Api())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
