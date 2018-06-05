from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO, emit
import eventlet
import random
# Lol what
eventlet.monkey_patch()
import time
import RPIO

app = Flask(__name__)
socketio = SocketIO(app)
thread = None

devices = []
# TODO: CHANGE THIS TO A REASONABLE PIN
ir_led_pin = 10
ir_thresh = 100


RPIO.setup(ir_led_pin, RPIO.IN)

class Device:
    def __init__(self, device_type, check_function, function_args = None):
        self.device_type = device_type
        self.check_function = check_function
        self.function_args = function_args

    def check(self):
        if self.function_args == None:
            return self.check_function()
        else:
            return self.check_function(*self.function_args)

def get_pin_value(pin):
    value = RPIO.input(ir_led_pin)
    return value
    return random.random() * 103

def check_ir(pin):
    """
    Returns true if something is obstructing the sensor, false otherwise
    """
    value = get_pin_value(pin)
    if value > ir_thresh:
        return value
    else:
        return False

ir_receiver = Device("ir_led",check_ir,[ir_led_pin])
devices.append(ir_receiver)

def check_sensors():
    output = {}
    for device in devices:
        result = device.check()
        if result != False:
            output[device.device_type] = result
    return output

def background_thread():
    while True:
        # This point in the code will monitor the thing
        output = check_sensors()
        if len(output.keys()) != 0:
            for sensor in output.keys():
                socketio.emit('message', output)
                print("Emmitted the thing")
                time.sleep(2)

@app.route('/')
def hello_world():
    # newFile = open("content.html", "rb")
    return render_template("content.html")
    # return 'Hello, World!'

@socketio.on("connect")
def connect():
    global thread
    if thread == None:
        thread = socketio.start_background_task(target = background_thread)

if __name__ == "__main__":
    socketio.run(app, debug = True)
