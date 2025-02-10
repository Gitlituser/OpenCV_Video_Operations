# This code suddenly showing transition of video being compressed.

import cv2
import numpy as np

def compress_and_expand_video(input_path, output_path, compression_factor, transition_duration=5):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate new dimensions after compression
    new_width = int(width * compression_factor)
    new_height = int(height * compression_factor)

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Calculate frames for compression and expansion phases
    compression_frames = int(transition_duration * fps)
    expansion_frames = compression_frames

    # Perform compression
    for frame_num in range(compression_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to compressed dimensions
        compressed_frame = cv2.resize(frame, (new_width, new_height))

        # Create a black canvas with the original dimensions
        black_canvas = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate the position to place the compressed frame in the black canvas
        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2

        # Place the compressed frame in the black canvas
        black_canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = compressed_frame

        # Write the frame with black areas to the output video
        out.write(black_canvas)

    # Perform expansion
    for frame_num in range(expansion_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to original dimensions
        expanded_frame = cv2.resize(frame, (width, height))

        # Write the frame to the output video
        out.write(expanded_frame)

    # Release video capture and writer objects
    cap.release()
    out.release()

    print("Video compression and expansion with transition completed successfully.")

input_video_path = './input_videos/1920x1080.mp4'
output_video_path = 'compressed_vdo_with_transition.mp4'
compression_factor = 0.5  # You can adjust the compression factor
transition_duration = 5  # You can adjust the transition duration in seconds

compress_and_expand_video(input_video_path, output_video_path, compression_factor, transition_duration)
