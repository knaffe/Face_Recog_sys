'''

Date : 2017-4-21
Author : Chilam
Application: the class for saving key event into video clip file

'''
# import the necessary packages
from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2
 
class KeyClipWriter:
	def __init__(self, bufSize=64, timeout=1.0):
		# store the maximum buffer size of frames to be kept
		# in memory along with the sleep timeout during threading
		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		# bufSize : The maximum number of frames to be keep cached in an in-memory buffer
		# timeout : An integer representing the number of seconds to sleep for when 
		#           (1) writing video clips to file and 
		#           (2) there are no frames ready to be written.
		'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		self.bufSize = bufSize
		self.timeout = timeout
        
		# initialize the buffer of frames, queue of frames that
		# need to be written to file, video writer, writer thread,
		# and boolean indicating whether recording has started or not
		'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		# frames : A buffer used to a store a maximum of bufSize frames 
		#          that have been most recently read from the video stream.
		#   Q    : A “first in, first out” (FIFO) Python Queue data structure used to hold frames 
		#          that are awaiting to be written to video file.
		# writer : An instantiation of the cv2.VideoWriter class 
		#          used to actually write frames to the output video file.
		# thread : A Python Thread  instance 
		#          that we’ll use when writing videos to file (to avoid costly I/O latency delays).
		# recording : Boolean value indicating whether or not we are in “recording mode”.
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		self.frames = deque(maxlen=bufSize)
		self.Q = None
		self.writer = None
		self.thread = None
		self.recording = False
    
    # update mode---update the frames
	def update(self, frame):
		# update the frames buffer
		# take this frame read from our video and store it in our "frames"
		self.frames.appendleft(frame)
        # if we are recording, update the queue as well
        if self.recording:
        	self.Q.put(frame)
    
    # start mode
	def start(self, outputPath, fourcc, fps):
		# indicate that we are recording, start the video writer,
		# and initialize the queue of frames that need to be written
		# to the video file
		self.recording = True
		self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
			(self.frames[0].shape[1], self.frames[0].shape[0]), True)
		# initialize our Quene used to store the frames readlly to be written to file
		self.Q = Queue()
 
		# loop over the frames in the deque structure and add them
		# to the queue
		for i in range(len(self.frames), 0, -1):
			self.Q.put(self.frames[i - 1])
 
		# start a thread write frames to the video file
		self.thread = Thread(target=self.write, args=())
		self.thread.daemon = True
		self.thread.start()


		