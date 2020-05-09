# TrainDataGenerate.py

import sys
import numpy as np
import cv2
import os


MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


global npaFlattenedImages

global intClassifications       


def main():
   npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
   intClassifications = []
                                    
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/2.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/1.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/3.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/4.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/5.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/6.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/7.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/8.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/9.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/10.png",npaFlattenedImages,intClassifications)
   npaFlattenedImages,intClassifications = trainimg("LicenceCharDataset/11.png",npaFlattenedImages,intClassifications)
  
   print("\n\ntraining complete !!\n")

   return

def trainimg(img_name,npaFlattenedImages,intClassifications):
    
    imgTrainingNumbers = cv2.imread(img_name)           

    if imgTrainingNumbers is None:                          
        print ("error: image not read from file \n\n")        
        os.system("pause")                                  
        return                                              
    # end if

    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)          
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        

                                                        
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           
                                      255,                                  
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,               
                                      11,                                   
                                      2)                                    

    cv2.imshow("imgThresh", imgThresh)      

    imgThreshCopy = imgThresh.copy()        

    npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        
                                                 cv2.RETR_EXTERNAL,                
                                                 cv2.CHAIN_APPROX_SIMPLE)           

                               

             
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')]

    for npaContour in npaContours:                          
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:          
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)        

                                                
            cv2.rectangle(imgTrainingNumbers,          
                          (intX, intY),                
                          (intX+intW,intY+intH),        
                          (0, 0, 255),                 
                          2)                           

            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                  
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))     

            cv2.imshow("imgROI", imgROI)                    
            cv2.imshow("imgROIResized", imgROIResized)      
            cv2.imshow("training_numbers.png", imgTrainingNumbers)      

            intChar = cv2.waitKey(0)                     

            if intChar == 27:                  
                sys.exit()                     
            elif intChar in intValidChars:      

                intClassifications.append(intChar)                                                

                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                    
            # end if
        # end if
    # end for

    fltClassifications = np.array(intClassifications, np.float32)                  

    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   

   

    np.savetxt("classifications.txt", npaClassifications)           
    np.savetxt("flattened_images.txt", npaFlattenedImages)         

    cv2.destroyAllWindows()
    return npaFlattenedImages,intClassifications


if __name__ == "__main__":
    main()
# end if




