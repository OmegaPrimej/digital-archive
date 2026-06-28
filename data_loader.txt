import numpy as np
import cv2

def load_data(video_path, caption_path, batch_size=32, frame_step=5, frame_height=224, frame_width=224):
    
    Load Hollywood video data and corresponding captions.

    Parameters:
    video_path (str): Path to Bollywood video file.
    caption_path (str): Path to text file containing video captions.
    batch_size (int): Number of video frames to load in each batch. Default=32.
    frame_step (int): Number of frames to skip between each loaded frame. Default=5.
    frame_height (int): Height of resized video frames. Default=224.
    frame_width (int): Width of resized video frames. Default=224.

    Returns:
    data (list): List of tuples containing video frames and corresponding captions.
    
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    captions = open(caption_path, 'r').readlines()

    # Preprocess captions
    captions = [cap.strip() for cap in captions]

    # Load video frames in batches
    for start in range(0, frame_count, batch_size * frame_step):
        batch_frames = []
        for _ in range(batch_size):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (frame_width, frame_height))  # Resize frames
            batch_frames.append(frame)
            for _ in range(frame_step - 1):  # Skip frames
                ret, _ = cap.read()
                if not ret:
                    break
        frames.append(np.array(batch_frames))

    # Match frames with captions
    data = list(zip(frames, captions[::batch_size * frame_step]))

    return data

def load_video(video_path):
    
    Load video file into memory.

    Parameters:
    video_path (str): Path to video file.

    Returns:
    frames (list): List of video frames.
    
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def load_caption(caption_path):
    
    Load caption file into memory.

    Parameters:
    caption_path (str): Path to caption file.

    Returns:
    captions (list): List of captions.
    
    with open(caption_path, 'r') as file:
        captions = [line.strip() for line in file.readlines()]
    return captions

def split_data(data, train_ratio=0.8):
    
    Split data into training and validation sets.

    Parameters:
    data (list): List of tuples containing video frames and captions.
    train_ratio (float): Ratio of training data. Default=0.8.

    Returns:
    train_data (list): List of tuples for training.
    val_data (list): List of tuples for validation.
    
    train_size = int(len(data) * train_ratio)
    train_data = data[:train_size]
    val_data = data[train_size:]
    return train_data, val_data
