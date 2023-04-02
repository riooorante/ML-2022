import os
import firebase_admin
from firebase_admin import credentials
from  firebase_admin import db
from firebase_admin import storage



cred = credentials.Certificate("pilajara-d8d3f-firebase-adminsdk-qvb91-117221a516.json")
firebase_admin.initialize_app(cred, {
    "storageBucket":"pilajara-d8d3f.appspot.com",
    "databaseURL":"https://pilajara-d8d3f-default-rtdb.firebaseio.com/"
})

ref = db.reference('Siswa')

data = {
    "H075":
        {
            "nama":"Mario Valerian",
            "ID":"C011221075",
            "jurusan":"Kedokteran",
            "angkatan":2022,
            "kehadiran":0,
            "lastScan":"2022-10-08 00:54:35"
        },

    "H089": {
        "nama": "Kelvin",
        "ID": "H0712210789",
        "jurusan": "Sistem Informasi",
        "angkatan": 2022,
        "kehadiran": 0,
        "lastScan": "2022-10-08 00:54:35"
    },
    "H084": {
        "nama": "Fail Fudol",
        "ID": "H0712210789",
        "jurusan": "Sistem Informasi",
        "angkatan": 2022,
        "kehadiran": 0,
        "lastScan": "2022-10-08 00:54:35"},
    "H080": {
        "nama": "Adnan Nano",
        "ID": "H0712210789",
        "jurusan": "Sistem Informasi",
        "angkatan": 2022,
        "kehadiran": 0,
        "lastScan": "2022-10-08 00:54:35"}
}



for key, value in data.items():
    ref.child(key).set(value)

profile = os.listdir("Profile")
for photo in profile:
    bucket = storage.bucket()
    blob = bucket.blob(photo)
    blob.upload_from_filename(f"Profile/{photo}")

print("Aman")