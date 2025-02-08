from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2 
import sys



type = cv2.aruco.DICT_6X6_50

dictionary = cv2.aruco.getPredefinedDictionary(type)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 1000 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)
    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucoDict, parameters=arucoParams)
    if len(corners) > 0 :
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
	    # extract the marker corners (which are always returned
	    # in top-left, top-right, bottom-right, and bottom-left
	    # order)
	    corners = markerCorner.reshape((4, 2))
	    (topLeft, topRight, bottomRight, bottomLeft) = corners
	    # convert each of the (x, y)-coordinate pairs to integers
	    topRight = (int(topRight[0]), int(topRight[1]))
	    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	    topLeft = (int(topLeft[0]), int(topLeft[1]))
                
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
	    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
	    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
	    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
	    # compute and draw the center (x, y)-coordinates of the
	    # ArUco marker
	    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
	    # draw the ArUco marker ID on the frame
	    cv2.putText(frame, str(markerID),(topLeft[0], topLeft[1] - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
	    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
	break
    # do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
            
