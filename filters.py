import cv2
import numpy as np
import time



def scale(frame, percentage):
    width = int(frame.shape[1] * percentage / 100)
    height = int(frame.shape[0] * percentage / 100)
    frame2 = (width, height)
    resize = cv2.resize(frame, frame2)
    return resize

# perspective function to get a bird's eye view
def perspective(video):
    pts1 = np.float32([[220, 300], [30, 720], [320, 300], [480, 720]])
    pts2 = np.float32([[0, 0], [0, 960], [540, 0], [540, 960]])
    trans = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(video, trans, (540, 960))
    return dst

def filtering_knn(video):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    knn = cv2.createBackgroundSubtractorKNN()


    # Applying knn filter for backgrounds
    mask = knn.apply(video, None, 0.01)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    # Dilate to merge adjacent blobs
    dilation = cv2.dilate(opening, kernel, iterations=2)
    # threshold
    # gray5 = cv2.cvtColor(dilation, cv2.COLOR_BGR2GRAY)
    __, th = cv2.threshold(dilation, 0, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
    # erode = cv2.erode(mask,None,iterations=4)
    # _, comp = cv2.connectedComponents(th)
    imfill = th.copy()
    height, weight = th.shape[:2]
    mask = np.zeros((height + 2, weight + 2), np.uint8)
    cv2.floodFill(imfill, mask, (0, 0), 255);
    imfill_inv = cv2.bitwise_not(imfill)
    filled_img = th | imfill_inv
    # eroding to get rid of the noise
    erode = cv2.erode(filled_img, None, iterations=4)
    return erode