import cv2
import os
import logging
from datetime import datetime

# Configure logging
log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_print(message, level="info"):
    """Helper function to log and print messages."""
    if level == "error":
        logging.error(message)
        print(f"[ERROR] {message}")
    elif level == "warning":
        logging.warning(message)
        print(f"[WARNING] {message}")
    else:
        logging.info(message)
        print(f"[INFO] {message}")

# File paths
main_video_path = "input_videos/1920x1080.mp4"
footer_video_path = "input_videos/1280x170.mp4"
rszd_main_vdo = "resized_main_video.mp4"
edited_video = "final_combined_video.mp4"

# Check if video files exist
if not os.path.exists(main_video_path):
    log_and_print(f"Main video file not found: {main_video_path}", "error")
    exit(1)

if not os.path.exists(footer_video_path):
    log_and_print(f"Footer video file not found: {footer_video_path}", "error")
    exit(1)

# Load videos
main_video = cv2.VideoCapture(main_video_path)
footer_video = cv2.VideoCapture(footer_video_path)

# Check if videos opened successfully
if not main_video.isOpened():
    log_and_print("Failed to open main video.", "error")
    exit(1)

if not footer_video.isOpened():
    log_and_print("Failed to open footer video.", "error")
    exit(1)

log_and_print("Both videos loaded successfully.")

# Reduce the height of the main video
resize_percentage = 0.5  # 50% of original height

# Get frame dimensions
main_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
main_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
footer_width = int(footer_video.get(cv2.CAP_PROP_FRAME_WIDTH))
footer_height = int(footer_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(main_video.get(cv2.CAP_PROP_FPS))

# Check if any dimension is zero (invalid video file)
if main_width == 0 or main_height == 0:
    log_and_print("Main video has invalid dimensions.", "error")
    exit(1)

if footer_width == 0 or footer_height == 0:
    log_and_print("Footer video has invalid dimensions.", "error")
    exit(1)

# Target size for main video after resizing
target_width = footer_width
target_height = int(main_height * resize_percentage)

log_and_print(f"Resizing main video to: {target_width}x{target_height}")

# Video writer for resized main video
resized_main_video = cv2.VideoWriter(rszd_main_vdo, cv2.VideoWriter_fourcc(*"mp4v"), fps, (target_width, target_height))

# Loop through frames and resize
frame_count = 0
while True:
    ret_main, main_frame = main_video.read()
    
    if not ret_main:
        log_and_print("End of main video during resizing.", "info")
        break

    if main_frame is None:
        log_and_print(f"Main video frame {frame_count} is None, skipping...", "warning")
        continue

    resized_main_frame = cv2.resize(main_frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
    resized_main_video.write(resized_main_frame)
    frame_count += 1

log_and_print(f"Resized main video saved. Total frames resized: {frame_count}")

# Release resources
main_video.release()
resized_main_video.release()

# Load resized main video
resized_main_video = cv2.VideoCapture(rszd_main_vdo)

# Output video writer
combined_video = cv2.VideoWriter(edited_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (target_width, target_height + footer_height))

log_and_print(f"Creating final video of size: {target_width}x{target_height + footer_height}")

frame_count = 0
while True:
    ret_resized_main, resized_main_frame = resized_main_video.read()
    ret_footer, footer_frame = footer_video.read()

    # Stop if main video ends
    if not ret_resized_main:
        log_and_print("End of resized main video. Stopping processing.", "info")
        break

    if resized_main_frame is None:
        log_and_print(f"Resized main video frame {frame_count} is None, skipping...", "warning")
        continue

    if not ret_footer:
        # Loop footer video if it reaches the end
        log_and_print("Footer video ended, restarting it.", "info")
        footer_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_footer, footer_frame = footer_video.read()
        
        if not ret_footer or footer_frame is None:
            log_and_print("Failed to restart footer video, stopping.", "error")
            break

    # Ensure frame dimensions match
    if resized_main_frame.shape[1] != footer_frame.shape[1]:
        log_and_print(f"Frame width mismatch at frame {frame_count}: Resized {resized_main_frame.shape[1]} vs Footer {footer_frame.shape[1]}", "warning")
        continue

    if resized_main_frame.shape[0] != target_height:
        log_and_print(f"Resized main frame height is incorrect at frame {frame_count}, skipping...", "warning")
        continue

    if footer_frame.shape[0] != footer_height:
        log_and_print(f"Footer frame height is incorrect at frame {frame_count}, skipping...", "warning")
        continue

    # Concatenate frames
    combined_frame = cv2.vconcat([resized_main_frame, footer_frame])

    # Write to output video
    combined_video.write(combined_frame)
    frame_count += 1

log_and_print(f"Final video created successfully with {frame_count} frames.")

# Release resources
resized_main_video.release()
footer_video.release()
combined_video.release()

# Remove temporary resized video
try:
    os.remove(rszd_main_vdo)
    log_and_print("Temporary resized video deleted.")
except Exception as e:
    log_and_print(f"Failed to delete temporary video: {e}", "error")

log_and_print("Processing completed successfully.")
