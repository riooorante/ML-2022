import os
import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("pilajara-d8d3f-firebase-adminsdk-qvb91-117221a516.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "pilajara-d8d3f.appspot.com",
    "databaseURL": "https://pilajara-d8d3f-default-rtdb.firebaseio.com/"
})
bucket = storage.bucket()

Webcam = cv2.VideoCapture(1)
Webcam.set(3, 640)
Webcam.set(3, 480)

file = open("EncodeFile.p", "rb")
EncodeAndLabel = pickle.load(file)
X, label = EncodeAndLabel
file.close()

TipeMode = 0
counter = 0
picture = []

backg = cv2.imread("Recourses/back.png")

modepath = 'Recourses/SCAN'
listmode = os.listdir(modepath)
imgModelist = []
for path in listmode:
    imgModelist.append(cv2.imread(os.path.join(modepath, path)))

while True:
    sukses, img = Webcam.read()
    smallIMG = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    smallIMG = cv2.cvtColor(smallIMG, cv2.COLOR_BGR2RGB)

    backg[150:150 + 480, 155:155 + 640] = img
    backg[0:0 + 788, 957:957 + 443] = imgModelist[TipeMode]

    facecurFrame = face_recognition.face_locations(smallIMG)
    encodeCurFrame = face_recognition.face_encodings(smallIMG, facecurFrame)

    if facecurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, facecurFrame):
            match = face_recognition.compare_faces(X, encodeFace)
            facedis = face_recognition.face_distance(X, encodeFace)

            matchIndex = np.argmin(facedis)
            id = label[matchIndex]

            if match[matchIndex]:
                print("Wajah Diketahui : ", label[matchIndex])
            if counter == 0:
                counter = 1
                TipeMode = 1

        if counter != 0:
            if counter == 1:
                profileInfo = db.reference(f"Siswa/{id}").get()
                blob = bucket.get_blob(f'{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                picture = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)


                tanggal = datetime.strptime(profileInfo['lastScan'], "%Y-%m-%d %H:%M:%S")
                hitungwaktu = (datetime.now()-tanggal).total_seconds()


                if hitungwaktu>30:
                    ref = db.reference(f"Siswa/{id}")
                    profileInfo['kehadiran'] += 1
                    ref.child('kehadiran').set(profileInfo['kehadiran'])
                    ref.child('lastScan').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    TipeMode = 2
                    counter = 0
                    backg[0:0 + 788, 957:957 + 443] = imgModelist[TipeMode]

            if TipeMode != 2:

                if 10 < counter <= 20:
                    TipeMode = 2

                backg[0:0 + 788, 957:957 + 443] = imgModelist[TipeMode]

                if counter <= 10:
                    (w, r), _ = cv2.getTextSize(profileInfo['nama'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (443 - w) // 2
                    cv2.putText(backg, str(profileInfo['nama']), (955 + offset, 315), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(backg, str(profileInfo['ID']), (1115, 425), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(backg, str(profileInfo['angkatan']), (1115, 520), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                                1)
                    cv2.putText(backg, str(profileInfo['jurusan']), (1115, 608), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                                1)
                    cv2.putText(backg, str(profileInfo['kehadiran']), (1115, 698), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                                1)

                    backg[50:50 + 223, 1070:1070 + 216] = picture
            counter += 1
            if counter>=20:
                counter=0
                TipeMode=0
                profileInfo=[]
                picture=[]
                backg[0:0 + 788, 957:957 + 443] = imgModelist[TipeMode]
        else:
            TipeMode = 0
            counter = 0

    cv2.imshow("Pengenalan Wajah", backg)
    cv2.waitKey(1)

Webcam.release()
