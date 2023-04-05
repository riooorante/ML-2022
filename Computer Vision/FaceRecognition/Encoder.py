import os

import face_recognition
import cv2
import pickle

pathlist = os.listdir("Images")
X = []
label = []

for path in pathlist:
    X.append(cv2.imread(os.path.join("Images", path)))
    label.append(os.path.splitext(path)[0])

def endcode(imglist):
    encodedList = []
    for img in imglist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList

endcoded = endcode(X)
endcodeandLabel = [endcoded, label]

file = open("EncodeFile.p","wb")
pickle.dump(endcodeandLabel, file)
file.close()