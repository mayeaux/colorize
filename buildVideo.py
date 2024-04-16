#!/usr/bin/env python
# coding: utf-8

import ffmpeg
import logging
import os
import shutil
from pathlib import Path

def get_fps(source_path):
    """ Helper function to extract frames per second from a video file. """
    try:
        probe = ffmpeg.probe(str(source_path))
        stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return eval(stream['r_frame_rate'])
    except Exception as e:
        logging.error("Error getting FPS: {0}".format(e))
        raise

def build_video():
    """ Function to build a video from colorized frames with hardcoded paths. """
    source_path = Path('/root/DeOldify/video/source/test.mp4')
    colorframes_root = Path('/root/DeOldify/video/colorframes')
    result_folder = Path('/root/DeOldify/video/result')

    colorized_path = result_folder / (source_path.name.replace('.mp4', '_no_audio.mp4'))
    colorframes_folder = colorframes_root / (source_path.stem)
    colorframes_path_template = str(colorframes_folder / '%5d.jpg')
    colorized_path.parent.mkdir(parents=True, exist_ok=True)
    if colorized_path.exists():
        colorized_path.unlink()
    fps = get_fps(source_path)

    process = (
        ffmpeg
            .input(colorframes_path_template, format='image2', vcodec='mjpeg', framerate=fps)
            .output(str(colorized_path), crf=17, vcodec='libx264')
            .global_args('-hide_banner')
            .global_args('-nostats')
            .global_args('-loglevel', 'error')
    )

    try:
        process.run()
    except ffmpeg.Error as e:
        logging.error("ffmpeg error: {0}".format(e), exc_info=True)
        logging.error('stdout:' + e.stdout.decode('UTF-8'))
        logging.error('stderr:' + e.stderr.decode('UTF-8'))
        raise e
    except Exception as e:
        logging.error('Error while building output video. Details: {0}'.format(e), exc_info=True)
        raise e

    result_path = result_folder / source_path.name
    if result_path.exists():
        result_path.unlink()
    shutil.copyfile(str(colorized_path), str(result_path))
    audio_file = Path(str(source_path).replace('.mp4', '.aac'))
    if audio_file.exists():
        audio_file.unlink()
    os.system(f'ffmpeg -y -i "{source_path}" -vn -acodec copy "{audio_file}" -hide_banner -nostats -loglevel error')
    if audio_file.exists():
        os.system(f'ffmpeg -y -i "{colorized_path}" -i "{audio_file}" -shortest -c:v copy -c:a aac -b:a 256k "{result_path}" -hide_banner -nostats -loglevel error')
    logging.info('Video created here: ' + str(result_path))
    return result_path

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_video()
