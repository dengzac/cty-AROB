import cv2
import numpy as np

def callback():
	
image = cv2.imread("/home/rush/")
cv2.namedWindow("window", 1)

cv2.createTrackbar("Rmin", "window",0,255,callback)

