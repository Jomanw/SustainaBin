"""
Script for playing with the picamera and opencv
"""
# import cv2
# import numpy as np
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

import picamera
camera = picamera.PiCamera()

from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
# Lol what
eventlet.monkey_patch()
from copy import deepcopy
import random
import time
# import cv2
# import numpy as np
from PIL import Image

PLASTIC_START_POINT = [0,0]
PLASTIC_END_POINT = [1000,1000]

PAPER_START_POINT = [0,1000]
PAPER_END_POINT = [1000,2000]

PLASTIC_TUPLE = (PLASTIC_START_POINT[0],PLASTIC_START_POINT[1],PLASTIC_END_POINT[0],PLASTIC_END_POINT[1])
PAPER_TUPLE = (PAPER_START_POINT[0],PAPER_START_POINT[1],PAPER_END_POINT[0],PAPER_END_POINT[1])

IMAGE_FILENAME = "bintest.jpg"


def get_average_pixel(img):
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color

def run_plastic_classifier():
    # Get only the relevant points
    x_o = PLASTIC_START_POINT[0]
    y_o = PLASTIC_START_POINT[1]
    x_f = PLASTIC_END_POINT[0]
    y_f = PLASTIC_END_POINT[1]
    img = cv2.imread(IMAGE_FILENAME)[x_o:x:f,y_o:y_f]
    average_pixel = get_average_pixel(img)


def run_paper_classifier():
    # Get only the relevant points
    x_o = PAPER_START_POINT[0]
    y_o = PAPER_START_POINT[1]
    x_f = PAPER_END_POINT[0]
    y_f = PAPER_END_POINT[1]
    img = cv2.imread(IMAGE_FILENAME)[x_o:x:f,y_o:y_f]
    average_pixel = get_average_pixel(img)


camera.capture(IMAGE_FILENAME)

img = Image.open(IMAGE_FILENAME)
cropped_plastic = img.crop(PLASTIC_TUPLE)
cropped_paper = img.crop(PAPER_TUPLE)

cropped_plastic.show()
