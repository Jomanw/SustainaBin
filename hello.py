"""
Flask server that pushes

Weight sensor (HX711)
IR LEDs with ADC
Microphone
Speaker
LCD Display
UltraSonic sensor


Get speaker set up: ORDERING SPEAKER SO DONE
NICE TO HAVE: Learn how to do voice recognition with the usb microphone (https://maker.pro/raspberry-pi/tutorial/the-best-voice-recognition-software-for-raspberry-pi)
Create a get_weight(bin) function # Gets the weight of a specified bin
Create a get_height(bin) function # Gets the height of a specified bin
LCD Display setup / make sure it works with the pi / get it to work EZ(?)
NICE TO HAVE: Motion Sensor, get it to work
No interruption




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

###
devices = []
# TODO: CHANGE THIS TO A REASONABLE PIN
# ir_led_pin = 10
# ir_thresh = 100
# PAPER_WEIGHT_PIN = 12
# PLASTIC_WEIGHT_PIN = 13
# METAL_WEIGHT_PIN = 14
#
# PAPER_ADC_PIN = 15
# PLASTIC_ADC_PIN = 16
# METAL_ADC_PIN = 17
#
# bins_weight = {"paper":PAPER_WEIGHT_PIN,"plastic":PLASTIC_WEIGHT_PIN,"metal":METAL_WEIGHT_PIN}
# bins_adc = {"paper":PAPER_ADC_PIN,"plastic":PLASTIC_ADC_PIN,"metal":METAL_ADC_PIN}

# Define pins being used for both plastic and paper IR LED's
PAPER_ADC_PIN = 0
PLASTIC_ADC_PIN = 1
IR_THRESHOLD = 500

IMAGE_FILENAME = "bin.jpg"


# class Device:
#     def __init__(self, device_type, check_function, function_args = None):
#         self.device_type = device_type
#         self.check_function = check_function
#         self.function_args = function_args
#
#     def check(self):
#         if self.function_args == None:
#             return self.check_function()
#         else:
#             return self.check_function(*self.function_args)
#
# def get_pin_value(pin):
#     # value = RPIO.input(ir_led_pin)
#     # return value
#     return random.random() * 103
#
# def check_ir(pin):
#     """
#     Returns true if something is obstructing the sensor, false otherwise
#     """
#     value = get_pin_value(pin)
#     if value > ir_thresh:
#         return value
#     else:
#         return False
#
# ir_receiver = Device("ir_led",check_ir,[ir_led_pin])
# devices.append(ir_receiver)
#
# def check_sensors():
#     output = {}
#     for device in devices:
#         result = device.check()
#         if result != False:
#             output[device.device_type] = result
#     return output

def check_bins():
    """
    Returns a dict indicating true if a bin was found to have something currently being thrown into it
    """
    plastic_result = mcp.read_adc(PLASTIC_ADC_PIN) > IR_THRESHOLD
    paper_result = mcp.read_adc(PAPER_ADC_PIN) > IR_THRESHOLD
    return {
    PLASTIC_ADC_PIN: plastic_result ,
    PAPER_ADC_PIN:paper_result
    }


# def check_bins():
#
#     output = {}
#     pin_values = get_pin_values()
#     for pin in pin_values.keys():
#         value = False
#         if pin_values[pin] > IR_THRESHOLD:
#             value = True
#         output[pin] = value
#     return output

def get_weight(bin_pin):
    """
    Returns the weight for a specified bin_pin, where the bin_pin is the pin associated
    with a bin's weight sensor
    """

def run_classifier(bin_type):
    pass

def classify_bin(bin_type):
    if bin_type == "PLASTIC":
        "plastic section; just look at the plastic side"
        if always_correct:
            return "PLASTIC"

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
            # if bin_status[PAPER_ADC_PIN]:
            #     # If something is thrown into the paper bin:
            #     plastic = False
            #     classification = classify_bin("PAPER")
            #     output = {
            #     "correct":classification,
            #     "thrown":"PAPER"
            #     }
            #
            # elif bin_status[PLASTIC_ADC_PIN]:
            #     # If something is thrown into the plastic bin:
            #     plastic = True
            #     classification = classify_bin("PLASTIC")
            #     correct = classification == "PLASTIC"
            socketio.emit('message', output)
            time.sleep(1)

        #
        #
        # if output != old_output:
        #     message = {}
        #     for sensor in output.keys():
        #         if output[sensor] != old_output[sensor]:
        #             message[sensor] = output[sensor]
        #
        #     print("Emmitted the thing")
        #     time.sleep(2)
        # old_output = deepcopy(output)

@app.route('/')
def hello_world():
    # newFile = open("content.html", "rb")
    return render_template("content.html")
    # return 'Hello, World!'

@app.route('/startdemo')
def startdemo():
    '''
    Used for starting the hardcoded demo
    '''

    return render_template("demo.html")

@app.route('/demo')
def do_demo_from_phone():
    '''
    thrown and correct are both url parameters.
    thrown: "PAPER" or "PLASTIC"
    correct: "TRUE" or "FALSE"
    '''
    # thrown = request.args.get("thrown")
    # correct = request.args.get("correct")
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
