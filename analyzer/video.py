import os
from tempfile import NamedTemporaryFile

import cv2
from PIL import Image


def extract_video_frames(video_bytes, sample_count=8, suffix=".mp4"):
    """Return evenly sampled RGB PIL frames and basic video metadata."""

    if not video_bytes:
        raise ValueError("No video was uploaded.")

    # Safety limit: 100 MB
    max_video_size = 100 * 1024 * 1024

    if len(video_bytes) > max_video_size:
        raise ValueError(
            "Video is too large. Please upload a video smaller than 100 MB."
        )

    video_file = NamedTemporaryFile(
        suffix=suffix,
        delete=False
    )

    video_path = video_file.name

    frames = []

    try:
        video_file.write(video_bytes)
        video_file.flush()
        video_file.close()

        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            raise ValueError(
                "The uploaded file is not a readable video."
            )

        frame_count = int(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        fps = float(
            capture.get(cv2.CAP_PROP_FPS) or 0
        )

        width = int(
            capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        duration = (
            frame_count / fps
            if fps > 0
            else 0
        )

        if frame_count <= 0:
            raise ValueError(
                "The video does not contain readable frames."
            )

        # Never request more frames than actually exist.
        actual_sample_count = min(
            sample_count,
            frame_count
        )

        if actual_sample_count > 1:
            frame_indexes = [
                round(
                    index * (frame_count - 1)
                    / (actual_sample_count - 1)
                )
                for index in range(actual_sample_count)
            ]
        else:
            frame_indexes = [0]

        for frame_index in dict.fromkeys(frame_indexes):

            capture.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_index
            )

            success, frame = capture.read()

            if not success:
                continue

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb_frame)

            # Prevent extremely large video frames
            # from consuming excessive memory.
            max_dimension = 1600

            if max(image.size) > max_dimension:
                image.thumbnail(
                    (max_dimension, max_dimension)
                )

            frames.append(image)

        capture.release()

    finally:

        try:
            if not video_file.closed:
                video_file.close()
        except Exception:
            pass

        if os.path.exists(video_path):
            os.unlink(video_path)

    if not frames:
        raise ValueError(
            "The video does not contain readable frames."
        )

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
