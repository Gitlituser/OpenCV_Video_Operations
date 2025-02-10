import os
import cv2
import numpy as np

def resize_video(input_file, output_file, target_width, target_height):
    try:
        # Open the video file
        cap = cv2.VideoCapture(input_file)

        # Get the original video's width, height, and frames per second (fps)
        original_width = int(cap.get(3))
        original_height = int(cap.get(4))
        fps = cap.get(5)

        # Create VideoWriter object to write the resized video
        # fourcc = cv2.VideoWriter_fourcc(*'X264')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, fps, (target_width, target_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame to the target resolution
            resized_frame = cv2.resize(frame, (target_width, target_height))

            # Write the resized frame to the output video file
            out.write(resized_frame)

        # Release the video capture and writer objects
        cap.release()
        out.release()

        # print(f"Video resized and saved to {output_file}")
        return True
    except Exception as e:
        print(e)
        return False

def combine_horizontal_videos(video1_path, video2_path, output_path):
    try:
        # Read the input videos
        video1 = cv2.VideoCapture(video1_path)
        video2 = cv2.VideoCapture(video2_path)
        separator_width = 5

        # Get the properties of the videos
        width1 = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height1 = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps1 = video1.get(cv2.CAP_PROP_FPS)

        width2 = int(video2.get(cv2.CAP_PROP_FRAME_WIDTH))
        height2 = int(video2.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps2 = video2.get(cv2.CAP_PROP_FPS)

        # Choose the maximum height of the two videos
        max_height = max(height1, height2)

        # Calculate the new width for both videos
        new_width1 = int(width1 * (max_height / height1))
        new_width2 = int(width2 * (max_height / height2))

        # Create the VideoWriter object
        output_width = new_width1 + separator_width + new_width2
        output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps1, (output_width, max_height))

        while True:
            # Read frames from both videos
            ret1, frame1 = video1.read()
            ret2, frame2 = video2.read()

            # Break the loop if either video reaches the end
            if not ret1 or not ret2:
                break

            # Resize frames to the maximum height
            frame1 = cv2.resize(frame1, (new_width1, max_height))
            frame2 = cv2.resize(frame2, (new_width2, max_height))

            # Create a black frame as a separator
            separator_frame = np.zeros((max_height, separator_width, 3), dtype=np.uint8)

            # Combine frames horizontally with the separator
            combined_frame = np.hstack((frame1, separator_frame, frame2))

            # Write the combined frame to the output video
            output.write(combined_frame)

        # Release video capture and writer objects
        video1.release()
        video2.release()
        output.release()
        return True

        # print(f"Videos combined successfully. Output saved to {output_path}")
    except Exception as e:
        print(f"{e}")
        return False

def combine_videos_vertically(upper_video_path, lower_video_path, output_path):
    try:
        # Open the videos
        upper_video = cv2.VideoCapture(upper_video_path)
        lower_video = cv2.VideoCapture(lower_video_path)
        separator_thickness=5

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

        print(f"Videos combined vertically and saved to {output_path}")
        return True
    except Exception as e:
        print(e)
        return False

def remove_files(*file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' removed.")
        else:
            print(f"File '{file_path}' does not exist.")
            
# Example usage
input_video = 'input_videos/1920x1080.mp4'
reduced1_output_video = 'resized_video1.mp4'
target_width = 1600
target_height = 900

reduce_main_vdo = resize_video(input_video, reduced1_output_video, target_width, target_height)
if reduce_main_vdo:
    # resize the side ad video : 
    input_video = 'input_videos/360x1080.mp4'
    reduced2_output_video = 'resized_video2.mp4'
    target_width = 320
    target_height = 900
    reduce_side_vdo = resize_video(input_video, reduced2_output_video, target_width, target_height)
    if reduce_side_vdo:
        # size vdo resized, now combining it with main to gen main_video
        left_video_path = reduced2_output_video
        right_video_path = reduced1_output_video
        combined_horizontal_vdo = 'main_horizontal_video.mp4'
        combine_h_vdos = combine_horizontal_videos(left_video_path, right_video_path, combined_horizontal_vdo)
        if combine_h_vdos:
            # print(f"Upwork has been done successfully, check {output_path}")
            # resizing third vdo
            target_width = 1920
            target_height = 900
            resized_sep_com_h_vdo = "rszd_sep_combined_hrzntl.mp4"
            resize_separator_vdo = resize_video(combined_horizontal_vdo, resized_sep_com_h_vdo, target_width, target_height)
            if resize_separator_vdo:
                #-------------- if separator resized
                input_video = 'input_videos/org_ad.mp4'
                output_resized_footer_video = reduced2_output_video
                target_width = 1920
                target_height = 180
                resize_base_vdo = resize_video(input_video, output_resized_footer_video, target_width, target_height)
                if resize_base_vdo:

                    # footer vdo resized
                    upper_video_path = resized_sep_com_h_vdo
                    lower_video_path = output_resized_footer_video
                    final_vdo_output_path = "final_vdo.mp4"
                    final_output_vdo = combine_videos_vertically(upper_video_path, lower_video_path, final_vdo_output_path)
                    if final_output_vdo:
                        target_width = 1920
                        target_height = 1080
                        final_1920x1080_vdo = "final_1920x1080_vdo.mp4"
                        resize_ver_sep_final_vdo = resize_video(final_vdo_output_path, final_1920x1080_vdo, target_width, target_height)
                        if resize_ver_sep_final_vdo:
                            # remove_files(reduced1_output_video, reduced2_output_video, combined_horizontal_vdo, resized_sep_com_h_vdo, final_output_vdo, final_vdo_output_path)
                            remove_files(reduced1_output_video, reduced2_output_video, combined_horizontal_vdo, resized_sep_com_h_vdo, output_resized_footer_video, final_vdo_output_path)
                            print(f"final vdo has been prepared... check - {final_1920x1080_vdo}")
        else:
            print("error combininb both vdos.")
    else:
        print("Error in resizing side ad vdo")
else:
    print("Error in resizing main vdo")


