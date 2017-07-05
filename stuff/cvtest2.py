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

	blue = [0,100]#cv2.meanStdDev(blue)
	green = [0,100]#cv2.meanStdDev(green)
	red = [0,140]#cv2.meanStdDev(red)
	#print blue, green, red

	blue1 = color[0]#0
	green1 = color[1]#0
	red1 = color[2]#220
	smallest = None
	largest = None
	image = cv2.inRange(image, np.array([blue1 - blue[1]+1, green1 - green[1]+1, red1 - red[1]+1]),np.array([blue1 + blue[1]-1, green1 + green[1]-1, red1 + red[1]-1]))
	image = np.bitwise_and(orig, image[:,:,np.newaxis])

	cv2.imshow("", image)
	cv2.waitKey(0)
	# for i in range(image.shape[0]):
	# 	for j in range(image.shape[1]):
	# 		if (abs(image[i][j][0]-blue1) < blue[1] and abs(image[i][j][1]-green1) < green[1] and abs(image[i][j][2]-red1) < red[1] ):
	# 			pass

	# 		else:
	# 			image[i][j] = np.array([0, 0, 0])
	kernel = np.ones((3,3))
	image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=10)
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=7)
	

	isum = 0
	jsum = 0
	total = 0
	print image[not np.array_equal(image, np.array([0,0,0]))]
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			if (image[i][j].any()):
				isum += i
				jsum += j
				total += 1
				if (smallest == None or (smallest[0] > i and smallest[1] > j)):
					smallest = [i, j]
				if (largest == None or (largest[0] < i and smallest[1] < j)):
					largest = [i, j]

	print smallest, largest
	print isum, jsum
	output = np.copy(orig)
	radius = math.sqrt((largest[0] - smallest[0])**2 + (largest[1] - smallest[1])**2 )
	print "radius, " , radius
	print isum / total, jsum / total
	cv2.circle(output, (int(jsum / total), int(isum / total)), int(radius/2), np.array([255,255,255]))
	cv2.circle(output, (int(jsum / total), int(isum / total)), int(5), np.array([255,255,255]))
	cv2.imshow("image", output)
	cv2.waitKey(0)



	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = np.copy(gray)#cv2.GaussianBlur(gray, (3, 3), 0)
	edges = cv2.Canny(image, 100, 200)
	blurred_edges = cv2.Canny(image, 100, 200)

	output = np.bitwise_or(output, blurred_edges[:,:,np.newaxis])
	cv2.imshow("images", output)
	cv2.waitKey(0)

	gray = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
	dst = cv2.cornerHarris(gray, 2, 3, 0.04)
	dst = cv2.dilate(dst,None)

	circlearray = np.zeros(orig.shape[:2])
	cv2.circle(circlearray, (int(jsum / total), int(isum / total)), int(radius/2)+10, (1), -1)

	print circlearray.shape, (dst>0.01*dst.max()).shape
	output[np.logical_and(dst>0.01*dst.max(), circlearray)] = [0,255,0]


	cv2.imshow("images", output)
	cv2.waitKey(0)

drawMarkers("/home/rush/Videos/images/block_challenge_3.jpg", (0,0,255))