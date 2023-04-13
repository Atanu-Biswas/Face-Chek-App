import cv2
import numpy as np 
import face_recognition
import os
import qrcode
from PIL import Image
from PIL import Image

import shutil
from datetime import datetime
import requests
import uuid
import requests
import uuid
import base64
from urllib.parse import quote
import time

cv2.VideoCapture(0)

lastEn=''

path = 'imageBasic'
images = []
className = []
frameCount = 0

myList = os.listdir(path)
    #print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

print(images)

def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            encodeList.append(encodings[0])
    return encodeList

encodeListKnown = findEncoding(images)

def face_track():
    

    def entry(uid):
        global lastEn
        lastEn=str(uid)
        print(lastEn,"52")
        
        url = 'http://127.0.0.1:5000/entry'
        payload = {'user_id':uid}

        response = requests.post(url, data=payload)
        
        print(response)

        

    
    

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
   
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
                user_id = className[matcheIndex]
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,user_id,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                print(lastEn, "92")
                print(str(user_id),"93")
                if lastEn != str(user_id):
                    entry(user_id)
                
            else:
                print("Arrived")
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                
                global frameCount
                frameCount +=1
                if frameCount > 2:
                    frameCount = 0
                    print("New face detected")

                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    
                    unique_id = uuid.uuid4()
                    uid=str(unique_id)
                    
                    img_name=uid+'.jpg'
                    cv2.imwrite(img_name,img)
                    shutil.move(img_name, 'imageBasic/'+img_name)
                    image=''
                    with open('imageBasic/'+img_name, 'rb') as image_file:
                        img = Image.open(image_file)
                        img_data = img.tobytes()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                    image = 'data:image/jpeg;base64,' + img_base64
                    print(image)

                    url = 'http://127.0.0.1:5000/new_user'
                    payload = {'user_id':uid,'Image': image}

                    response = requests.post(url, data=payload)
                    
                    print(response)


                    data = "https://www.example.com"
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")

                    img.show()
                    cv2.destroyWindow("Webcam")
                    while True:
                        response = requests.get('http://127.0.0.1:5000/isUserAdded')


                        data = response.json()
                        data = str(data)
                        # print(data)

                        if data == 'data=[] count=None':
                            face_track()
                        else:
                            continue
                    

                    # time.sleep(10)
                
                
                
                
                return
            

        cv2.imshow('Webcam',img)
        if (cv2.waitKey(1) == ord('q') or (cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1)):
            if cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyWindow("Webcam")
            else:
                cv2.destroyWindow('Webcam')
            break

while True:
    face_track()