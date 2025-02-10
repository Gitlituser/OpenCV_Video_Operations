# mod3_cv.py - vertaical compress and merge


import cv2
import os

main_video = cv2.VideoCapture("compressed_output9.mp4")

# Load the footer video
# footer_video = cv2.VideoCapture("output8.mp4")
# footer_video = cv2.VideoCapture("input_videos/ad_video.mp4")
# Load the main video
# main_video = cv2.VideoCapture("input_videos/1920x1080.mp4")

# # Load the footer video (ad video)
footer_video = cv2.VideoCapture("input_videos/org_ad.mp4")

rszd_main_vdo = "resized_main_video1.mp4"
rszd_footer_vdo = "resized_footer_video1.mp4"
edited_video = "new_edited_video3.mp4"


# Reduce the height of the main video by 20% - 0.8 | 40% - 0.6
percentage_decrease = 0.5

# Get frame dimensions
main_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
main_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
footer_width = int(footer_video.get(cv2.CAP_PROP_FRAME_WIDTH))
footer_height = int(footer_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Adjust the width of the main video to match the ad video
target_width = footer_width
target_height = int(main_height * percentage_decrease)  

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

# Release main video capture and writer
main_video.release()
resized_main_video.release()

# ------------ resized_main_video released here.

# Now, load the resized main video
resized_main_video = cv2.VideoCapture(rszd_main_vdo)

# Create a combined video with the same width as the ad video
combined_video = cv2.VideoWriter(edited_video, cv2.VideoWriter_fourcc(*"mp4v"), int(resized_main_video.get(cv2.CAP_PROP_FPS)), (target_width, target_height + footer_height))

# Loop through frames of the resized main video and concatenate with the ad video
while True:
    ret_resized_main, resized_main_frame = resized_main_video.read()
    ret_footer, footer_frame = footer_video.read()

    if not ret_resized_main:
        print("End of resized main video.")
        break

    if not ret_footer:
        # If the ad video reaches the end, loop it
        footer_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Concatenate frames vertically
    combined_frame = cv2.vconcat([resized_main_frame, footer_frame])

    # Write the combined frame to the output video
    combined_video.write(combined_frame)

# Release video captures and writer
resized_main_video.release()
footer_video.release()
combined_video.release()
# os.remove('resized_main_video1.mp4')