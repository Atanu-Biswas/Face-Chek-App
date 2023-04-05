import cv2
import numpy as np 
import face_recognition
import os
from PIL import Image
import shutil
from datetime import datetime
import requests
import uuid
cv2.VideoCapture(0)

lastEn = ''

def face_track():
    path = 'imageBasic'
    images = []
    className = []

    myList = os.listdir(path)
    #print(myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        className.append(os.path.splitext(cl)[0])
    print('classname =',className)

    def findEncoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
            
        return encodeList

    def markAttendence(name):
        
            
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        sheetData = {'name':name,'time':dtString}
        url = 'https://api.sheetmonkey.io/form/bGbUDMSNnWgnDRRwAS4WNw'
        requests.post(url, json = sheetData)

    

    encodeListKnown = findEncoding(images)
    print('encodelist = ',encodeListKnown)
    print('Encoding complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
   
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame  = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matcheIndex = np.argmin(faceDis)

       
            if matches[matcheIndex]:
                name = className[matcheIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                url = 'http://127.0.0.1:5000/add_user'
                response = requests.post(url, name=name)
            else:
                print("New face detected")
                
                unique_id = uuid.uuid4()
                uid=str(unique_id)
                
                img_name=uid+'.jpg'
                cv2.imwrite(img_name,img)
                url = 'http://127.0.0.1:5000/upload-image'
                files = {'image': open('img.jpg', 'rb')}
                print(files)
                response = requests.post(url, files=files)
            
                shutil.move(img_name, 'imageBasic/'+img_name)
                
            
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                return

        cv2.imshow('Webcam',img)
        cv2.waitKey(1)

while True:
    face_track()