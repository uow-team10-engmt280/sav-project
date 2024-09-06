import cv2 as cv
import numpy as np


# TODO Need to make it capable of video stream

def MV() -> list[int]:
    image = cv.imread("c:/Users/LucaC/OneDrive/Documents/Visual Studio Code/University/Python/ENGMT280/picCamTow (5).png")

    def rescaleFrame(frame, scale=0.50):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)

        dimensions = (width, height)

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def nothing(x):
        pass

    rimage = rescaleFrame(image)
    # cv.imshow('Cam Tower 01', rimage)

    # S_mask = np.zeros((rimage.shape[0], rimage.shape[1], 3), dtype='uint8') # Very good
    S_mask = np.zeros((480, 640, 3), dtype='uint8')
    cv.namedWindow('Controls')
    cv.resizeWindow('Controls', 400, 500)

    cv.createTrackbar('H', 'Controls', 0, int(rimage.shape[0]), nothing)
    cv.createTrackbar('W', 'Controls', int(rimage.shape[1]), int(rimage.shape[1]), nothing)
    cv.createTrackbar('Find B', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find G', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find R', 'Controls', 0, 1, nothing)
    cv.createTrackbar('Find Y', 'Controls', 0, 1, nothing)


    cv.createTrackbar('Hue lower','Controls', 0, 180, nothing)
    cv.createTrackbar('Sat lower','Controls', 0, 255, nothing)
    cv.createTrackbar('Val lower','Controls', 0, 255, nothing)
    cv.createTrackbar('Hue higher','Controls', 180, 180, nothing)
    cv.createTrackbar('Sat higher','Controls', 255, 255, nothing)
    cv.createTrackbar('Val higher','Controls', 255, 255, nothing)

    while(True):
        # s = cv.getTrackbarPos('Switch','Controls')
        testH = cv.getTrackbarPos('H', 'Controls')
        testW = cv.getTrackbarPos('W', 'Controls')
        b = cv.getTrackbarPos('Find B','Controls')
        g = cv.getTrackbarPos('Find G','Controls')
        r = cv.getTrackbarPos('Find R','Controls')
        y = cv.getTrackbarPos('Find Y','Controls')

        if b == 1:
            cv.setTrackbarPos('Hue lower','Controls', 31)
            cv.setTrackbarPos('Sat lower','Controls', 219)
            cv.setTrackbarPos('Val lower','Controls', 87)
            cv.setTrackbarPos('Hue higher','Controls', 180)
            cv.setTrackbarPos('Sat higher','Controls', 255)
            cv.setTrackbarPos('Val higher','Controls', 255)
            cv.setTrackbarPos('Find B','Controls', 0)
        elif g == 1:
            cv.setTrackbarPos('Hue lower','Controls', 25)
            cv.setTrackbarPos('Sat lower','Controls', 146)
            cv.setTrackbarPos('Val lower','Controls', 86)
            cv.setTrackbarPos('Hue higher','Controls', 180)
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
            cv.setTrackbarPos('Hue lower','Controls', 24)
            cv.setTrackbarPos('Sat lower','Controls', 65)
            cv.setTrackbarPos('Val lower','Controls', 145)
            cv.setTrackbarPos('Hue higher','Controls', 57)
            cv.setTrackbarPos('Sat higher','Controls', 255)
            cv.setTrackbarPos('Val higher','Controls', 230)
            cv.setTrackbarPos('Find Y','Controls', 0)
        else:
            hue_l = cv.getTrackbarPos('Hue lower','Controls')
            sat_l = cv.getTrackbarPos('Sat lower','Controls')
            val_l = cv.getTrackbarPos('Val lower','Controls')
            hue_h = cv.getTrackbarPos('Hue higher','Controls')
            sat_h = cv.getTrackbarPos('Sat higher','Controls')
            val_h = cv.getTrackbarPos('Val higher','Controls')

        cv.rectangle(S_mask, (int(rimage.shape[1]), int(rimage.shape[0])), (0,0), (255, 255, 255), -1)
        cv.rectangle(S_mask, (testW, testH), (0,0), (0, 0, 0), -1)
        # cv.imshow('Sliding mask', S_mask)

        # Blurs the video for better edge detection
        blurred = cv.bilateralFilter(rimage, 5, 30, 50)
        # Coverts to HSV colour space
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
        cv.imshow('HSV', hsv)
        # Sets the HSV threshold values (controlled by sliders)
        hsvThreshold = cv.inRange(hsv, (hue_l, sat_l, val_l), (hue_h, sat_h, val_h)) 
        # Finds the contours
        contours, hierarchy = cv.findContours(hsvThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # Draws the contours onto out bitmap mask
        cv.drawContours(hsvThreshold, contours, -1, (0, 255, 0), 1)
        # Puts the mask over our camera feed
        maskedImage = cv.bitwise_and(rimage, rimage, mask=hsvThreshold)
        sMaskGrey = cv.cvtColor(S_mask, cv.COLOR_BGR2GRAY)
        empty, bitMap = cv.threshold(sMaskGrey, 100, 255, cv.THRESH_BINARY)
        FinalImage = cv.bitwise_and(maskedImage, maskedImage, mask=bitMap)

        numBoxes = 0
        boxes = []
        for c in contours:
            area = cv.contourArea(c)
            if (area > 500) & (area < 3000):
                numBoxes = numBoxes + 1
                x, y, w, h = cv.boundingRect(c)
                boxes.append(int(x + w/2))
                cv.rectangle(FinalImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
                centroid_x = x + w/2
                centroid_y = y + h/2
                cv.putText(FinalImage, "x= " + str(centroid_x) + " y= " + str(centroid_y), 
                        (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)
        # print(numBoxes)
        # print(boxes)
        # print(type(boxes))
        direction1 = []
        direction2 = []

        if numBoxes == 2:
            if boxes[1] < boxes[0]:
                boxes.reverse()

        # print(boxes)
        if numBoxes > 1:
            if boxes[1] > int(rimage.shape[1])*7/8:
                direction1 = [0, 0]
            elif boxes[1] > int(rimage.shape[1])*6/8:
                direction1 = [0, 1]
            elif boxes[1] > int(rimage.shape[1])*5/8:
                direction1 = [1, 0]
            elif boxes[1] > int(rimage.shape[1])*4/8:
                direction1 = [1, 1]

        if numBoxes > 0:
            if boxes[0] < int(rimage.shape[1])*1/8:
                direction2 = [0, 0]
            elif boxes[0] < int(rimage.shape[1])*2/8:
                direction2 = [0, 1]
            elif boxes[0] < int(rimage.shape[1])*3/8:
                direction2 = [1, 0]
            elif boxes[0] < int(rimage.shape[1])*4/8:
                direction2 = [1, 1]


        direction = direction1 + direction2
        print(direction)

        # cv.imshow('Contoured Image', hsvThreshold)
        cv.imshow('Masked Image', maskedImage)
        cv.imshow('Final Image', FinalImage)

        if cv.waitKey(20) & 0xFF==ord('e'):
            break

    cv.waitKey(0)
    cv.destroyAllWindows()
    return direction




# Image part still needs some fixing, but could definitely get a good mark





#=============================================================================
# Reading the camera feed
# facecam = cv.VideoCapture(0)

# def nothing(x):
#     pass

# img = np.zeros((300,512,3), np.uint8)
# cv.namedWindow('Masked Image')

# cv.createTrackbar('Hue_l','Masked Image', 0, 180, nothing)
# cv.createTrackbar('Sat_l','Masked Image', 0, 255, nothing)
# cv.createTrackbar('Val_l','Masked Image', 0, 255, nothing)
# cv.createTrackbar('Hue_h','Masked Image', 0, 180, nothing)
# cv.createTrackbar('Sat_h','Masked Image', 0, 255, nothing)
# cv.createTrackbar('Val_h','Masked Image', 0, 255, nothing)

# while True:
#     # Gets the position of the slider
#     hue_l = cv.getTrackbarPos('Hue_l','Masked Image')
#     sat_l = cv.getTrackbarPos('Sat_l','Masked Image')
#     val_l = cv.getTrackbarPos('Val_l','Masked Image')
#     hue_h = cv.getTrackbarPos('Hue_h','Masked Image')
#     sat_h = cv.getTrackbarPos('Sat_h','Masked Image')
#     val_h = cv.getTrackbarPos('Val_h','Masked Image')
    
#     # Gets the video stream
#     isTrue, frame = facecam.read()
#     # Flips the video so it's like mirror
#     flipped = cv.flip(frame, 1)
#     cv.imshow('Camera', flipped)
#     # Blurs the video, potentially REMOVE when figure out about small contours
#     blurred = cv.bilateralFilter(flipped, 5, 30, 50)
#     cv.imshow('Blur', blurred)

#     # Coverts to HSV colour space
#     hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
#     # H, S, V = cv.split(hsv)

#     # Sets the HSV threshold values (controlled by sliders)
#     hsvThreshold = cv.inRange(hsv, (hue_l, sat_l, val_l), (hue_h, sat_h, val_h)) # Mask/bitmap
#     # cv.imshow('Threshold', hsvThreshold) 
#     # Converts to grey scale (better edge detection)
#     greyScale = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
#     ret, greyThresh = cv.threshold(greyScale, 90, 255, 0)
#     # Finds the contours
#     contours, hierarchy = cv.findContours(greyThresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
#     # Draws the contours onto out bitmap mask
#     cv.drawContours(hsvThreshold, contours, -1, (0, 255, 0), 1)
#     # Puts the mask over our camera feed
#     maskedImage = cv.bitwise_and(flipped, flipped, mask=hsvThreshold)

#     for c in contours:
#         area = cv.contourArea(c)
#         if area > 300:
#             x, y, w, h = cv.boundingRect(c)
#             cv.rectangle(maskedImage, (x, y), (x+w, y+h), (255, 0, 0), 2)
#             cv.drawContours(hsvThreshold, c, -1, (0, 0, 0), 1)
#         elif area > 700:
#             x, y, w, h = cv.boundingRect(c)
#             cv.rectangle(maskedImage, (x, y), (x+w, y+h), (0, 255, 0), 2)

#     cv.imshow('Contoured Image', hsvThreshold)
#     cv.imshow('Masked Image', maskedImage)
 
#     if cv.waitKey(20) & 0xFF==ord('e'):
#         break

# facecam.release()
# cv.destroyAllWindows()
