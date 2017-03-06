#!/usr/bin/env python2

import time
import argparse
import cv2
import os
import pickle
import collections

import numpy as np
import openface

from naoqi import ALProxy

np.set_printoptions(precision=2)

IMG_DIM = 96
WIDTH = 320
HEIGHT = 240
THRESHOLD = 0.65

FILEDIR = os.path.dirname(os.path.realpath(__file__))

def recognizeStudent(robotIP):
    ''' Recognize the student in front of the webcam. '''

    # Load the directories and neural network
    modelDir = os.path.join(FILEDIR, 'models')
    dlibModelDir = os.path.join(modelDir, 'dlib')
    openfaceModelDir = os.path.join(modelDir, 'openface')

    dlibFacePredictor = os.path.join(dlibModelDir,
        "shape_predictor_68_face_landmarks.dat")
    networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
    cuda = False

    align = openface.AlignDlib(dlibFacePredictor)
    net = openface.TorchNeuralNet(networkModel, imgDim=IMG_DIM, cuda=cuda)

    return identifyPerson(align, net, robotIP)


def identifyPerson(align, net, robotIP):
    ''' Take 10 pictures to identify the person. '''

    if robotIP != "None":
        # Get robot video device
        videoDevice = ALProxy('ALVideoDevice', robotIP, 9559)

        # subscribe top camera
        AL_kTopCamera = 0
        AL_kQVGA = 1            # 320x240
        AL_kBGRColorSpace = 13
        captureDevice = videoDevice.subscribeCamera(
            "nao", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    else:
        videoDevice = cv2.VideoCapture(0)
        videoDevice.set(3, WIDTH)
        videoDevice.set(4, HEIGHT)

    # Check if person is known
    picturesTaken = 0
    possiblePersons = collections.Counter()
    while (picturesTaken < 10):
        if robotIP != "None":
            frame = robotWebcam(videoDevice, captureDevice)
        else:
            ret, frame = videoDevice.read()
        persons, confidences = infer(frame, align, net)

        # If no person is detected, take an extra picture
        if len(persons) == 0:
            picturesTaken -= 1
            print "No person detected"

        # Add recognized person to list of possible persons
        for i, c in enumerate(confidences):
            # If the confidence is too low, classify the person as unknown
            if c <= THRESHOLD:
                persons[i] = "_unknown"
            possiblePersons[persons[i]] += 1

        cv2.imshow('', frame)
        # Quit the program on the press of key 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        picturesTaken += 1
    if robotIP != "None":
        videoDevice.unsubscribe(captureDevice)
    else:
        videoDevice.release()
    cv2.destroyAllWindows()

    person = possiblePersons.most_common(1)[0][0]
    return person


def robotWebcam(videoDevice, captureDevice):
    ''' Get an image from the robot. '''

    result = videoDevice.getImageRemote(captureDevice)

    if result == None:
        print 'Cannot capture.'
    elif result[6] == None:
        print 'No image data string.'
    else:
        # Create image
        values = map(ord, list(result[6]))
        image = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
        image = np.reshape(values, (HEIGHT, WIDTH,3)).astype('uint8')
    return image



def infer(img, align, net):
    ''' Classify people that were detected in the picture with a confidence. '''

    classifierModel = FILEDIR + "/generated-embeddings/classifier.pkl"

    with open(classifierModel, "r") as f:
        (le, clf) = pickle.load(f)

    reps = getRep(img, align, net)
    persons = []
    confidences = []

    for rep in reps:
        try:
            rep = rep.reshape(1, -1)
        except:
            print "No face detected"
            return None, None

        predictions = clf.predict_proba(rep).ravel()
        maxI = np.argmax(predictions)
        persons.append(le.inverse_transform(maxI))
        confidences.append(predictions[maxI])

    return persons, confidences


def getRep(bgrImg, align, net):
    ''' Retrieve the representation of a face.  '''

    if bgrImg is None:
        raise Exception("Unable to load image/frame")

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    bb = align.getAllFaceBoundingBoxes(rgbImg)

    if bb is None:
        return None

    alignedFaces = []
    for box in bb:
        alignedFaces.append(
            align.align(
                IMG_DIM,
                rgbImg,
                box,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        raise Exception("Unable to align the frame")

    reps = []
    for alignedFace in alignedFaces:
        reps.append(net.forward(alignedFace))

    return reps


def saveNewUser(fName, lName):
    ''' Save a new person to the training images. '''

    # Create folder with name
    trainDir = os.path.join(FILEDIR, 'training-images')
    directory = os.path.join(trainDir, fName + "-" + lName)
    n = 0

    if not os.path.exists(directory + "-0"):
        os.makedirs(directory + "-0")
    else:
        n = max([int(d.split("-")[2]) for d in os.listdir(trainDir)
            if d.startswith(fName + "-" + lName)] + [0]) + 1
        os.makedirs(directory + "-" + str(n))

    takePictures(n, directory)

    return fName + "-" + lName + "-" + str(n)


def takePictures(n, directory):
    ''' Take pictures of the new person to save as training images. '''

    images = []
    imagesTaken = 0

    while imagesTaken < 10:
        camera = cv2.VideoCapture(0)
        s, img = camera.read()
        cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

        if s:
            cv2.imshow("image", img)
            key = cv2.waitKey(0) & 0xFF

            if key == ord("y"):
                cv2.imwrite(directory + "-" + str(n) + "/image" +
                str(imagesTaken) + ".png", img)
                imagesTaken += 1
            camera.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    recognizeStudent("10.42.0.180")
