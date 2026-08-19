import os
from tempfile import NamedTemporaryFile

import cv2
from PIL import Image


def extract_video_frames(video_bytes, sample_count=8, suffix=".mp4"):
    """Return evenly sampled RGB PIL frames and basic video metadata."""

    video_file = NamedTemporaryFile(suffix=suffix, delete=False)
    video_path = video_file.name

    try:
        video_file.write(video_bytes)
        video_file.flush()
        video_file.close()

        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            raise ValueError("The uploaded file is not a readable video.")

        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        if frame_count <= 0:
            capture.release()
            raise ValueError("The video does not contain readable frames.")

        frame_indexes = [
            round(index * (frame_count - 1) / (sample_count - 1))
            for index in range(sample_count)
        ] if sample_count > 1 else [0]

        frames = []
        for frame_index in dict.fromkeys(frame_indexes):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = capture.read()

            if success:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(rgb_frame))

        capture.release()
    finally:
        if not video_file.closed:
            video_file.close()
        os.unlink(video_path)

    if not frames:
        raise ValueError("The video does not contain readable frames.")

    metadata = {
        "Filename": "",
        "Format": "Video",
        "Width": width,
        "Height": height,
        "Frames": frame_count,
        "Frames analyzed": len(frames),
        "FPS": round(fps, 2),
        "Duration": f"{duration:.2f} seconds",
    }

    return frames, metadata