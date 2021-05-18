import numpy as np
import cv2
import cv2.aruco as aruco
import glob
from datetime import datetime
cap = cv2.VideoCapture(0)
marker_length = 0.1

focal = 650
width, height = 640,480
mtx = np.array([[  focal,   0.00000000e+00,   width//2],
       [  0.00000000e+00,   focal,   height//2],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])

dist = np.array([[-0.12481632, -0.00360626,  0.00294025, -0.00138677,  0.52909508]])


###------------------ ARUCO TRACKER ---------------------------
detections = 0
def get_shot():
    ret, frame = cap.read()
    print(frame.shape)
    # operations on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):

        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, marker_length, mtx, dist)
        #(rvec-tvec).any() # get rid of that nasty numpy value array error
        if rvec is None:
            return
        for coor in range(rvec.shape[0]):
            
            for i in range(0, ids.size):
                # draw axis for the aruco markers
                #print(tvec[i])
                cv2.putText(frame, "tvec" + "{0:.2f}".format(tvec[i][0][0])+" "+ "{0:.2f}".format(tvec[i][0][1])+ " " +"{0:.2f}".format(tvec[i][0][2]),(0,32), font, 1, (0,255,0),2,cv2.LINE_AA)
                #cv2.imwrite('raw/'+str(detections) + "good.png", frame)
                aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
                #cv2.imwrite('axis/'+str(detections) + "with_axis.png", frame)
        
        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)


        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0])+', '
            offset = i*30
            cv2.putText(frame, "Id: " + strg, (0+offset,64), font, 1, (0,255,0),2,cv2.LINE_AA)
        yield ids.flatten().tolist()

    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    # display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass

while (True):
    ids = get_shot()
    print("ids", *ids)