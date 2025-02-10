# compressing main video


import cv2
import os

# Load the main video
main_video = cv2.VideoCapture("output8.mp4")
# main_video = cv2.VideoCapture("input_videos/1920x1080.mp4")

# Load the footer video (ad video)
# footer_video = cv2.VideoCapture("input_videos/720x1280.mp4")

# rszd_main_vdo = "expanded_output8.mp4"
rszd_main_vdo = "compressed_output9.mp4"
# rszd_footer_vdo = ".mp4"
# edited_video = "horizontal_concatenation.mp4"


# Reduce the height of the main video by 20% - 0.8 | 40% - 0.6
# percentage_decrease = 0.8
# percentage_increase = 1.779
percentage_increase = 1.186
# percentage_increase = 1

# Get frame dimensions
main_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
main_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# footer_width = int(footer_video.get(cv2.CAP_PROP_FRAME_WIDTH))
# footer_height = int(footer_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Adjust the width of the main video to match the ad video
# target_width = int(main_width * percentage_decrease)
target_width = int(main_width * percentage_increase)
# target_width = int(footer_width * percentage_decrease) 
target_height = main_height

# Producing resized main_video to the target dimensions
resized_main_video = cv2.VideoWriter(rszd_main_vdo, cv2.VideoWriter_fourcc(*"mp4v"), int(main_video.get(cv2.CAP_PROP_FPS)), (target_width, target_height))
# resized_main_video = cv2.VideoWriter(rszd_footer_vdo, cv2.VideoWriter_fourcc(*"mp4v"), int(footer_video.get(cv2.CAP_PROP_FPS)), (target_width, target_height))

# Loop through frames of the main video and resize
while True:
    ret_main, main_frame = main_video.read()

    if not ret_main:
        print("End of main video.")
        break

    # Resize main frame to target dimensions
    resized_main_frame = cv2.resize(main_frame, (target_width, target_height))

    # Write resized frame to the resized_main_video
    resized_main_video.write(resized_main_frame)


# -------------------- second step of finding size of output video : ------------------------------------


# Release main video capture and writer
main_video.release()
resized_main_video.release()

print ("compressing main video successfull")


# Example usage
# video1_path = "input_videos/1920x1080.mp4"
# video1_path = "input_videos/main_video.mp4"
# video1_path = "expanded_output8.mp4"

# video1_path = "input_videos/ad_video.mp4"
# video1_path = "compressed_output9.mp4"
# video1_path = "output9.mp4"
# video2_path = "input_videos/720x1080.mp4"

# combine_videos(video1_path)
# combine_videos(video1_path, video2_path)
