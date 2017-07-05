import cv2
import numpy as np
import random
import math

image = cv2.imread("/home/rush/Pictures/blocks.jpg")
print image
cv2.imshow("image", image)
#v2.waitKey(0)

def ROI(image, x, y, h, w):
	return image[y:y+h, x:x+w]

print image.shape[1]

red = image[:, :, 2]
blue = image[:, :, 0]
green = image[:, :, 1]
sum = 0
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		pass
		#blue = np.append(blue, image[i][j][0])
		#green= np.append(green, image[i][j][1])
		#red= np.append(red, image[i][j][2])
		# if image[i][j][2] > 150 and image[i][j][0] < 100 and image[i][j][1] < 40:
		# 	pass
		# else:
		# 	image[i][j] = np.array([0,0,0])
		# for k in range(image.shape[2]):

		# 	image[i][j][k] = image[i][j][k] if k==0 else 0
		# 	#image[i][j][k] = int(random.randint(0, 255)) #(255 - image[i][j][k] + int(random.random()*100))%256
		# 	sum += image[i, j, k]
blue = cv2.meanStdDev(blue)
green = cv2.meanStdDev(green)
red = cv2.meanStdDev(red)
print blue, green, red

blue1 = 0
green1 = 0
red1 = 220
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
radius = math.sqrt((largest[0] - smallest[0])**2 + (largest[1] - smallest[1])**2 )
print "radius, " , radius
print isum / total, jsum / total
cv2.circle(image, (int(isum / total), int(jsum / total)), int(radius/2), np.array([255,255,255]))
# image = np.sort(image, 2)
# image = np.sort(image, 0)
# image = np.sort(image, 1)
# image = np.sort(image, 2)
# ball = ROI(image, 49, 380, 64, 62)#image[380:444,49:111]
# #image[0:64, 0:62] = ball
#cv2.imshow("image", ball)
#cv2.waitKey(0)
#print ball

#image[:][50:100]  = np.zeros((50, 370, 3))
#cv2.rectangle(image, (0,0), (100,100), (0,0,0), -1)
cv2.imshow("image", image)
cv2.waitKey(0)