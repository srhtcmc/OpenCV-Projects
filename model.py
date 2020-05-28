import cv2
import numpy as np
import time
from filters import *
#%%
speed = [0,0,0,0,0,0,0,0,0,0]
start_time = time.time()
camera = cv2.VideoCapture("video_file")
# filters to remove the background
knn = cv2.createBackgroundSubtractorKNN()
images = []


while True:
    ret, mov = camera.read()
    # Grayscaling the video
    gray = cv2.cvtColor(mov, cv2.COLOR_BGR2GRAY)
    # if video format is ".mov" activate the code below and deactivate the line 80.
    # rotating the video because .mov type videos starts horizontal
    # gray3 = scale(cv2.rotate(gray,cv2.ROTATE_90_CLOCKWISE), 50)
    # scaling to obtain needed size
    gray3 = scale(gray, 50)
    # sol ust sol alt
    cv2.line(gray3, (220, 300), (30, 720), (255, 0, 0), 2)
    # sağ üst sağ alt
    cv2.line(gray3, (320, 300), (480, 720), (255, 0, 0), 2)
    # sol üst sağ üst
    cv2.line(gray3, (220, 300), (320, 300), (255, 0, 0), 2)
    # sol alt sağ alt
    cv2.line(gray3, (30, 720), (480, 720), (255, 0, 0), 2)
    cv2.imshow("Gray", gray3)
    # lines for visualization
    """
    pers line
    cv2.line(gray3, (205, 350), (40, 710), (255, 0, 0), 2)
    cv2.line(gray3, (345, 350), (485, 710), (255, 0, 0), 2)
    cv2.line(gray3, (205, 350), (345, 350), (255, 0, 0), 2)
    cv2.line(gray3, (40, 710), (485, 710), (255, 0, 0), 2)
    #up
    cv2.line(gray3, (20, 380), (250, 380), (255, 0, 0), 2)
    #down
    cv2.line(gray3, (20, 410), (250, 410), (255, 0, 0), 2)
    #left
    cv2.line(gray3, (20, 380), (20, 410), (255, 0, 0), 2)#right
    cv2.line(gray3, (250, 380), (250, 410), (255, 0, 0), 2)
    """
    pers = perspective(gray3)
    b = scale(pers, 50)
    c = cv2.flip(b, 0)
    #üst çizgiler
    cv2.line(b, (0,20 ), (270, 20), (255, 0, 0), 2)
    cv2.line(b, (0, 60), (270, 60), (255, 0, 0), 2)
    #alt çizciler
    cv2.line(b, (0, 100), (270, 100), (255, 0, 0), 2)
    cv2.line(b, (0, 140), (270, 140), (255, 0, 0), 2)
    cv2.imshow("b", b)
    f1 = filtering_knn(c)
    cv2.imshow("knn", f1)
    connectivity = 4
    output = cv2.connectedComponentsWithStats(f1, connectivity, cv2.CV_32S)
    # number of objects on foreground
    numberOfLabels = output[0]
    # label matrix
    labels = output[1]
    # stat matrix
    stats = output[2]
    # objects centroid matrix
    centroids = output[3]
    if numberOfLabels > 1:
        for i in range(numberOfLabels - 1):
            label = i + 1
            if stats[label, 4] < 600:
                cv2.imshow("b", b)
                break
            height, width = labels.shape[:2]
            labels = np.zeros((height, width), np.uint8)
            labels[labels == label] = 255
            if numberOfLabels > 1:
                left_top_x = stats[label, 0]
                left_top_y = 480-stats[label, 1]
                right_bot_x = stats[label, 0] + stats[label, 2]
                right_bot_y = 480-(stats[label, 1] + stats[label, 3])
                cent_x = int(centroids[label, 0])
                cent_y = 480 - int(centroids[label, 1])
                cv2.rectangle(b, (left_top_x, left_top_y), (right_bot_x,right_bot_y), (255, 255, 255), 2)
                circle1 = cv2.circle(b, (cent_x, cent_y), 10, (0, 0, 0), -1)
                if cent_x > 20 and cent_x < 250 and cent_y > 20 and cent_y < 60:
                    start_time = time.time()
                if cent_x > 20 and cent_x < 250 and cent_y > 100 and cent_y < 140:
                    end_time = time.time()
                    t1 = end_time - start_time
                    speed[label]= int(28.8/t1)
                    print(label, " ",speed[label])
                if cent_x > 20 and cent_x < 250 and cent_y > 190 and cent_y < 400:
                    cv2.putText(b, "%rkm/h" % speed[label], (left_top_x,
                                                             left_top_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 0),2)
                    cv2.imshow("b", b)
    else:
        cv2.imshow("b", b)
    
    cent_x = 0
    cent_y = 0
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()