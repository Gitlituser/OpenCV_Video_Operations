import cv2
import numpy as np

def combine_videos(video1_path):
    '''Priovide path of any video and check its dimensions.'''
    # Read the input videos
    video1 = cv2.VideoCapture(video1_path)
    # video2 = cv2.VideoCapture(video2_path)

    # Get the properties of the videos
    width1 = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = video1.get(cv2.CAP_PROP_FPS)


    print(f"check_dmxn : (width x height) : {width1} x {height1}")

    # Release video capture and writer objects
    video1.release()

video1_path = "input_videos/trimmed_ad_video.mp4" # 1280 x 170 done
# video1_path = "zx.mp4" # 1080 x 1080
combine_videos(video1_path)
