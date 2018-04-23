import cv2
from math import sin, cos, radians
import numpy as np

cap = cv2.VideoCapture(0)
# camera =  cv2.VideoCapture(0)
face = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 5, 
    # 'minSize': (50, 50), 
    # 'flags': cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
}

def rotate_image(image, angle):
    if angle == 0: return image
    # print("checked for shape".format(image.shape))
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[:,0] - img.shape[1]*0.4
    y = pos[:,1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return np.array((newx, newy, pos[:,2], pos[:,3]), int).T

#    x1 = pos1[0] - img.shape[1]*0.4
#    y1 = pos1[1] - img.shape[0]*0.4
#    newx1 = x1*cos(radians(angle)) + y1*sin(radians(angle)) + img.shape[1]*0.4
#    newy1 = -x1*sin(radians(angle)) + y1*cos(radians(angle)) + img.shape[0]*0.4
#    return int(newx), int(newy), pos[2], pos[3]


while True:
    # ret, img = camera.read()
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for angle in [0, -30, 30]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        print("before",len(detected))
        
        
        if len(detected):
            detected = rotate_point(detected, img, -angle)
            print("after", len(detected))
            break
        
       
        

    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow('facedetect', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# cv2.destroyWindow("facedetect")