import cv2

# Load the main video
main_video = cv2.VideoCapture("input_videos/main_video.mp4")

# Load the footer video
footer_video = cv2.VideoCapture("input_videos/ad_video.mp4")

# Get frame dimensions
main_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
main_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
footer_width = int(footer_video.get(cv2.CAP_PROP_FRAME_WIDTH))
footer_height = int(footer_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Ensure both videos have the same width
if main_width != footer_width:
    print("Error: Both videos must have the same width.")
    exit()

# Resize main video to 1920x720
target_width = 1920
target_height = 720
resized_main_video = cv2.VideoWriter("combined_video5.mp4", cv2.VideoWriter_fourcc(*"mp4v"), int(main_video.get(cv2.CAP_PROP_FPS)), (target_width, target_height))

# Loop through main video frames and resize
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

# Now, load the resized main video
resized_main_video = cv2.VideoCapture("resized_main_video.mp4")

# Create a combined video with the same dimensions as the resized main video
combined_video = cv2.VideoWriter("combined_video4.mp4", cv2.VideoWriter_fourcc(*"mp4v"), int(main_video.get(cv2.CAP_PROP_FPS)), (target_width, target_height + footer_height))

# Loop until the ad video duration matches or exceeds the main video duration
while True:
    # Read frames from both videos
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
