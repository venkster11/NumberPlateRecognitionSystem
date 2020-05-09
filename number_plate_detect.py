# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 14:28:12 2020

@author: venka
"""

import cv2
import numpy as np
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os
from google.oauth2 import service_account

if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('serviceAccountKey.json') 
    default_app = firebase_admin.initialize_app(cred)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="serviceAccountKey.json"

db = firestore.Client()


image = cv2.imread('car_dataset/c20.jpeg')


#c19,20,a1,c15,c16,c20,c30,c31,c32,c33,c34,c35,c39,c40,s20 - s38 sies1 - sies3,s17,h17,sih17
#c20,c16,c34,c39,s20,h17.i17   c20,c16,c34,s20,s34,s36,
#s33,s34,s35,s36,sies1,sies3
image = imutils.resize(image, width = 500)
cv2.imshow('1 - Original image',image)
#rgb to gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#noice remv
gray = cv2.bilateralFilter(gray, 11, 17, 17)

#edge og grayscale img
edged = cv2.Canny(gray, 170, 200)


#finding countours on edges
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST,
                             cv2.CHAIN_APPROX_SIMPLE)
img1cpy = image.copy()
cv2.drawContours(img1cpy, cnts, -1, (255,0,255), 2)

#sorting contours
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
NumberPlateCnt = None

#top 30 contours
img2cpy = image.copy()
cv2.drawContours(img2cpy, cnts, -1, (255,0,255), 2)

#finding the best contours for num plate
count = 0
idx = 7
for c in cnts:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        NumberPlateCnt = approx
        #crop contours
        
        x, y, w, h = cv2.boundingRect(c) 
        new_img = gray[y:y + h, x:x + w]
        
        cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img)
        idx+=1
        
        break
    
    
cv2.drawContours(image, [NumberPlateCnt], -1, (255,0,255), 2)
        
Cropped_img_loc = 'Cropped Images-Text/7.png'

cv2.imshow('2 - Gray image', gray)
cv2.imshow("3 - bilateral Filter", gray)
cv2.imshow("4 - canny edges", edged)
cv2.imshow("5 - contours", img1cpy)
cv2.imshow("6 - top 30 contours", img2cpy)
cv2.imshow("7 - Number plate",image)
cv2.imshow("8 - Cropped img", cv2.imread(Cropped_img_loc))


new_img = cv2.resize(new_img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
kernel = np.ones((1, 1), np.uint8)
new_img = cv2.dilate(new_img, kernel, iterations=1)
new_img = cv2.erode(new_img, kernel, iterations=1)

cv2.threshold(cv2.GaussianBlur(new_img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.threshold(cv2.bilateralFilter(new_img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.threshold(cv2.medianBlur(new_img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.adaptiveThreshold(cv2.GaussianBlur(new_img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

cv2.adaptiveThreshold(cv2.bilateralFilter(new_img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

cv2.adaptiveThreshold(cv2.medianBlur(new_img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img)
nCropped_img_loc = 'Cropped Images-Text/8.png'

text = pytesseract.image_to_string(nCropped_img_loc, lang = 'eng')
import re
clean_NumPlt = re.sub('\W+','', text )
clean_NumPlt = clean_NumPlt.rstrip('_')
print("\nCharacter recognition using Tesseract OCR")
print("Car Number is:", text)
print("Car Number is:", clean_NumPlt)
cv2.imshow("9 - new Cropped img", cv2.imread(nCropped_img_loc))

import time
ts = time.time()
import datetime
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d  %H:%M:%S')
print(st)

doc_ref = db.collection(u'currentlogs').document()
doc_ref.set({
    u'plate_num': clean_NumPlt,
    u'time_stamp': st,
    u'status': "Not Known",
    u'entry_status': "Not Known"
    
})

cv2.waitKey(0)
cv2.destroyAllWindows()



#gray = cv2.bilateralFilter(gray, 170, 200)
