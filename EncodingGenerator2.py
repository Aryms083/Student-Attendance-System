import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate(r"A:\sem3\pythonProject\college-attendance-53948-firebase-adminsdk-ipa91-e7e1c2d016.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://college-attendance-53948-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://college-attendance-53948.appspot.com'
})


# Importing student images
folderPath = r'A:\sem3\pythonProject\Images2'
PathList = os.listdir(folderPath)
print(PathList)
imageList = []
studentIds=[]
for path in PathList:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    print(os.path.splitext(path)[0]) #by using splittext we can use our ids to recognise the
    studentIds.append(os.path.splitext(path)[0])

    filename = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    try:
        blob.upload_from_filename(filename)
    except Exception as e:
        print(f"Error uploading {filename} to Firebase Storage: {e}")

print(len(imageList))


def findencoding(imagesList):
    encodelist=[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist


encodelistknown = findencoding(imageList)
print(encodelistknown)
print("Encoding complete")
encodelistknownwithids = [encodelistknown,studentIds]

file= open("EncodedFile2.p",'wb')
pickle.dump(encodelistknownwithids, file)
file.close()
print("File saved")