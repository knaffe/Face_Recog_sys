#!/usr/bin/python3
# use camera to read and write video

import cv2

# open the camera,  you can find the camera ID in  /dev/
#capture = cv2.VideoCapture(0)

# open the video file
capture = cv2.VideoCapture("./test1.mp4")

# check whether the camera is opened
while(not capture.isOpened()):
	print("camera can't be opened!!")

#将capture保存为motion-jpeg,cv_fourcc为保存格式
size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

# if you set the FPS as the input video, the saved video will soo fater
fps = capture.get(cv2.CAP_PROP_FPS)
#fps = 10
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video=cv2.VideoWriter("VideoTest.avi",  fourcc, fps, size)


num = 0

# raed the frames in a loop, process and save it
while True:
	ret, img = capture.read()
	#write the frame into avi video file
	video.write(img)
	cv2.imshow('Video', img)
	print(capture.get(cv2.CAP_PROP_FPS))
	key = cv2.waitKey(100)
	cv2.imwrite('%s.jpg' %(str(num)), img)
	num = num + 1
	if key ==ord('q'):
		break
# save the video file
video.release()
# close the camera
capture.release()
cv2.destroyAllWindows()