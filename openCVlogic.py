import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces = 1)
idlist = [22,23,24,26,110,130,157,158,159,160,161,243]
ratioList = []
blinkCount = 0
counter = 0
plotY = LivePlot(640,360,[20,50])
while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img,draw = False)
    if faces:
        #RGB BGR
        face = faces[0]
        for id in idlist:
            cv2.circle(img,face[id],3,(0,0,255),cv2.FILLED)
        eyeTop = face[159]
        eyeBot = face[23]
        eyeLeft = face[130]
        eyeRight = face[243]
        eyeLength, _ = detector.findDistance(eyeTop,eyeBot)
        eyeWidth, _ = detector.findDistance(eyeLeft,eyeRight)
        cv2.line(img,eyeTop,eyeBot,(255,255,0),2)
        cv2.line(img,eyeLeft,eyeRight,(255,255,0),2)
        ratio = (eyeLength/eyeWidth)*100
        ratioList.append(ratio)
        if len(ratioList)>7:
            ratioList.pop(0)
        avgRatio = sum(ratioList)/len(ratioList)
        dynamic_limit = avgRatio *0.9
        if ratio < dynamic_limit and counter == 0:
            blinkCount += 1
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
        cvzone.putTextRect(img,f'Blinks:{blinkCount}',(50,100))
        cvzone.putTextRect(img,f'Avg:{blinkCount}',(50,50))
        print(avgRatio)
        imgPlot = plotY.update(avgRatio)

        img = cv2.resize(img,(640,360))
        imgStack = cvzone.stackImages([img,imgPlot],2,1)
    else:
        imgStack = cvzone.stackImages([img,imgPlot],2,1)
    cv2.imshow("Result",imgStack)
    if cv2.waitKey(1)== ord('q'):
        break