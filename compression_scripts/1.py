
import cv2
import numpy as np

def compress_and_expand_video(input_path, output_path, compression_factor):
    ''' This script generates a video which is compressed vertically by a given factor.'''
    try:
        # Open the video file
        cap = cv2.VideoCapture(input_path)

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Calculate new dimensions after compression
        new_width = int(width)
        # new_width = int(width * compression_factor)
        new_height = int(height * compression_factor)

        # Create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
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

        # Release video capture and writer objects
        cap.release()
        out.release()

        print("Video compression and expansion completed successfully.")
        
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage
input_video_path = './input_videos/1920x1080.mp4'
output_video_path = './output_videos/vert_compressed_vdo_output.mp4'
compression_factor = 0.5  # Adjust this value based on your compression requirements

compress_and_expand_video(input_video_path, output_video_path, compression_factor)
