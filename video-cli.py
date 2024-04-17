#!/usr/bin/env python
# coding: utf-8

import argparse
import warnings
import logging
import datetime


from deoldify import device
from deoldify.device_id import DeviceId

current_time = datetime.datetime.now()
logging.info(f"Booting the CLI - {current_time}")

# Set GPU device first as required
device.set(device=DeviceId.GPU0)

from deoldify.visualize import get_video_colorizer

# Set up warnings to ignore specific user warnings about empty datasets
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")


# NOTE: For render_factor max is 44 with 11GB video cards.
# 21 is a good default

# Get the current date and time

# Create a command line argument parser
parser = argparse.ArgumentParser(description='Colorize black and white videos using DeOldify.')

# needs to be an mp4 in the video/source folder
parser.add_argument('file_name', type=str, help='File name of the video to colorize, including extension (e.g., video.mp4)')
parser.add_argument('-r', '--render_factor', type=int, default=21, help='Render factor to control the quality of colorization, higher is better but more resource-intensive (default: 4)')

# Parse the arguments
args = parser.parse_args()

current_time = datetime.datetime.now()
logging.info(f"Instantiating the video colorizer - {current_time}")


# Initialize the video colorizer
colorizer = get_video_colorizer()

current_time = datetime.datetime.now()
logging.info(f"Video colorizer instantiated - {current_time}")


# print the file name and render factor
print("File name:", args.file_name)
print("Render factor:", args.render_factor)

# Perform colorization
result_path = colorizer.colorize_from_file_name(args.file_name, render_factor=args.render_factor)

# Output the result path
print("Result path:")
print(result_path)
