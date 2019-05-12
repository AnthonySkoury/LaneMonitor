import time
import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt

from video_object import Video
import image_processing as Image

# Must have this video file in the same directory"
file_name = "GP010020.MP4"

# Switches
graph = False
save_data = False
display = True

if (graph):
	print("Graphing Results!")
if (save_data):
	print("Saving Data at the end!")
if (display):
	print("Displaying Frames!")

def main():
	factor = 0.3

	# Reading Video
	video = Video(file_name)
	global height, width, shape
	height, width, shape = video.get_frame().shape

	# Memory of previous lines
	line_list = []
	line_coords = []
	line_distances = []

	# if (graph):
	# 	# configuring graph for plotting
	# 	plt.figure(figsize=(15,8))
	# 	plt.axis([0, video.n_frames, 0, height])
	# 	plt.grid(True)
	#
	# if (save_data):
	# 	file = open("data.csv", 'w', newline="")
	# 	writer = csv.writer(file)

	#for frame_count in range(0, video.n_frames-1):
	max1=0
	max2=0

	count1=1
	count2=1

	for frame_count in range(0, video.n_frames-1):
		# Get next frame in the video
		image = video.get_frame()
		image = Image.resize(image, factor)
		# print(image.shape)
		# print(image[0][0])
		# x = (float(image[0][0][0])/255+float(image[0][0][1])/255+float(image[0][0][2])/255)/3
		# print(x)

		# #code needed for column algorithm
		# signal_list = []
		#
		# Image.column_signal(image, signal_list)
		# temp = np.copy(signal_list)
		# Image.draw_line(image, signal_list, 1)
		# square_wave = Image.square_wave(signal_list[0], 30)
		# for column in range(0, len(signal_list)):
		# 	signal_list[column] = Image.convolve(signal_list[column], square_wave)
		# Image.draw_line(image, signal_list, 0)
		#
		# #cv2.imshow('image', image)
		# #cv2.waitKey(0)
		# #new_signal = Image.convolve(signal_list[100])
		#
		# # print(len(new_signal))
		# # print(new_signal)
		# # #new_signal = np.array(new_signal)
		# # print(np.amax(new_signal))
		# # result = int(np.where(new_signal == np.amax(new_signal)))
		# # print(int(result[0]))
		# # print(len(new_signal))
		#
		# # for i in range(0, image.shape[1]):
		# # 	signal = image[:, i]
		# # 	print(signal)
		# # 	csignal = Image.convolve(signal)
		# # print(csignal)
		# #end code needed

		#code needed for row algorithm

		# signal = []
		#
		# Image.row_sum(image, signal)
		# temp = np.copy(signal)
		# if frame_count== 0:
		# 	max1 = Image.horiz_line(image, temp, 1, frame_count)
		# else:
		# 	max1 = Image.horiz_line(image, temp, 1, frame_count, 0, max1)
		# square_wave = Image.square_wave(signal, 30)
		# if frame_count == 0:
		# 	max2 = Image.horiz_line(image, signal, 0, frame_count, square_wave)
		# else:
		# 	max2 = Image.horiz_line(image, signal, 0, frame_count, square_wave, max2)
		#
		signal = []

		Image.row_sum(image, signal)
		temp = np.copy(signal)
		max_list_conv = []
		max_list = []

		count1, max_list = Image.horiz_line(image, temp, max_list, 1, count1)
		square_wave = Image.square_wave(signal, 30)
		count2, max_list_conv = Image.horiz_line(image, signal, max_list_conv, 0, count2, square_wave)
		#end code needed for row algorithm

		# Display Original Frame from the video
		#if (display):
		cv2.imshow("1. Original Video", image)


		# # Calculating the distance from the car to the lane (in pixels)
		# for line_coord in line_coords:
		# 	line_distances.append(line_coord[1])	# y1
		# 	line_distances.append(line_coord[3])	# y2
		# try:
		# 	lane_distance = (height - int(max(line_distances)/factor))
		# 	print("Frame [{}]: Distance from car to lane line: {}" .format(frame_count, lane_distance))
		# 	line_distances.clear()
		# 	if (save_data):
		# 		writer.writerow([frame_count, lane_distance])
		# 	if (graph):
		# 		# plotting lane distance of current frame
		# 		plt.scatter(frame_count, lane_distance)
		# 		plt.pause(0.05)
		# except ValueError:
		# 	print("No Lines Found!")
		#
		# time.sleep(0)

		# To end the process, click on any of the display windows and press "q" on the keyboard.
		if cv2.waitKey(25) & 0xFF == ord('q'):
				video.file.release()
				cv2.destroyAllWindows()
				break

	if (save_data):
		print("Finished Writing!\n")
		#file.close()

	if (graph):
		plt.show()

if __name__ == '__main__':
	main()
