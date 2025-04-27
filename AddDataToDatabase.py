import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"A:\sem3\pythonProject\college-attendance-53948-firebase-adminsdk-ipa91-e7e1c2d016.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://college-attendance-53948-default-rtdb.firebaseio.com/',

})

ref = db.reference('Students')

data = {
    "1":
        {
            "name": "Aryan",
            "Major": "Computer Vision",
            "Starting-Year": "2022",
            "Total Attendance": 10,
            "Standing": "G",
            "Year": 2,
            "Last_attendence_time": '22-01-2024 00:54:34'
        },
    "2":
        {
            "name": "Shashank_Yadav",
            "Major": "Teaching",
            "Starting-Year": "2016",
            "Total Attendance": 12,
            "Standing": "G",
            "Year": 7,
            "Last_attendence_time": '22-01-2024 00:53:22'
        },
}

for key,value in data.items():
    ref.child(key).set(value)