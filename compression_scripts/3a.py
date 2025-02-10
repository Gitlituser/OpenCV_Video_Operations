import cv2
import numpy as np

def compress_and_expand_video(input_path, output_path, compression_factor, transition_start, transition_end, transition_duration=5):
    '''Here we are compressing the original video, in 3 part, the duration was lowered that has been handeled here'''
    try:
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
        expansion_frames = total_frames - compression_frames

        # Perform compression only for the specified part of the video
        for frame_num in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            if transition_start * fps <= frame_num < (transition_start + transition_duration) * fps:
                # Resize frame to gradually compressed dimensions during the transition period
                compression_scale = 1.0 - ((frame_num - transition_start * fps) / compression_frames) * (1.0 - compression_factor)
                compressed_frame = cv2.resize(frame, (int(width * compression_scale), int(height * compression_scale)))

                # Create a black canvas with the original dimensions
                black_canvas = np.zeros((height, width, 3), dtype=np.uint8)

                # Calculate the position to place the compressed frame in the black canvas
                x_offset = (width - compressed_frame.shape[1]) // 2
                y_offset = (height - compressed_frame.shape[0]) // 2

                # Place the compressed frame in the black canvas
                black_canvas[y_offset:y_offset + compressed_frame.shape[0], x_offset:x_offset + compressed_frame.shape[1]] = compressed_frame

                # Write the frame with black areas to the output video
                out.write(black_canvas)
            else:
                # Write the frame to the output video without compression
                out.write(frame)

        # Release video capture and writer objects
        cap.release()
        out.release()

        print("Video compression and expansion with gradual transition completed successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage
input_video_path = './input_videos/1920x1080.mp4'
output_video_path = './output_videos/output_video.mp4'
compression_factor = 0.8  # You can adjust the compression factor
transition_start = 5  # Start of the transition in seconds
transition_end = 10  # End of the transition in seconds
transition_duration = 5  # Duration of the transition in seconds

compress_and_expand_video(input_video_path, output_video_path, compression_factor, transition_start, transition_end, transition_duration)
