--------------------------------------------------------------------
project.py
Dependencies:
	OpenCV (python)
	Python3
	numpy
	imutils
	tkinter
Setup:

Simply run the program on the command line using 'python3 ./project.py'

Upon running, you will be given a few options:
	#1: Debug mode - 0 is off, 1 is on
	#2: Video input type - 1 is SyntheticGazesDataset.mp4
			       2 is WebcamDemonstration.mp4
			       3 is loading your webcam (live footage)

Debug mode will display the direction that the face in the input data
is currently looking (Up, Down, Left, Right).

Feel free to use your own input video, the name of the video must be
either 'SyntheticGazesDataset.mp4' or 'WebcamDemonstration.mp4'
--------------------------------------------------------------------