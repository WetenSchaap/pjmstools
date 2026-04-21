from numpy._typing._array_like import NDArray


from typing import Any


import warnings
import numpy as np
import ffmpeg
from pathlib import Path

def contrast_normalize(image:np.ndarray, maxpx:int = 255) -> np.ndarray:
    """Renormalize contrast to outer bounds. Does not change datatype! Only input np.array's!"""
    return ((image - np.min(image)) / (np.max(image) - np.min(image))) * maxpx

def autocontrast(image:np.ndarray, cliprange:float = 2, maxpx:int = 255) -> np.ndarray:
    """Autocontrast to outer bounds + cliprange in %. Does not change datatype! Only input np.array's!"""
    minval = np.percentile(image, cliprange)
    maxval = np.percentile(image, 100 - cliprange)
    pixvals = np.clip(image, minval, maxval)
    return ((pixvals - minval) / (maxval - minval)) * maxpx


def stream_video(path: Path | str, batch_size: int = 100) -> NDArray[Any]:
    """
    Stream video frames from file using in batches to limit memory use.

    Decodes video via ffmpeg subprocess, yielding frames in fixed-size batches
    to avoid loading entire video into RAM. Returns RGB frames as uint8 arrays.

    Parameters
    ----------
    path : str or Path
        Path to video file (mp4, avi, mov, etc.). Any format readable by ffmpeg.
    batch_size : int, optional
        Number of frames per yielded batch. Tune based on available RAM and
        frame resolution (e.g., 1080p frames are ~6 MB each), by default 100.

    Yields
    ------
    np.ndarray
        Batch of frames with shape (N, H, W, 3) where N ≤ batch_size.
        Dtype is uint8, channels are RGB. Final batch may be smaller.
    """
    probe = ffmpeg.probe(path)
    width = probe["streams"][0]["width"]
    height = probe["streams"][0]["height"]

    process = (
        ffmpeg.input(path)
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .run_async(pipe_stdout=True)
    )

    frame_size = width * height * 3

    while True:
        batch = []
        for _ in range(batch_size):
            in_bytes = process.stdout.read(frame_size)
            if not in_bytes:
                break
            frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
            batch.append(frame)

        if not batch:
            break

        yield np.array(batch)  # Process this chunk, then discard

    process.wait()


def load_video(path:Path|str, batch_size:int=100, every_n_frames:int=1,) -> NDArray[Any]:
    """
    Load a video into a numpy array using ffmpeg. Load only every n frames to prevent memory explosion.

    Load every n frames of a video file into a numpy array using ffmpeg; cut the video into batches, load these, only keep every n frames, and throw out the rest, and continue to the next batch. Use stream_video to manage batch-based loading.

    Parameters
    ----------
    path : Path | str
        Path to video file (mp4, avi, mov, etc.). Any format readable by ffmpeg.
    batch_size : int, optional
        Number of frames per yielded batch. Tune based on available RAM and
        frame resolution (e.g., 1080p frames are ~6 MB each), by default 100.
    every_n_frames : int, optional
        Keep every n frames, discard the rest to save memory, by default 1 (e.g., discard no frames).

    Returns
    -------
    _type_
        _description_
    """
    if batch_size % every_n_frames != 0:
        warnings.warn(
            "batch_size and every_n_frames are not attuned to each other; every_n_frames should fit into batch_size an integer number of times, or drift will occur between batches"
        )
    full_array = []
    for batch in stream_video(path, batch_size=batch_size):
        full_array.extend(batch[::every_n_frames])  # 
    return np.array(full_array)
