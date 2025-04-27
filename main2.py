import cv2
import pickle
import cvzone
import os
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate(r"A:\sem3\pythonProject\college-attendance-53948-firebase-adminsdk-ipa91-e7e1c2d016.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://college-attendance-53948-default-rtdb.firebaseio.com/',
    'storageBucket': 'college-attendance-53948.appspot.com'
})

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread(r'A:\sem3\pythonProject\pythonProject\Resources\background.png')

# Importing the mode images into a list
folderModePath = r'A:\sem3\pythonProject\pythonProject\Resources\Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

bucket = storage.bucket()

# Load the encoding file
print("Loading Encoded File....")
file = open(r'A:\sem3\pythonProject\EncodedFile2.p', 'rb')
encodeListknownwithids = pickle.load(file)
file.close()
encodelistknown, studentIds = encodeListknownwithids
# print(studentIds)
print("Encoded File Loaded...")

File_name = r'A:\sem3\pythonProject\Student_id.txt'

if os.path.exists(File_name):
    with open(File_name, 'r') as f:
        student_id = int(f.read().strip())
else:
    print("Error")
    # Counter = 1

modeType = 0
counter = 0
ids = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodelistknown, encodeFace)
            faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                ids = studentIds[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1
            if not matches[matchIndex]:
                cv2.putText(imgBackground,"Not RECOGNISED", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.imshow("Face Attendence", imgBackground)
                cv2.waitKey(0)

                name = input("Enter Student's Name")
                major = input("Enter Student's major")
                starting_year = input("Enter student's Starting Year")
                total_attendence = int(input("Enter student's Total Attendence"))
                standing = input("Enter Student's Standing")
                year = int(input("Enter Student's Year"))
                last_attendance_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                new_student_ref = db.reference('Students').child(str(student_id))

                image_file_path = fr'A:\sem3\pythonProject\Images2/{student_id}.png'
                cv2.imwrite(image_file_path, img)
                student_id += 1

                blob = bucket.blob(image_file_path)
                blob.upload_from_filename(image_file_path)

                new_student_ref.set({
                    'name': name,
                    'Major': major,
                    'Starting-Year': starting_year,
                    'Total Attendance': total_attendence,
                    'Standing': standing,
                    'Year': year,
                    'Last_attendence_time': last_attendance_time
                })
                with open(File_name, 'w') as f:
                    f.write(str(student_id))
                folderPath = r'A:\sem3\pythonProject\pythonProject\Images2'
                PathList = os.listdir(folderPath)
                imageList = []
                studentIds = []
                for path in PathList:
                    imageList.append(cv2.imread(os.path.join(folderPath, path)))
                    print(os.path.splitext(path)[0])  # by using splittext we can use our ids to recognise the
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
                    encodelist = []
                    for img in imagesList:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)[0]
                        encodelist.append(encode)

                    return encodelist


                encodelistknown = findencoding(imageList)
                print(encodelistknown)
                print("Encoding complete")
                encodelistknownwithids = [encodelistknown, studentIds]
                #
                file = open("EncodedFile2.p", 'wb')
                pickle.dump(encodelistknownwithids, file)
                file.close()
                print("File saved")
                #
                PathList = os.listdir(folderPath)
                print(PathList)

    

    if counter !=0:

        if counter == 1:
            studentinfo = db.reference(f'Students/{ids}').get()
            print(studentinfo)
            blob = bucket.get_blob(f'Images2/{ids}.png')
            print("IDs:", ids)
            print("Blob:", blob)
            if blob is not None:
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            else:
                print(f"Blob for {ids} not found in the storage bucket.")

            # array = np.frombuffer(blob.download_as_string(), np.uint8)
            # imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            # update data of attendance
            datetimeobject = datetime.strptime(studentinfo['Last_attendence_time'],
                                              '%d-%m-%Y %H:%M:%S')
            difference=(datetime.now()-datetimeobject).total_seconds()

            if difference>30:
                ref = db.reference(f'Students/{ids}')
                studentinfo['Total Attendance'] +=1
                ref.child('Total Attendance').set(studentinfo['Total Attendance'])
                ref.child('Last_attendence_time').set(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if modeType != 3:

            if 10<counter<20:
                modeType=2

            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if counter<=10:

                cv2.putText(imgBackground, str(studentinfo['Total Attendance']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentinfo['Major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentinfo['Standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentinfo['Year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentinfo['Starting-Year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(studentinfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imgBackground, str(studentinfo['name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                imgStudent = cv2.resize(imgStudent, (216, 216))

                imgBackground[175:175+216, 909:909+216] = imgStudent

        counter += 1

        if counter>=20:
            counter = 0
            modeType = 0
            imgStudent = []
            studentinfo = []
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
       modeType = 0
       counter=0

    cv2.imshow("Face Attendance", imgBackground)

    key = cv2.waitKey(1)
    if key == ord('q'):  # 'q' to quit
       cv2.destroyAllWindows()

