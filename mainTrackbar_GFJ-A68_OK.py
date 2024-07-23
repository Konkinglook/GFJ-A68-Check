import cv2
import pickle
import cvzone
import numpy as np
import serial
import time

####################################################
arduino = serial.Serial(port='COM3', baudrate=9600 ,timeout=10)

def arduinoDataOut(Output):
    Output = ngCout
    if Output >= 1 : 
        
        print("switch ON")
        arduino.write(b'H')
       
    elif Output == 0 :
        
        print("switch OFF")
        arduino.write(b'L')

###################################################

cap = cv2.VideoCapture(0)
width, height = 26,60
with open('GFJ-A68Pos', 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass

def checkSpaces():
    spaces = 0
    ngCout = 0
    for pos in posList:
        x, y = pos
        w, h = width, height
        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count >= 150:
            color = (0, 200, 0)
            thic = 2
            spaces += 1
        else:
            color = (0, 0, 200)
            thic = 2
            
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,color, 2)

    # cvzone.putTextRect(img, f': {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,colorR=(0, 200, 0)) ค่าเริ่มต้น


    if spaces < 20 :
        ngCout = len(posList) - spaces

    cvzone.putTextRect(img, f'OK : {spaces} PCS', (50, 60), thickness=3, offset=20,colorR=(0, 200, 0))
    cvzone.putTextRect(img, f'NG : {ngCout} PCS', (50, 450), thickness=3, offset=20,colorR=(0, 0, 255))

# ##################################Trackbar####################################
# cv2.namedWindow("Vals")
# cv2.resizeWindow("Vals", 640, 240)
# cv2.createTrackbar("Val1", "Vals", 24, 50, empty) 
# cv2.createTrackbar("Val2", "Vals", 25, 50, empty)
# cv2.createTrackbar("Val3", "Vals", 13, 50, empty)

while True:

    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1) # 3,3 def

    # ###### Default Code use with Trackbar ############ 
    # val1 = cv2.getTrackbarPos("Val1", "Vals")
    # val2 = cv2.getTrackbarPos("Val2", "Vals")
    # val3 = cv2.getTrackbarPos("Val3", "Vals")
    # if val1 % 2 == 0: val1 += 1
    # if val3 % 2 == 0: val3 += 1
    # imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, val1, val2)
    # imgThres = cv2.medianBlur(imgThres, val3)
    

    ###################################### Edit Code ########################################### 
    val1 = 24
    val2 = 26
    val3 = 13
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    ###########################################################################################

    kernel = np.ones((3,3), np.uint8) # 3,3 Def
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)
    

    ##################################################################
    spaces = 0
    ngCout = 0

    for pos in posList:
        x, y = pos
        w, h = width, height
        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)
        
        if count < 65 :
            color = (0, 200, 0)
            thic = 2
            spaces += 1
        else:
            color = (0, 0, 255)
            thic = 2
            
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,color, 2)
        
    cvzone.putTextRect(img, f'OK : {spaces}/{len(posList)} PCS', (50, 60), thickness=3, offset=20,colorR=(0, 200, 0)) ##ค่าเริ่มต้น
    ########################################################
    if spaces < 20 :
        ngCout = len(posList) - spaces
        cvzone.putTextRect(img, f'NG : {ngCout} PCS', (50, 450), thickness=3, offset=20,colorR=(0, 0, 255))
        arduinoDataOut(ngCout)
    else:
        arduinoDataOut(ngCout)
    ###############################################################################   
    

    print("NG = ",ngCout)
    # Display Output
    cv2.imshow("Image", img)
    # cv2.imshow("ImageGray", imgThres)
    # cv2.imshow("ImageBlur", imgBlur)
    if cv2.waitKey(10) & 0xFF == ord("q"): 
        break