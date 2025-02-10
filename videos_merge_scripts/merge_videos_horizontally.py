# code for joining two videos horizontally

import cv2
import numpy as np

def combine_videos(video1_path, video2_path, output_path):
    # Read the input videos
    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    # Get the properties of the videos
    width1 = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = video1.get(cv2.CAP_PROP_FPS)

    width2 = int(video2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(video2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps2 = video2.get(cv2.CAP_PROP_FPS)

    print(f"stack4 : video1 (width x height) : {width1} x {height1}")
    print(f"stack4 : video2 (width x height) : {width2} x {height2}")

    # Choose the minimum height of the two videos
    min_height = min(height1, height2)

    # Create the VideoWriter object
    output_width = width1 + width2
    output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps1, (output_width, min_height))

    while True:
        # Read frames from both videos
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()

        # Break the loop if either video reaches the end
        if not ret1 or not ret2:
            break

        # Resize frames to the minimum height
        frame1 = cv2.resize(frame1, (int(width1 * min_height / height1), min_height))
        frame2 = cv2.resize(frame2, (int(width2 * min_height / height2), min_height))

        # Combine frames horizontally
        combined_frame = np.hstack((frame1, frame2))

        # Write the combined frame to the output video
        output.write(combined_frame)

    # Release video capture and writer objects
    video1.release()
    video2.release()
    # output.release()

    print(f"Videos combined successfully. Output saved to {output_path}")

# Example usage
# video1_path = "input_videos/1920x1080.mp4"
video1_path = "input_videos/360x1080.mp4"
video2_path = "input_videos/1920x1080.mp4"
output_path = 'output9.mp4'
# video1_path = "resized_main_video1.mp4"
# video1_path = "resized_main_video2.mp4"
# video2_path = "input_videos/1920x1080.mp4"

combine_videos(video1_path, video2_path, output_path)
