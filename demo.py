import face_recognition
import numpy as np
import cv2
import glob
import random
import string
import os
import math
import argparse


os.system('cls' if os.name=='nt' else 'clear')

parser = argparse.ArgumentParser();
parser.add_argument('-i', type=str, help='Image of target face to scan for.', required=True)
parser.add_argument('-v', type=str, help='Video to process', required=True)
parser.add_argument('-t', type=float, help='Tolerance of face detection, lower is stricter. (0.1-1.0)', default=0.6)
parser.add_argument('-f', type=int, help='Amount of frames per second to extract.', default=25)
parser.add_argument('-n', type=int, help='Number of frames with target face to save from each vid.', default=500)
parser.add_argument('-s', type=int, help='Minimum KB size of images to keep in the faceset.', default=32)
args = vars(parser.parse_args())

if args['t'] > 1.0:
	args['t'] = 1.0
elif args['t'] < 0.1:
	args['t'] = 0.1

min_KB = args['s']
tol = args['t']
xfps = args['f']
targfname = args['i']
vid_dir = args['v']
faces_from_each_video = args['n']
'''
if xfps < 25:
	xfps = 25
'''
if faces_from_each_video < 1:
	faces_from_each_video = 500

if min_KB < 1:
	min_KB = 32

print("Target filename: " + targfname + ".")
print("Video input directory: " + vid_dir + ".")
print("Tolerance: " + str(tol) + ".")
print("Number of confirmed faces saved from each video: " + str(faces_from_each_video) + ".")

if(cv2.ocl.haveOpenCL()):
	cv2.ocl.setUseOpenCL(True)
	print("Using OpenCL: " + str(cv2.ocl.useOpenCL()) + ".")

target_image = face_recognition.load_image_file(targfname)
outdir = str(str(os.path.splitext(targfname)[0]) + "_output");
scanned_vids = str(str(os.path.splitext(targfname)[0]) + "_scanned_vids");
too_small = str(str(os.path.splitext(targfname)[0]) + "_too_small");

#check if output directories already exists, and if not, create it
os.makedirs(outdir, exist_ok=True)
os.makedirs(scanned_vids, exist_ok=True)
os.makedirs(too_small, exist_ok=True)

print("Output directory: " + outdir + ".")
print("Scanned videos will be moved to: " + scanned_vids + ".")

try:
	target_encoding = face_recognition.face_encodings(target_image)[0]
except IndexError:
	print("No face found in target image.")
	raise SystemExit(0)

for i in range(5):
	try:
		vid = random.choice(glob.glob(vid_dir + '*.mp4'))
		print("Now looking at video: " + vid)
		input_video = cv2.VideoCapture(vid)

		framenum = 0
		vidheight = input_video.get(4)
		vidwidth = input_video.get(3)
		vidfps = input_video.get(cv2.CAP_PROP_FPS)
		totalframes = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
		outputsize = 256, 256

		if xfps > vidfps:
			xfps = vidfps

		print("Frame Width: " + str(vidwidth) + ", Height: " + str(vidheight) + ".")

		known_faces = [
			target_encoding
		]

		def random_string(length):
			return ''.join(random.choice(string.ascii_letters) for m in range(length))

		#switch to output directory
		os.chdir(str(os.path.splitext(targfname)[0]) + "_output")

		written = 1
		while(input_video.isOpened()):
			input_video.set(1, (framenum + (vidfps/xfps)))
			framenum += vidfps/xfps
			ret, frame = input_video.read()

			if not ret:
				break

			percentage = (framenum/totalframes)*100
			print("Checking frame " + str(int(framenum)) + "/" + str(int(totalframes)) + str(" (%.2f%%)" % percentage))
			
			rgb_frame = frame[:, :, ::-1]
			
			face_locations = face_recognition.face_locations(rgb_frame)
			face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
			
			for fenc, floc in zip(face_encodings, face_locations):
				istarget = face_recognition.compare_faces(known_faces, fenc, tolerance=float(tol))
			
		    	#if the face found matches the target
				if istarget[0]:
					top, right, bottom, left = floc
					facefound = True
					#squaring it up
					if (bottom - top) > (right - left):
						right = left + (bottom - top)
					elif (right - left) > (bottom - top):
						bottom = top + (right - left)
					#calculating the diagonal of the cropped face for rotation purposes
					#diagonal = math.sqrt(2*(bottom - top))
					#padding = diagonal / 2
					#alignment script causes images cropped "too closely" to get a bit fucky, so crop them less severely.
					padding = (bottom - top)/2
					
					if((top - padding >= 0) and (bottom + padding <= vidheight) and (left - padding >= 0) and (right + padding <= vidwidth)):
						croppedframe = frame[int(top - padding):int(bottom + padding), int(left - padding):int(right + padding)]
						#if the image is too small, resize it to outputsize
						cheight, cwidth, cchannels = croppedframe.shape
						if (cheight < 256) or (cwidth < 256):
							croppedframe = cv2.resize(croppedframe, outputsize, interpolation=cv2.INTER_CUBIC)
						print('Writing image ' + str(written) + '.')
						cv2.imwrite(("vid_" + str(i) + random_string(15) + ".jpg"), croppedframe, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
						written += 1
			if percentage > 99.9:
				os.rename(vid, scanned_vids + '/vid' + str(i) + '_' + random_string(5) + '.mp4')
				break
			if written > faces_from_each_video:
				os.rename(vid, scanned_vids + '/vid' + str(i) + '_' + random_string(5) + '.mp4')
				break
		input_video.release()
	except ValueError:
		print ("Scanning videos complete.")
		pass
	except IndexError:
		pass
#Removes images under 32KB
counter = 0
low_quat = min_KB * 1000
for i in (os.listdir(os.getcwd())):
	if(os.path.getsize(i)) < low_quat:
		os.rename(i, too_small + "/too small-" + str(counter) + random_string(15) + ".jpg")
		print ("Moving " + str(i) + " to the too small folder")
		counter += 1


#Remove images with more than one face
print ("Now double checking there is only one face in each photo")
for i in (os.listdir(os.getcwd())):
	# Load the jpg file into a numpy array
	image = face_recognition.load_image_file(i)

	# Find all the faces in the image using a pre-trained convolutional neural network.
	# This method is more accurate than the default HOG model, but it's slower
	# unless you have an nvidia GPU and dlib compiled with CUDA extensions. But if you do,
	# this will use GPU acceleration and perform well.
	# See also: find_faces_in_picture.py
	face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

	print("I found {} face(s) in this photograph.".format(len(face_locations)))

	if not (len(face_locations)) == 1:
		os.remove(i)
		print (str(i) + ' was removed')
