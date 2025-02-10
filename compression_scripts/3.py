import cv2
import numpy as np

def compress_and_expand_video(input_path, output_path, compression_factor, transition_duration=5):
    '''This code gradually showing transition of video being compressed from all corners. '''
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
        expansion_frames = compression_frames

        # Perform compression
        for frame_num in range(compression_frames):
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame to gradually compressed dimensions
            compression_scale = 1.0 - (frame_num / compression_frames) * (1.0 - compression_factor)
            compressed_frame = cv2.resize(frame, (int(width * compression_scale), int(height * compression_scale)))

            # Create a black canvas with the original dimensions
            black_canvas = np.zeros((height, width, 3), dtype=np.uint8)

            # Calculate the position to place the compressed frame in the black canvas
            x_offset = (width - compressed_frame.shape[1]) // 2
            y_offset = (height - compressed_frame.shape[0]) // 2

            # Place the compressed frame in the black canvas
            black_canvas[y_offset:y_offset+compressed_frame.shape[0], x_offset:x_offset+compressed_frame.shape[1]] = compressed_frame

            # Write the frame with black areas to the output video
            out.write(black_canvas)

        # Perform expansion
        for frame_num in range(expansion_frames):
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame to gradually original dimensions
            expansion_scale = (frame_num / expansion_frames) * (1.0 - compression_factor) + compression_factor
            expanded_frame = cv2.resize(frame, (int(width * expansion_scale), int(height * expansion_scale)))

            # Write the frame to the output video
            out.write(expanded_frame)

        # Release video capture and writer objects
        cap.release()
        out.release()

        print("Video compression and expansion with gradual transition completed successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage
input_video_path = './input_videos/1920x1080.mp4'
output_video_path = './output_videos/compressed_expanded_video2.mp4'
compression_factor = 0.5  # You can adjust the compression factor
transition_duration = 5  # You can adjust the transition duration in seconds

compress_and_expand_video(input_video_path, output_video_path, compression_factor, transition_duration)
