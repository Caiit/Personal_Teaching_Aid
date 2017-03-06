import pickle
from Student import Student
from ProblemGenerator import ProblemGenerator
from imageRecognition import recognizeStudent
from imageRecognition import saveNewUser
from answerRecognition import getResponse, correct
from gtts import gTTS
import os
import zerorpc

class Api(object):

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.dbFile = os.path.join(fileDir, "StudentDatabase.pkl")
        self.loadDatabase()

        with open(os.path.join(fileDir, "wordToNumDict.pickle"), "rb") as handle:
            self.w2n = pickle.load(handle)


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
        n = 5
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
        self.problem = self.problems.pop(0)[0]
        self.textToSpeech(self.problem)
        return self.problem


    def getResponse(self):
        return getResponse()


    def checkAnswer(self, response):
        if not self.problems:
            return False, "None"
        # TODO: Update operators?
        correctAnswer = eval(self.problem)
        return correct(correctAnswer, response, self.w2n, 2)


    def textToSpeech(self, string):
        language = "nl"
        tts = gTTS(text=string, lang=language)
        tts.save("speech.mp3")
        os.system("mpg123 speech.mp3")


    # def checkAnswers(student, problems):
    #     with open('wordToNumDict.pickle', 'rb') as handle:
    #         w2n = pickle.load(handle)
    #     for p in problems:
    #         problem = p[0]
    #         operator = p[1]
    #         print(problem)
    #         correctAnswer = eval(problem)
    #         givenAnswer = AnswerRecognition.correct(correctAnswer, w2n, 2)
    #         student.updateOperators(operator, givenAnswer)
    #     print(student.getOperators())
    #
    #
    # def saveStudent(student):
    #     database = loadDatabase()
    #     studentID = student.getID()
    #     database[studentID] = student
    #     storeDatabase(database)


# if __name__== '__main__':
#     Api().recognizeStudent()
    # checkAnswer(student, problems)
    # saveStudent(student)


def main():
#     # api = Api()
#     # api.getStudentInfo("tirza-soutehakjsdhasdj-0")
#     # for i in range(2):
#     #     problem = api.getNewProblem()
#     #     if problem:
#     #         print api.checkAnswer(eval(problem))
#     #     print problem
    addr = 'tcp://127.0.0.1:' + str(3006)
    s = zerorpc.Server(Api())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
