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


## 09-02-2017
Looked into face recognition: 
  - https://cmusatyalab.github.io/openface/: openface would be perfect, only we didn't manage to get it working locally. The docker on their container did work though.
  - http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html: using opencv, did work, but not that good.
  
Looked into speech recognition:
  - Sphinx speech recognition
  
