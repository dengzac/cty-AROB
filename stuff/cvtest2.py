import cv2
import numpy as np
import math

def drawMarkers(filename, color):
	image = cv2.imread(filename)#"/home/rush/Pictures/chessboard.png")
	orig = np.copy(image)
	print image.shape
	red = image[:, :, 2]
	blue = image[:, :, 0]
	green = image[:, :, 1]
	sum = 0

	blue = cv2.meanStdDev(blue)
	green = cv2.meanStdDev(green)
	red = cv2.meanStdDev(red)
	print blue, green, red

	blue1 = color[0]#0
	green1 = color[1]#0
	red1 = color[2]#220
	smallest = None
	largest = None
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			if (abs(image[i][j][0]-blue1) < blue[1] and abs(image[i][j][1]-green1) < green[1] and abs(image[i][j][2]-red1) < red[1] ):
				pass

			else:
				image[i][j] = np.array([0, 0, 0])
	kernel = np.ones((3,3))
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
	image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)

	isum = 0
	jsum = 0
	total = 0
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			if not (np.array_equal(image[i][j],np.array([0,0,0]))):
				isum += i
				jsum += j
				total += 1
				if (smallest == None or (smallest[0] > i and smallest[1] > j)):
					smallest = [i, j]
				if (largest == None or (largest[0] < i and smallest[1] < j)):
					largest = [i, j]

	print smallest, largest
	print isum, jsum
	output = np.copy(image)
	radius = math.sqrt((largest[0] - smallest[0])**2 + (largest[1] - smallest[1])**2 )
	print "radius, " , radius
	print isum / total, jsum / total
	cv2.circle(output, (int(isum / total), int(jsum / total)), int(radius/2), np.array([255,255,255]))
	cv2.imshow("image", output)
	cv2.waitKey(0)



	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	edges = cv2.Canny(image, 100, 200)
	blurred_edges = cv2.Canny(blurred, 100, 200)

	output = np.bitwise_or(output, blurred_edges[:,:,np.newaxis])
	cv2.imshow("images", output)
	cv2.waitKey(0)

	gray = np.float32(cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY))
	dst = cv2.cornerHarris(gray, 2, 3, 0.04)
	dst = cv2.dilate(dst,None)
	output[dst>0.01*dst.max()] = [0,0,255]


	cv2.imshow("images", output)
	cv2.waitKey(0)

drawMarkers("/home/rush/Pictures/blocks.jpg", (0,0,220))