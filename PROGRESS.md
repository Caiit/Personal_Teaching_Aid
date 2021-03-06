## 06-02-2017
The idea is to develop a program where children can practice basic math problems. The program keeps track of the child's strengths and weaknesses. According to these stats, the program continues offering questions the child has the most problems with. 

A Nao will be used in combination with the program. The Nao should face the child and use facial recognition to recognize the child. This is done in order to personalise the data. The Nao will ask the child the current question out loud, and the child is supposed to answer out loud. The child's voice also has to be recognized by the Nao. For example, if another child answers, the answer should not be accepted.

If the child's answer is not recognized, the child has to type in the answer on the computer. 

Main features:
 - facial recognition
 - text-to-speech
 - speech recognition
 - voice/speaker recognition
 - API for math questions


## 07-02-2017
Looked into face recognition: 
  - https://cmusatyalab.github.io/openface/: openface would be perfect, only we didn't manage to get it working locally. The docker on their container did work though.
  - http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html: using opencv, did work, but not that good.
  
Looked into speech recognition:
  - ~~Sphinx speech recognition~~
  - Python SpeechRecognition: https://pypi.python.org/pypi/SpeechRecognition/
  
## 09-02-2017
Managed to get openface working locally: followed the setup by hand from http://cmusatyalab.github.io/openface/setup/

Created our own little dataset and script to test openfaces with a webcam. 

Managed to implement speech recognition. Still need to make sure that we get the numeric version of a number instead of the word.

Program idea:
A child is seated in front of the webcam and photos are taken to identify who it is. If the confidence is high enough, the child is identified and the lesson begins. If the confidence is too low for a certain amount of photos, the images of the child are added to the database as training data (if training is fast enough, the program can say it is trying to recognise the child and starting the rest of the program -> otherwise, the program has to be trained the next time). 

Datastructure:
- Child types their name (first and last name) into the program after the pictures are added. Child is identified by the name of the folder (their first and last name).
- Link child to their maths level

## 13-02-2017
Child sits in front of the webcam and 10 photos are taken. The face recognition identifies the child and adds a counter to that classified person. The person that is classified the most out of ten times is taken as identified person. For example, out of the ten images, the face recognition recognizes the child 7 times as "person1" and does not know (threshold is too low) the other 3 times: {"person1": 7, "\_unknown":3}. The child is now identifies as person1. If the child is unknown, the name is asked and the images are saved to the new person. 

## 16-02-2017
found watson: https://www.ibm.com/watson/developercloud/doc/speech-to-text/
might be interesting for recognising who's speaking.

Finished project proposal.

## 20-02-2017
Error with Speech Recognition part on ubuntu, on windows it works fine.

>ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear </br>
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe </br>
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side </br>
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map </br>
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map </br>
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map </br>
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map </br>

Fixed first three errors with: http://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time

It did work (it weren't errors, but warnings?), so we now only supress the errors and didn't use the first fix.

## 22-02-2017
Looked into text to speech for dutch: https://pypi.python.org/pypi/gTTS

To install gtts:
> sudo pip install gtts

To install mpg123:
> sudo apt-get install mpg123


## 23-02-2017
Creating an GUI with electron (http://electron.atom.io/)

things to install for this part:

nodejs: 
>curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - </br>
sudo apt-get install -y nodejs </br>

npm: </br>
>sudo apt-get install npm </br>

zerorpc: </br>
>sudo pip install zerorpc </br>

faceRecognition is started when clicking on the start button in the GUI.

Integrated image recognition in main program. 
Taking pictures and check if they are correct instead of using the images that were used for recogniting the person.

Integrated speech recognition in main program.
Speech module works faster if you connect an external microphone.

## 01-03-2017
The camera caption did not close when finished with face recognition. However, when using a different OpenCV version it did work. We now use version 3.2.0.

We worked on the UI. You can now add yourself if the program does not recognize you. If it does, a random problem is shown.

We started working on the first draft report.

## 02-03-2017
Integrated speech recognition into the main program (UI) and worked on UI layout. 

Worked on problem generator. The operators are now randomly chosen based on their probability distribution. An operator that has a high correctness, is asked less often than an operator that has a low correctness.

## 06-03-2017
Set a 6 second limit on speech recognition listening time to fix electron's TimeOutError. Added a text input field in case the answer is wrong or the program did not understand what was said. 

Still need to implement: a listening gif that indicates when the program is listening, a picture that the user can click if they want to use the Nao instead of a computer: https://community.ald.softbankrobotics.com/en/forum/impossible-subscribe-alaudiodevice-2563

Got the Dutch Text To Speech working on the nao and camera input from the robot. The microphone input seems harder then expected. We need to be able to get the buffer of the microphone input or transfer .wav files from the robot to the program.

## 10-03-2017
Added the listening gif and fixed the style of the robot/program indication images, also linked this to the program so that the right version of the program starts when an image is clicked.

## 13-03-2017
Implemented an input field where the user can give the robot's IP address.

## 14-03-2017
Hardcoded the operators so that they are pronounced correctly: e.g. "-" pronounced as "min" instead of "tot". Changed answerRecognition.py so that the WaitTimeOutError is caught. Added robot behaviors: the user is greeted when the program starts and at the end of the session, the user is given feedback -> still needs to be connected with the new problem generator so that it gives feedback corresponding to how well the user performed.

Implement:
- Robot says "Hello", "I don't know you yet", etc.
- English language option?
- Nao gives the student feedback at the end of the session based on the student's level update: "Well done!" \*Nao cheers\* or "I bet it will go better next time"
- When will the program train on new data?
- After adding a new user, start the program

## 17-03-2017
Incorporated the latest ProblemGenerator into Electron so the basic program fully works now. Also prevented the possibility of getting the same problems in a set of questions.

## 20-03-2017
Tested facial and speech recognition for the evaluation. Implemented the feedback functionality, the program now trains at the end if a new user was added and the rest of the program now starts after adding a new user.

Implement:
- Robot says "I don't know you yet" 
- English language option?

## 22-03-2017
Cleaned Git and finished up the program. There were a lot of errors after the last commit/push and they were all fixed. The entire program works as expected now.
