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

	if (graph):
		# configuring graph for plotting
		plt.figure(figsize=(15,8))
		plt.axis([0, video.n_frames, 0, height])
		plt.grid(True)

	if (save_data):
		file = open("data.csv", 'w', newline="")
		writer = csv.writer(file)

	for frame_count in range(0, video.n_frames-1):
		# Get next frame in the video
		image = video.get_frame()
		image = Image.resize(image, factor)
		#print(image.shape[0])
		#print(image.shape[1])

		# Display Original Frame from the video
		if (display):
			cv2.imshow("1. Original Video", image)

		alg1_image = np.copy(image)
		signal_list = []
		Image.column_signal(alg1_image, signal_list)
		temp = np.copy(signal_list)
		Image.draw_line(alg1_image, signal_list, 1)
		square_wave = Image.square_wave(signal_list[0], 30)
		for column in range(0, len(signal_list)):
			signal_list[column] = Image.convolve(signal_list[column], square_wave)
		Image.draw_line(alg1_image, signal_list, 0)

		# Display Frame from Column Signal Algorithm
		if (display):
			cv2.imshow("2. Column Signal Algorithm", alg1_image)

		alg2_image = np.copy(image)
		signal = []
		Image.row_sum(alg2_image, signal)
		Image.horiz_line(alg2_image, signal, 1)
		#square_wave = Image.square_wave(signal, alg2_image.shape[1])
		#Image.horiz_line(alg2_image, signal, 0, square_wave)
		# Display Frame from Row Signal Algorithm
		if (display):
			cv2.imshow("3. Row Sum Algorithm", alg2_image)

		# # Display the frame after edge detection has been applied to it
		# edge_image = Image.detect_edges(image)
		# if (display):
		# 	cv2.imshow("2. Edge-Detected Video", edge_image)
        #
		# # Display the frame with all lines detected
		# line_image = Image.detect_lines(np.copy(image), np.copy(edge_image))
		# if (display):
		# 	cv2.imshow("3. Line-Detected Image", line_image)
        #
		# # Display the frame with filtered lines detected
		# line_list, line_coords = Image.detect_lane_lines(image, edge_image, line_list, line_coords, frame_count, 5)
		# if (display):
		# 	cv2.imshow("4. Final Image", image)
        #
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

		time.sleep(0)

		# To end the process, click on any of the display windows and press "q" on the keyboard.
		if cv2.waitKey(25) & 0xFF == ord('q'):
				video.file.release()
				cv2.destroyAllWindows()
				break

	if (save_data):
		print("Finished Writing!\n")
		file.close()

	if (graph):
		plt.show()

if __name__ == '__main__':
	main()

