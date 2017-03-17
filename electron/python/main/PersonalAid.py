import pickle
from Student import Student
from ProblemGenerator import ProblemGenerator
from faceRecognition import recognizeStudent
from faceRecognition import saveNewUser
from answerRecognition import getResponse, correct
from gtts import gTTS
import os
import zerorpc
from naoqi import ALProxy

class Api(object):

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.dbFile = os.path.join(fileDir, "StudentDatabase.pkl")
        self.loadDatabase()

        with open(os.path.join(fileDir, "wordToNumDict.pickle"), "rb") as handle:
            self.w2n = pickle.load(handle)


    def startProgram(self, robotIP):
        self.robotIP = str(robotIP)
        self.startRobot()
        self.recognizeStudent()


    def startRobot(self):
        if self.robotIP != "None":
            self.motionProxy = ALProxy("ALMotion", robotIP, 9559)
            self.motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)
            self.robotBehavior(True, "animations/Stand/Gestures/Hey_4",
                str("Hallo ik ben Noa"))


    def robotBehavior(self, parallel, behavior, text):
        manager = ALProxy("ALBehaviorManager", self.robotIP, 9559)

        if manager.isBehaviorInstalled(behavior):
            if not manager.isBehaviorRunning(behavior):
                if parallel:
                    manager.post.runBehavior(behavior)
                else:
                    manager.runBehavior(behavior)
                self.textToSpeech(text)


    def recognizeStudent(self):
        # self.studentID = recognizeStudent(self.robotIP)
        name = ""
        self.studentID = "Tirza-Soute-0"
        # self.studentID = "_unknown"
        if self.studentID is not "_unknown":
            self.getStudentInfo()
            name = self.student.getName()
        return name


    def addNewUser(self, firstName, lastName):
        self.studentID = saveNewUser(firstName, lastName)

        if not self.studentID in self.database:
            studentName = firstName + " " + lastName
            self.student = Student(studentName, self.studentID)
            self.database[self.studentID] = self.student
            self.storeDatabase()


    def getStudentInfo(self):
        self.student = self.database.get(self.studentID)
        print self.student.getMax('+')
        # TODO: deze vanuit ui krijgen
        n = 3
        self.getPersonalProblems(n)
        print self.student.getOperators()


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
        if len(self.problems) == 0:
            self.endProgram()
            return "None"
        self.problem = self.problems.pop(0)
        self.textToSpeech(self.problem[0])
        return self.problem[0]

    def endProgram(self):
        if (self.robotIP != "None"):
            self.robotBehavior(False,
                "animations/Stand/Emotions/Positive/Happy_3",
                str("Je bent klaar. Goed gedaan!"))
            self.motionProxy.stiffnessInterpolation("Body", 0.0, 1.0)
        self.updateRanges()
        self.initNewOperator()
        self.saveStudent()


    def getResponse(self):
        return getResponse()


    def checkAnswer(self, response):
        correctAnswer = eval(self.problem[0])
        isCorrect = correct(correctAnswer, response, self.w2n, 2)

        for operator in self.problem[1]:
            self.student.updateOperators(operator, isCorrect[0])
            self.student.updateIncrement(operator)

        return isCorrect


    def textToSpeech(self, text):
        text = self.replaceOperators(text)
        language = "nl"
        tts = gTTS(text=text, lang=language)
        tts.save("speech.mp3")
        if self.robotIP != "None":
            ttsProxy = ALProxy("ALTextToSpeech", self.robotIP, 9559)
            # ttsProxy.setLanguage("Dutch")
            ttsProxy.say(text)
        else:
            os.system("mpg123 speech.mp3")


    def replaceOperators(self, text):
        text = text.replace("-", "min")
        text = text.replace("+", "plus")
        text = text.replace("*", "keer")
        text = text.replace("/", "gedeeld door")
        return text


    def updateRanges(self):
        # TODO: niet elke keer updaten als geen vragen meer geweest zijn
        for op in self.student.getOperators():
            increment = self.student.getLastIncrement(op)
            if self.student.getCorrectness(op)>=0.8 and increment%20==0 and increment%40!=0 and increment %60 !=0:
                self.student.incrementMax(op, 10)


    def initNewOperator(self):
        operators = self.student.getOperators()
        if '/' in operators:
            return
        elif '*' in operators  and self.student.getCorrectness('*')>=0.8  and operators['*']['lastIncrement']>=40:
            if '/' not in operators:
                self.student.initialiseOperator('/')
        elif '-' in operators and self.student.getCorrectness('-')>=0.8  and operators['-']['lastIncrement']>=40:
            if '*' not in operators:
                self.student.initialiseOperator('*')
        elif self.student.getCorrectness('+')>=0.8  and operators['+']['lastIncrement']>=40:
            if '-' not in operators:
                self.student.initialiseOperator('-')


    def saveStudent(self):
        self.database[self.studentID] = self.student
        self.storeDatabase()


# if __name__== '__main__':
#     Api().startProgram("None")
#     # Api().recognizeStudent("146.50.60.31")
#     # Api().recognizeStudent("196.50.60.31")
#     # Api().moveRobot("animations/Stand/Gestures/Hey_4")
#     # Api().getNewProblem()
#     # Api().checkAnswer("0")
#     # checkAnswer(student, problems)
#     # saveStudent(student)


def main():
#     # api = Api()
#     # api.recognizeStudent("None")
#     # api.textToSpeech("hallo")
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
