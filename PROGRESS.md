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
  - Sphinx speech recognition
  
## 09-02-2017
Managed to get openface working locally. 

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
