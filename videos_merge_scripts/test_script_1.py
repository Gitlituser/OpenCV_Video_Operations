# only merging the two videos, enhacing ratio - vertically
# Working fine : see result - output_video.mp4
# This is taking around 15 seconds 20 second main vdo with 10 sec ad

# Here both videos width must be equal 

import cv2

# Load the main video
# main_video = cv2.VideoCapture("input_videos/main_video.mp4")
main_video = cv2.VideoCapture("input_videos/720x1280.mp4")
# main_video = cv2.VideoCapture("compressed_output9.mp4")

# Load the footer video
# footer_video = cv2.VideoCapture("output8.mp4")
footer_video = cv2.VideoCapture("input_videos/720x1080.mp4")

# Get frame dimensions
main_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
main_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
footer_width = int(footer_video.get(cv2.CAP_PROP_FRAME_WIDTH))
footer_height = int(footer_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"mode_cv_code : video1 (width x height) : {main_width} x {main_height}")
print(f"mode_cv_code : video2 (width x height): {footer_width} x {footer_height}")

# Ensure both videos have the same width
if main_width != footer_width:
    print("Error: Both videos must have the same width.")
    exit()

# Calculate the duration of the ad video and the main video
main_fps = main_video.get(cv2.CAP_PROP_FPS)
ad_fps = footer_video.get(cv2.CAP_PROP_FPS)
ad_duration = footer_video.get(cv2.CAP_PROP_FRAME_COUNT) / ad_fps
main_duration = main_video.get(cv2.CAP_PROP_FRAME_COUNT) / main_fps

# Create a combined video with the same dimensions as the main video
combined_video = cv2.VideoWriter("final_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), int(main_fps), (main_width, main_height + footer_height))
# combined_video = cv2.VideoWriter("output_videos/test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), int(main_fps), (main_width, main_height + footer_height))

# Loop until the ad video duration matches or exceeds the main video duration
while ad_duration < main_duration:
    # Read frames from both videos
    ret_main, main_frame = main_video.read()
    ret_footer, footer_frame = footer_video.read()

    if not ret_main:
        print("End of main video.")
        break

    if not ret_footer:
        print("reached end of ad video")
        # If the ad video reaches the end, loop it
        footer_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Concatenate frames vertically
    combined_frame = cv2.vconcat([main_frame, footer_frame])

    # Write the combined frame to the output video
    combined_video.write(combined_frame)

    # Update the duration of the ad video
    ad_duration = footer_video.get(cv2.CAP_PROP_POS_FRAMES) / ad_fps

# Release video captures and writer
main_video.release()
footer_video.release()
combined_video.release()
