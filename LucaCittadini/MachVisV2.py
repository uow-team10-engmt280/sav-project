# NOTE RED
import cv2 as cv
import numpy as np
from picamera2 import Picamera2 # type: ignore # NOTE this is for taking the picture
import paho.mqtt.client as paho # type: ignore # NOTE this is for subscribing
from time import sleep, time
# MQTT = Message Queuing Telemetry Transport

def MV() -> list[bool]:
    def takePicture(): 
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(raw = {"size": (1640, 1232)}, main = {"size": (1280, 960), "format": 'RGB888'}))
        picam2.start()

    def rescaleFrame(frame, scale=0.50):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
    
    def createWindows(function): # Decorator - It creates the window with the controls and creates the sliding mask, this decorates the mainloop because these things will always need to exist
        def wrapper(): # should fix so that it makes sense, but it does it's function
            def nothing(placeHolder) -> None:
                pass
            image = np.zeros()
            slidingMask = np.zeros((image.shape[0], image.shape[1], 3), dtype='uint8') # Makes an array the same size as the photo/picture
            # slidingMask = np.zeros((480, 640, 3), dtype='uint8')
            cv.namedWindow('Controls')
            cv.resizeWindow('Controls', 600, 550)

            cv.createTrackbar('DIRECTIONS ACQUIRED', 'Controls', 0, 1, nothing)
            cv.createTrackbar('H', 'Controls', 0, int(image.shape[0]), nothing)
            cv.createTrackbar('W', 'Controls', int(image.shape[1]), int(image.shape[1]), nothing)
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
            return function(slidingMask) 
        return wrapper
    
    @createWindows
    def mainLoop(S_mask, rimage) -> list[bool]:
        direction1 = []
        direction2 = []
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(raw = {"size": (1640, 1232)}, main = {"size": (1280, 960), "format": 'RGB888'}))
        picam2.start()
        frequency = 60
        startTime = time()
        count = 0
        
        while True:
            image = rescaleFrame(picam2.capture_array())
            cv.imshow('Video Stream', image)
            nowTime = time()
            elaspedTime = nowTime - startTime
            if elaspedTime > frequency:
                fileName = f'Snap{str(count)}.png'
                cv.imwrite(fileName, image)
                count += 1
                startTime = time()
            if cv.waitKey(0) == 27:
                break
            testH = cv.getTrackbarPos('H', 'Controls')
            testW = cv.getTrackbarPos('W', 'Controls')
            b = cv.getTrackbarPos('Find B', 'Controls')
            g = cv.getTrackbarPos('Find G', 'Controls')
            r = cv.getTrackbarPos('Find R', 'Controls')
            y = cv.getTrackbarPos('Find Y', 'Controls')
            sc = cv.getTrackbarPos('Find Special R', 'Controls')
            stop = cv.getTrackbarPos('DIRECTIONS ACQUIRED', 'Controls')

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

            # Creating the image
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
            for contour in contours: # Finds location of 
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

            if numBoxes == 2: # This is if all the stops are present
                if boxes[1] < boxes[0]: # This just corrects the index of the boxes so that the 0th box is on the left
                    boxes.reverse()
            match numBoxes:
                case 2:
                    if boxes[1] < boxes[0]:
                        boxes.reverse()

                    if boxes[1] > int(rimage.shape[1])*7/8:
                        direction1 = [False, False]
                    elif boxes[1] > int(rimage.shape[1])*6/8:
                        direction1 = [False, True]
                    elif boxes[1] > int(rimage.shape[1])*5/8:
                        direction1 = [True, False]
                    elif boxes[1] > int(rimage.shape[1])*4/8:
                        direction1 = [True, True]

                    if boxes[0] < int(rimage.shape[1])*1/8:
                        direction2 = [False, False]
                    elif boxes[0] < int(rimage.shape[1])*2/8:
                        direction2 = [False, True]
                    elif boxes[0] < int(rimage.shape[1])*3/8:
                        direction2 = [True, False]
                    elif boxes[0] < int(rimage.shape[1])*4/8:
                        direction2 = [True, True]

                case 1:
                    if boxes[0] > int(rimage.shape[1])*7/8:
                        direction1 = [False, False]
                    elif boxes[0] > int(rimage.shape[1])*6/8:
                        direction1 = [False, True]
                    elif boxes[0] > int(rimage.shape[1])*5/8:
                        direction1 = [True, False]
                    elif boxes[0] > int(rimage.shape[1])*4/8:
                        direction1 = [True, True]

            cv.imshow('Final Image', FinalImage)
            if cv.waitKey(20) & stop == 1:
                    break
        if numBoxes == 2:
            return [direction1, direction2]
        else:
            return direction1
    decisions = mainLoop()
    cv.destroyAllWindows()

    return decisions

try:
    def publish():
        broker = "192.168.1.10"
        port = 1883
        def on_publish(client, userdata, result):
            pass

        client1 = paho.Client("toSAV")
        client1.on_publish = on_publish
        client1.connect(broker, port)

        string = str(decision)
        count = 0
        while True:
            client1.publish('MT280/Group10', string) 
            print(f'data sent {string}')
            sleep(0.5)
            count += 1
            if count == 20:
                break
    decision = MV()
    publish()
    # decision = MV(colour)
    # publish()
except:
    pass
