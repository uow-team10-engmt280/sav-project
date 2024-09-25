# NOTE RED

import cv2 as cv
import numpy as np
# from picamzero import Camera # type: ignore

# def takePicture():
#     cam = Camera()
#     cam.start_preview()
#     cam.take_photo('~/Desktop/cameraPhoto.jpg')
#     cam.stop_preview()
    

def MV() -> list[bool]:
    image = cv.imread("C:/Users/LucaC/OneDrive/Documents/GitHub/sav-project/LucaCittadini/MachineVisionPictures/picCamTow (19).png")
    # image = cv.imread('~/Desktop/cameraPhoto.jpg') # For when on track
    def rescaleFrame(frame, scale=0.50):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)

        dimensions = (width, height)

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def nothing() -> None:
        pass

    rimage = rescaleFrame(image) # NOTE might not need this when actually on track

    S_mask = np.zeros((rimage.shape[0], rimage.shape[1], 3), dtype='uint8') # Makes an array the same size as the photo/picture
    # S_mask = np.zeros((480, 640, 3), dtype='uint8')
    cv.namedWindow('Controls')
    cv.resizeWindow('Controls', 400, 500)

    cv.createTrackbar('H', 'Controls', 0, int(rimage.shape[0]), nothing)
    cv.createTrackbar('W', 'Controls', int(rimage.shape[1]), int(rimage.shape[1]), nothing)
    cv.createTrackbar('Find B', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find G', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find R', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find Y', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find Special R', 'Controls', 0, 1, nothing)

    cv.createTrackbar('Hue lower','Controls', 0, 180, nothing)
    cv.createTrackbar('Sat lower','Controls', 0, 255, nothing)
    cv.createTrackbar('Val lower','Controls', 0, 255, nothing)
    cv.createTrackbar('Hue higher','Controls', 180, 180, nothing)
    cv.createTrackbar('Sat higher','Controls', 255, 255, nothing)
    cv.createTrackbar('Val higher','Controls', 255, 255, nothing)

    while(True):
        testH = cv.getTrackbarPos('H', 'Controls')
        testW = cv.getTrackbarPos('W', 'Controls')
        b = cv.getTrackbarPos('Find B', 'Controls')
        g = cv.getTrackbarPos('Find G', 'Controls')
        r = cv.getTrackbarPos('Find R', 'Controls')
        y = cv.getTrackbarPos('Find Y', 'Controls')
        sc = cv.getTrackbarPos('Find Special R', 'Controls')

        if b == 1:
            cv.setTrackbarPos('Hue lower','Controls', 31)
            cv.setTrackbarPos('Sat lower','Controls', 250)
            cv.setTrackbarPos('Val lower','Controls', 87)
            cv.setTrackbarPos('Hue higher','Controls', 180)
            cv.setTrackbarPos('Sat higher','Controls', 255)
            cv.setTrackbarPos('Val higher','Controls', 255)
            cv.setTrackbarPos('Find B','Controls', 0)
        elif g == 1:
            cv.setTrackbarPos('Hue lower','Controls', 25)
            cv.setTrackbarPos('Sat lower','Controls', 146)
            cv.setTrackbarPos('Val lower','Controls', 86)
            cv.setTrackbarPos('Hue higher','Controls', 90)
            cv.setTrackbarPos('Sat higher','Controls', 216)
            cv.setTrackbarPos('Val higher','Controls', 212)
            cv.setTrackbarPos('Find G','Controls', 0)
        elif r == 1:
            cv.setTrackbarPos('Hue lower','Controls', 0)
            cv.setTrackbarPos('Sat lower','Controls', 207)
            cv.setTrackbarPos('Val lower','Controls', 50)
            cv.setTrackbarPos('Hue higher','Controls', 21)
            cv.setTrackbarPos('Sat higher','Controls', 255)
            cv.setTrackbarPos('Val higher','Controls', 255)
            cv.setTrackbarPos('Find R','Controls', 0)
        elif y == 1: 
            cv.setTrackbarPos('Hue lower', 'Controls', 15)
            cv.setTrackbarPos('Sat lower', 'Controls', 210)
            cv.setTrackbarPos('Val lower', 'Controls', 50)
            cv.setTrackbarPos('Hue higher', 'Controls', 57)
            cv.setTrackbarPos('Sat higher', 'Controls', 255)
            cv.setTrackbarPos('Val higher', 'Controls', 230)
            cv.setTrackbarPos('Find Y', 'Controls', 0)
        elif sc == 1:
            cv.setTrackbarPos('Hue lower', 'Controls', 0)
            cv.setTrackbarPos('Sat lower', 'Controls', 210)
            cv.setTrackbarPos('Val lower', 'Controls', 50)
            cv.setTrackbarPos('Hue higher', 'Controls', 180)
            cv.setTrackbarPos('Sat higher', 'Controls', 250)
            cv.setTrackbarPos('Val higher', 'Controls', 255)
            cv.setTrackbarPos('Find Special R', 'Controls', 0)
        else:
            hue_l = cv.getTrackbarPos('Hue lower','Controls')
            sat_l = cv.getTrackbarPos('Sat lower','Controls')
            val_l = cv.getTrackbarPos('Val lower','Controls')
            hue_h = cv.getTrackbarPos('Hue higher','Controls')
            sat_h = cv.getTrackbarPos('Sat higher','Controls')
            val_h = cv.getTrackbarPos('Val higher','Controls')

        cv.rectangle(S_mask, (int(rimage.shape[1]), int(rimage.shape[0])), (0,0), (255, 255, 255), -1)
        cv.rectangle(S_mask, (testW, testH), (0,0), (0, 0, 0), -1)

        sMaskGrey = cv.cvtColor(S_mask, cv.COLOR_BGR2GRAY) # Converts the sliding mask to greyscale (needs to be to be turned into bitmap)
        empty, bitMap = cv.threshold(sMaskGrey, 100, 255, cv.THRESH_BINARY) # Gets bitmap in shape of sliding mask
        maskedImage = cv.bitwise_and(rimage, rimage, mask=bitMap)

        
        blurred = cv.bilateralFilter(maskedImage, 5, 30, 50) # Blurs the video for better edge detection
      
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV) # Coverts to HSV colour space
       
        hsvThreshold = cv.inRange(hsv, (hue_l, sat_l, val_l), (hue_h, sat_h, val_h))  # Sets the HSV threshold values (controlled by sliders)

        contours, hierarchy = cv.findContours(hsvThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # Draws the contours onto out bitmap mask
       
        cv.drawContours(hsvThreshold, contours, -1, (0, 255, 0), 1)

        FinalImage = cv.bitwise_and(maskedImage, maskedImage, mask=hsvThreshold)

        numBoxes = 0
        boxes = []
        for contour in contours:
            area = cv.contourArea(contour)
            if (area > 500) & (area < 3000):
                numBoxes = numBoxes + 1
                x, y, w, h = cv.boundingRect(contour)
                boxes.append(int(x + w/2))
                cv.rectangle(FinalImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
                centroid_x = x + w/2
                centroid_y = y + h/2
                cv.putText(FinalImage, "x= " + str(centroid_x) + " y= " + str(centroid_y), 
                        (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)
        direction1 = []
        direction2 = []

        if numBoxes == 2:
            if boxes[1] < boxes[0]:
                boxes.reverse()

        # print(boxes)
        if numBoxes > 1:
            if boxes[1] > int(rimage.shape[1])*7/8:
                direction1 = [False, False]
            elif boxes[1] > int(rimage.shape[1])*6/8:
                direction1 = [False, True]
            elif boxes[1] > int(rimage.shape[1])*5/8:
                direction1 = [True, False]
            elif boxes[1] > int(rimage.shape[1])*4/8:
                direction1 = [True, True]

        if numBoxes > 0:
            if boxes[0] < int(rimage.shape[1])*1/8:
                direction2 = [False, False]
            elif boxes[0] < int(rimage.shape[1])*2/8:
                direction2 = [False, True]
            elif boxes[0] < int(rimage.shape[1])*3/8:
                direction2 = [True, False]
            elif boxes[0] < int(rimage.shape[1])*4/8:
                direction2 = [True, True]


        direction = direction1 + direction2
        # print(direction)

        cv.imshow('Final Image', FinalImage)

        if cv.waitKey(20) & 0xFF==ord('e'):
            break

    cv.waitKey(0)
    cv.destroyAllWindows()
    return direction

# try:
#     MV()
# except:
#     print('Failed to run programme')

#=============================================================================
# Reading the camera feed
# def MVvid() -> list[bool]:
#     facecam = cv.VideoCapture(0)

#     def nothing() -> None:
#         pass

#     # S_mask = np.zeros((facecam.shape[0], facecam.shape[1], 3), dtype='uint8') # Very good
#     S_mask = np.zeros((480, 640, 3), dtype='uint8')
#     cv.namedWindow('Controls')
#     cv.resizeWindow('Controls', 400, 500)

#     cv.createTrackbar('H', 'Controls', 0, int(facecam.shape[0]), nothing)
#     cv.createTrackbar('W', 'Controls', int(facecam.shape[1]), int(facecam.shape[1]), nothing)
#     cv.createTrackbar('Find B', 'Controls', 0, 1, nothing)
#     cv.createTrackbar('Find G', 'Controls', 0, 1, nothing)
#     cv.createTrackbar('Find R', 'Controls', 0, 1, nothing)
#     cv.createTrackbar('Find Y', 'Controls', 0, 1, nothing)
#     cv.createTrackbar('Find Special R', 'Controls', 0, 1, nothing)

#     cv.createTrackbar('Hue lower','Controls', 0, 180, nothing)
#     cv.createTrackbar('Sat lower','Controls', 0, 255, nothing)
#     cv.createTrackbar('Val lower','Controls', 0, 255, nothing)
#     cv.createTrackbar('Hue higher','Controls', 180, 180, nothing)
#     cv.createTrackbar('Sat higher','Controls', 255, 255, nothing)
#     cv.createTrackbar('Val higher','Controls', 255, 255, nothing)

#     while(True):
#         testH = cv.getTrackbarPos('H', 'Controls')
#         testW = cv.getTrackbarPos('W', 'Controls')
#         b = cv.getTrackbarPos('Find B', 'Controls')
#         g = cv.getTrackbarPos('Find G', 'Controls')
#         r = cv.getTrackbarPos('Find R', 'Controls')
#         y = cv.getTrackbarPos('Find Y', 'Controls')
#         sc = cv.getTrackbarPos('Find Special R', 'Controls')

#         if b == 1:
#             cv.setTrackbarPos('Hue lower','Controls', 31)
#             cv.setTrackbarPos('Sat lower','Controls', 250)
#             cv.setTrackbarPos('Val lower','Controls', 87)
#             cv.setTrackbarPos('Hue higher','Controls', 180)
#             cv.setTrackbarPos('Sat higher','Controls', 255)
#             cv.setTrackbarPos('Val higher','Controls', 255)
#             cv.setTrackbarPos('Find B','Controls', 0)
#         elif g == 1:
#             cv.setTrackbarPos('Hue lower','Controls', 25)
#             cv.setTrackbarPos('Sat lower','Controls', 146)
#             cv.setTrackbarPos('Val lower','Controls', 86)
#             cv.setTrackbarPos('Hue higher','Controls', 90)
#             cv.setTrackbarPos('Sat higher','Controls', 216)
#             cv.setTrackbarPos('Val higher','Controls', 212)
#             cv.setTrackbarPos('Find G','Controls', 0)
#         elif r == 1:
#             cv.setTrackbarPos('Hue lower','Controls', 0)
#             cv.setTrackbarPos('Sat lower','Controls', 207)
#             cv.setTrackbarPos('Val lower','Controls', 50)
#             cv.setTrackbarPos('Hue higher','Controls', 21)
#             cv.setTrackbarPos('Sat higher','Controls', 255)
#             cv.setTrackbarPos('Val higher','Controls', 255)
#             cv.setTrackbarPos('Find R','Controls', 0)
#         elif y == 1: 
#             cv.setTrackbarPos('Hue lower', 'Controls', 15)
#             cv.setTrackbarPos('Sat lower', 'Controls', 210)
#             cv.setTrackbarPos('Val lower', 'Controls', 50)
#             cv.setTrackbarPos('Hue higher', 'Controls', 57)
#             cv.setTrackbarPos('Sat higher', 'Controls', 255)
#             cv.setTrackbarPos('Val higher', 'Controls', 230)
#             cv.setTrackbarPos('Find Y', 'Controls', 0)
#         elif sc == 1:
#             cv.setTrackbarPos('Hue lower', 'Controls', 0)
#             cv.setTrackbarPos('Sat lower', 'Controls', 210)
#             cv.setTrackbarPos('Val lower', 'Controls', 50)
#             cv.setTrackbarPos('Hue higher', 'Controls', 180)
#             cv.setTrackbarPos('Sat higher', 'Controls', 250)
#             cv.setTrackbarPos('Val higher', 'Controls', 255)
#             cv.setTrackbarPos('Find Special R', 'Controls', 0)
#         else:
#             hue_l = cv.getTrackbarPos('Hue lower','Controls')
#             sat_l = cv.getTrackbarPos('Sat lower','Controls')
#             val_l = cv.getTrackbarPos('Val lower','Controls')
#             hue_h = cv.getTrackbarPos('Hue higher','Controls')
#             sat_h = cv.getTrackbarPos('Sat higher','Controls')
#             val_h = cv.getTrackbarPos('Val higher','Controls')

#         cv.rectangle(S_mask, (int(facecam.shape[1]), int(facecam.shape[0])), (0,0), (255, 255, 255), -1)
#         cv.rectangle(S_mask, (testW, testH), (0,0), (0, 0, 0), -1)

#         sMaskGrey = cv.cvtColor(S_mask, cv.COLOR_BGR2GRAY) # Converts the sliding mask to greyscale (needs to be to be turned into bitmap)
#         empty, bitMap = cv.threshold(sMaskGrey, 100, 255, cv.THRESH_BINARY) # Gets bitmap in shape of sliding mask
#         maskedImage = cv.bitwise_and(facecam, facecam, mask=bitMap)

#         # Blurs the video for better edge detection
#         blurred = cv.bilateralFilter(maskedImage, 5, 30, 50)
#         # Coverts to HSV colour space
#         hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
#         # Sets the HSV threshold values (controlled by sliders)
#         hsvThreshold = cv.inRange(hsv, (hue_l, sat_l, val_l), (hue_h, sat_h, val_h)) 

#         contours, hierarchy = cv.findContours(hsvThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         # Draws the contours onto out bitmap mask
#         cv.drawContours(hsvThreshold, contours, -1, (0, 255, 0), 1)
#         # Puts the mask over our camera feed
#         FinalImage = cv.bitwise_and(maskedImage, maskedImage, mask=hsvThreshold)

#         numBoxes = 0
#         boxes = []
#         for contour in contours:
#             area = cv.contourArea(contour)
#             if (area > 500) & (area < 3000):
#                 numBoxes = numBoxes + 1
#                 x, y, w, h = cv.boundingRect(contour)
#                 boxes.append(int(x + w/2))
#                 cv.rectangle(FinalImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 centroid_x = x + w/2
#                 centroid_y = y + h/2
#                 cv.putText(FinalImage, "x= " + str(centroid_x) + " y= " + str(centroid_y), 
#                         (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)
#         direction1 = []
#         direction2 = []

#         if numBoxes == 2:
#             if boxes[1] < boxes[0]:
#                 boxes.reverse()

#         # print(boxes)
#         if numBoxes > 1:
#             if boxes[1] > int(facecam.shape[1])*7/8:
#                 direction1 = [False, False]
#             elif boxes[1] > int(facecam.shape[1])*6/8:
#                 direction1 = [False, True]
#             elif boxes[1] > int(facecam.shape[1])*5/8:
#                 direction1 = [True, False]
#             elif boxes[1] > int(facecam.shape[1])*4/8:
#                 direction1 = [True, True]

#         if numBoxes > 0:
#             if boxes[0] < int(facecam.shape[1])*1/8:
#                 direction2 = [False, False]
#             elif boxes[0] < int(facecam.shape[1])*2/8:
#                 direction2 = [False, True]
#             elif boxes[0] < int(facecam.shape[1])*3/8:
#                 direction2 = [True, False]
#             elif boxes[0] < int(facecam.shape[1])*4/8:
#                 direction2 = [True, True]

#         direction = direction1 + direction2
#         print(direction)

#         cv.imshow('Final Image', FinalImage)

#         if cv.waitKey(20) & 0xFF==ord('e'):
#             break

#     cv.waitKey(0)
#     facecam.release()
#     cv.destroyAllWindows()
#     return direction


# # MVvid()
