# TrainAndTest.py

import cv2
import numpy as np
import operator
import os

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


class ContourWithData():

    
    npaContour = None           
    boundingRect = None         
    intRectX = 0                
    intRectY = 0                
    intRectWidth = 0            
    intRectHeight = 0           
    fltArea = 0.0              

    def calculateRectTopLeftPointAndWidthAndHeight(self):               
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            
        if self.fltArea < MIN_CONTOUR_AREA: return False        
        return True


def main():
    allContoursWithData = []                
    validContoursWithData = []              

    try:
        npaClassifications = np.loadtxt("classifications1.txt", np.float32)                  
    except:
        print ("error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_images1.txt", np.float32)                 
    except:
        print ("error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       

    kNearest = cv2.ml.KNearest_create()                   

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
    nCropped_img_loc = 'Cropped Images-Text/8.png'

    imgTestingNumbers = cv2.imread(nCropped_img_loc)          

    if imgTestingNumbers is None:                           
        print ("error: image not read from file \n\n")        
        os.system("pause")                                  
        return                                              
    # end if

    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)       
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    

                                                       
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           
                                      255,                                  
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,                
                                      11,                                  
                                      2)                                    

    imgThreshCopy = imgThresh.copy()        

    npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             
                                                 cv2.RETR_EXTERNAL,         
                                                 cv2.CHAIN_APPROX_SIMPLE)   

    for npaContour in npaContours:                             
        contourWithData = ContourWithData()                                             
        contourWithData.npaContour = npaContour                                        
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                   
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           
        allContoursWithData.append(contourWithData)                                     
    # end for

    for contourWithData in allContoursWithData:                
        if contourWithData.checkIfContourIsValid():             
            validContoursWithData.append(contourWithData)      
        # end if
    # end for

    validContoursWithData.sort(key = operator.attrgetter("intRectX"))        

    strFinalString = ""         

    for contourWithData in validContoursWithData:            
                                               
        cv2.rectangle(imgTestingNumbers,                                       
                      (contourWithData.intRectX, contourWithData.intRectY),     
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      
                      (0, 255, 0),              
                      2)                       

        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,    
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             

        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      

        npaROIResized = np.float32(npaROIResized)       

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 5)     

        strCurrentChar = str(chr(int(npaResults[0][0])))                                             

        strFinalString = strFinalString + strCurrentChar            
    # end for
   

    print("\nCharacter recognition using KNN Algorithm")
    print ("\n" + strFinalString[2:] + "\n")          

    cv2.imshow("Char recognition", imgTestingNumbers)      
 
    cv2.waitKey(0)                                          

    cv2.destroyAllWindows()             

    return


if __name__ == "__main__":
    main()
# end if









