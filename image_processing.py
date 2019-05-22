import numpy as np
import cv2


#squareWave = np.repeat([0., 1., 0.], len(signal))

#	INPUT: 	Image
#	OUTPUT:	Resized Image
#	DESCRIPTION: Currently set to reduce the size of the input image by a factor of both width and height dimensions.
def resize(src_image, factor):
	return cv2.resize(src_image, (0, 0), fx=factor, fy=factor)

#method 1 column signals

def column_signal(src_image, signal_list):
	#first loop through columns
	for column in range(0, src_image.shape[1]):
		signal = []
		for row in range(0, src_image.shape[0]):
			channel_sum = (float(src_image[row][column][0])/255+float(src_image[row][column][1])/255+float(src_image[row][column][2])/255)
			#channel_sum = (float(src_image[row][column][0])*0.0722+float(src_image[row][column][1])*0.7152+float(src_image[row][column][2])*0.2126)
			signal.append(channel_sum)
		signal_list.append(signal)
	return


def convolve(signal, square_signal):
	#squareWave = np.repeat([0., 1., 0.], len(signal))
	sample_rate = 100
	num_samples = len(signal)
	#wave = np.fromfunction(lambda i: (2 * sample_rate < i) & (i < 3 * sample_rate), (num_samples,)).astype(np.float)
	return np.convolve(signal, square_signal, mode="same")
	#return np.convolve(signal, wave, mode="same")

def plot_max(src_image, signal, column, flag):
	result = np.where(signal == np.amax(signal))
	#print("This is the max of the array : ")
	#print(np.amax(result))
	max = np.amax(result)
	max = int(max)
	#flag being 0 means green line, for convolution method, red line for no convolution, just max
	for i in range(max-1, max+1):
		if flag == 0:
			src_image[i][column][0] = 0
			src_image[i][column][1] = 255
			src_image[i][column][2] = 0
		else:
			src_image[i][column][0] = 0
			src_image[i][column][1] = 0
			src_image[i][column][2] = 255
	return

def draw_line(src_image, signal_list, flag):
	for column in range(0, src_image.shape[1]):
		plot_max(src_image, signal_list[column], column, flag)
	return

def square_wave(signal, lane_width):
	square_signal = []

	for i in range(0, len(signal)):
		if i<lane_width:
			square_signal.append(0)
		elif i<lane_width+(lane_width)/2:
			square_signal.append(-15)
		elif i<lane_width+(lane_width)*(3/2):
			square_signal.append(15)
		elif i<lane_width+(lane_width)*2:
			square_signal.append(-15)
		else:
			square_signal.append(0)
	return square_signal


#method 2 row summing

def row_sum(src_image, signal):
	#sum the pixel values at each row so first loop through row then column
	for row in range(0, src_image.shape[0]):
		channel_sum = 0
		for column in range(0, src_image.shape[1]):
			channel_sum += (float(src_image[row][column][0])+float(src_image[row][column][1])+float(src_image[row][column][2]))/3
		signal.append(channel_sum)
	return

# it1=0
# it2=0
# max_list = []
# max_list_conv = []

# def horiz_line(src_image, signal, max_list1, flag, count, square_signal=""):
# 	global it1
# 	global it2
# 	global max_list
# 	iteration = int((it1+it2)/2)
# 	it1+=1
# 	it2+=1
#
# 	if flag == 0:
# 		signal = convolve(signal, square_signal)
# 	result = np.where(signal == np.amax(signal))
# 	print("This is the max of the array : ")
# 	print(np.amax(result))
# 	max = np.amax(result)
# 	max = int(max)
# 	max_list.append(int(max))
# 	print("This is the iteration "+ str(iteration))
# 	print(max_list)
# 	if iteration > 0:
# 		if max_list[iteration] > max_list[iteration-1]+40 or max_list[iteration] < max_list[iteration-1]-40:
# 			if count%2==0:
# 				draw_horiz_line(src_image, max, flag)
# 			else:
# 				count+=1
# 				max_list[iteration] = max_list[iteration-1]
# 				max = max_list[iteration-1]
# 				draw_horiz_line(src_image, max, flag)
#
# 	else:
# 		draw_horiz_line(src_image, max, flag)
# 	return count, max_list


def horiz_line(src_image, signal, flag, square_signal=""):
	if flag == 0:
		signal = convolve(signal, square_signal)
	result = np.where(signal == np.amax(signal))
	max = np.amax(result)
	max = int(max)
	#max_list.append(int(max))
	draw_horiz_line(src_image, max, flag)
	return


def draw_horiz_line(src_image, max, flag):
	if flag == 0:
		for column in range(0, src_image.shape[1]):
			src_image[max][column][0] = 0
			src_image[max][column][1] = 255
			src_image[max][column][2] = 0
	else:
		for column in range(0, src_image.shape[1]):
			src_image[max][column][0] = 0
			src_image[max][column][1] = 0
			src_image[max][column][2] = 255
	return