import cv2
import numpy as np

def combine_videos_with_separator(upper_video_path, lower_video_path, output_path, separator_thickness=5):
    # Open the videos
    upper_video = cv2.VideoCapture(upper_video_path)
    lower_video = cv2.VideoCapture(lower_video_path)

    # Get the properties of the upper video
    upper_width = int(upper_video.get(3))
    upper_height = int(upper_video.get(4))
    upper_fps = upper_video.get(5)

    # Get the properties of the lower video
    lower_width = int(lower_video.get(3))
    lower_height = int(lower_video.get(4))
    lower_fps = lower_video.get(5)

    # Ensure the widths of both videos are the same
    if upper_width != lower_width:
        raise ValueError("Widths of the videos must be the same.")

    # Create VideoWriter object to write the combined video
    combined_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), upper_fps,
                                     (upper_width, upper_height + separator_thickness + lower_height))

    while True:
        ret_upper, frame_upper = upper_video.read()
        ret_lower, frame_lower = lower_video.read()

        if not ret_upper or not ret_lower:
            break

        # Resize the lower video to match the width of the upper video
        frame_lower_resized = cv2.resize(frame_lower, (upper_width, lower_height))

        # Create a black frame as a separator
        separator_frame = np.zeros((separator_thickness, upper_width, 3), dtype=np.uint8)

        # Combine frames vertically with the separator
        combined_frame = np.vstack((frame_upper, separator_frame, frame_lower_resized))

        # Write the combined frame to the output video file
        combined_video.write(combined_frame)

    # Release the video capture and writer objects
    upper_video.release()
    lower_video.release()
    combined_video.release()

    print(f"Videos combined with separator and saved to {output_path}")


# Example usage
video1_path = 'input_videos/360x1080.mp4'
video2_path = 'input_videos/360x1280.mp4'
output_path = 'zv.mp4'

combine_videos_with_separator(video1_path, video2_path, output_path)



# # Example usage
# upper_video_path = 'input_videos/360x1280.mp4'
# # upper_video_path = 'input_videos/720x1080.mp4'
# lower_video_path = 'input_videos/360x1080.mp4'
# output_path = 'combined_video_with_separator.mp4'

# combine_videos_with_separator(upper_video_path, lower_video_path, output_path)
