"""



"""

### IMPORTS
from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
# Lol what
eventlet.monkey_patch()
from copy import deepcopy
import random
import time
import cv2
import numpy as np

# Import SPI library (for hardware SPI) and MCP3008 library.
is_pi = False
always_correct = True

if is_pi:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_MCP3008
    CLK  = 18
    MISO = 23
    MOSI = 24
    CS   = 25
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    import picamera
    camera = picamera.PiCamera()
    # camera.capture(filename) captures an image from the picamera, and puts the result into filename

### DEFINE THE FLASK APP
app = Flask(__name__)
socketio = SocketIO(app)
thread = None

PAPER_ADC_PIN = 0
PLASTIC_ADC_PIN = 1
IR_THRESHOLD = 500

IMAGE_FILENAME = "bin.jpg"


PLASTIC_START_POINT = [0,0]
PLASTIC_END_POINT = [1000,1000]

PAPER_START_POINT = [0,1000]
PAPER_END_POINT = [1000,2000]







def check_bins():
    """
    Returns a dict indicating true if a bin was found to have something currently being thrown into it
    """
    plastic_result = mcp.read_adc(PLASTIC_ADC_PIN) > IR_THRESHOLD
    paper_result = mcp.read_adc(PAPER_ADC_PIN) > IR_THRESHOLD
    return {
    PLASTIC_ADC_PIN: plastic_result,
    PAPER_ADC_PIN:paper_result
    }

def get_weight(bin_pin):
    """
    Returns the weight for a specified bin_pin, where the bin_pin is the pin associated
    with a bin's weight sensor
    """


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


def classify_bin(bin_type):
    if bin_type == "PLASTIC":
        "plastic section; just look at the plastic side"
        if always_correct:
            return "PLASTIC"
        else:
            return run_plastic_classifier(bin_type)

    else: # which means that bin_type == "PAPER"
        "paper section; just look at the paper side"
        if always_correct:
            return "PAPER"


def background_thread():

    # old_output = check_bins()
    while True:
        # This point in the code will monitor the thing
        bin_status = check_bins()
        # Actually, now we just need to monitor the two sensors and take a picture when one of them is tripped
        # if len(output.keys()) != 0:

        if True in bin_status.values():
            correct = True
            if is_pi:
                camera.capture(IMAGE_FILENAME)

            # Message to return to the webpage
            if bin_status[PAPER_ADC_PIN]:
                thrown = 'PAPER'
            elif bin_status[PLASTIC_ADC_PIN]:
                thrown = "PLASTIC"
            classification = classify_bin(thrown)
            output = {
            "correct":classification,
            "thrown":thrown
            }
            socketio.emit('message', output)
            time.sleep(1)

@app.route('/')
def hello_world():
    # Give them the main page, created by Billy
    return render_template("content.html")

@app.route('/startdemo')
def startdemo():
    '''
    Used for starting the hardcoded demo
    '''
    # Give the demo page
    return render_template("demo.html")

@app.route('/demo')
def do_demo_from_phone():
    '''
    thrown and correct are both url parameters.
    thrown: "PAPER" or "PLASTIC"
    correct: "TRUE" or "FALSE"
    '''
    results = request.args.get("result").split("_")
    thrown = results[0]
    correct = results[1]
    message = {
    "thrown":thrown,
    "correct":correct
    }
    socketio.emit("message",message)
    return render_template("demo.html")

@socketio.on("connect")
def connect():
    global thread
    if thread == None:
        thread = socketio.start_background_task(target = background_thread)

if __name__ == "__main__":
    socketio.run(app, debug = True)
