import numpy as np
import cv2
import math
import imutils
import tkinter

#Returns largest eye based on the area of the region of interest
def FindLargestEye(eyes):
    areas = []
    for i in range(len(eyes)):
        areas.append(math.pow(eyes[i][2],2))
    largest = areas.index(max(areas))
    return eyes[largest]

#Centroid of contour is found using moments, with the formula:
#Cx = M_10 / M_00
#Cy = M_01 / M_00
#If a centroid can be found, will return the value True, plus the coordinates
#of the centroid.
def FindMiddleOfContour(ct):
    M = cv2.moments(ct)
    if M['m00'] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return True, cX, cY
    return False, 0, 0

#Calculates based on counterclockwise movement around the origin
def CalculateAngle(p1, p2):
    ang1 = np.arctan2(*p1[::])
    ang2 = np.arctan2(*p2[::])
    return np.rad2deg(ang1 - ang2)

#Print statement based on the calculated degree
def GetDirection(point1, point2):
    degrees = math.degrees(CalculateAngle(point1, point2))
    degrees %= 360
    if degrees <= 45 or degrees >= 315:
        return "Right"
    elif degrees <= 135 and degrees > 45:
        return "Up"
    elif degrees <= 225 and degrees > 135:
        return "Left"
    elif degrees < 315 and degrees > 225:
        return "Down"
    else:
        return "-"

def EyeTrackingPainter(input, debug):

    #White Canvas creation using Tkinter:
    c_height = 400
    c_width = 400
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, bg="white", height=c_height, width=c_width)
    canvas.pack()

    if input == '1':
        cap = cv2.VideoCapture("SyntheticGazesDataset.mp4")
    elif input == '2':
        cap = cv2.VideoCapture("WebcamDemonstration.mp4")
    elif input == '3':
        print("Please wait while the webcam is loaded...")
        cap = cv2.VideoCapture(0)
    else:
        return

    #Load haar cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Facial detection using haar cascade
        faces = face_cascade.detectMultiScale(gray, 1.1, 15)

        for (x,y,w,h) in faces:

            #Only look above the nose for eyes
            h = h//2

            #Find regions of interest according to the face classifier
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            #Eyes detection using haar cascade
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 15)

            if (len(eyes) > 0):
                #Measure for biggest eye, only use one to limit painting confusion
                #Biggest eye is based on the AREA of the surrounding box
                largestEye = FindLargestEye(eyes)

                #Grab the coordinates of the largest eye: x, y, width, height
                ex, ey, ew, eh = largestEye[0], largestEye[1], largestEye[2], largestEye[3]

                #Draw a rectangle on the frame around the largest detected eye
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0,255,0), 5)

                #Re-computes region of interest for pupil detection
                roi_gray = roi_gray[ey:ey+eh, ex:ex+ew]

                #Contours preparation for pupil detection: first blur to get rid of noise,
                #then use a binary threshold to isolate dark areas
                roi_gray = cv2.GaussianBlur(roi_gray, (5,5), 0)
                _, threshold = cv2.threshold(roi_gray, 50, 255, cv2.THRESH_BINARY_INV)

                #Finds the contours (blobs) within the thresholded image
                contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                if len(contours) > 0:

                    #Only look at the largest contour found, others contours will
                    #be noise
                    contour = max(contours, key = cv2.contourArea)

                    #Finds center of contour based on contour Moments
                    foundCentroid, cX, cY = FindMiddleOfContour(contour)
                    if (foundCentroid):
                        cv2.circle(roi_color, (cX + ex, cY + ey), 7, (0, 0, 255), -1)
                        pupil_location = (ew-cX, eh-cY)
                        eye_location = (0, 0)
                        if (debug == '1'):
                            print(GetDirection(pupil_location, eye_location))
                        #Calculates drawing point on canvas based on the location
                        #of the pupil within the eye frame.
                        #This is a percentage, which gets multiplied by the canvas
                        #dimensions to find an accurate location within the canvas
                        canvas_location = (cX / ew * c_width, cY / eh * c_height)
                        canvas.create_rectangle(canvas_location[0], canvas_location[1], canvas_location[0] + 1, canvas_location[1] + 1)
                        canvas.pack()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break
        root.update() #Draw next canvas frame
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Welcome to the Eye-Tracking Painter application.")
    print("NOTE: Pressing 'q' will terminate the program.\n")
    print("To use debug mode (to see angle of points), type '1'")
    print("otherwise, type '0'")
    debugMode = input("Enter a value: ")
    print("To use the supplied input named 'SyntheticGazesDataset.mp4', type '1'")
    print("To use the supplied input named 'WebcamDemonstration.mp4', type '2'")
    print("To capture input from your webcam, type '3'")
    captureType = input("Enter a value: ")
    EyeTrackingPainter(captureType, debugMode)
main()
