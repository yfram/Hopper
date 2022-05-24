import imp
from picamera import PiCamera
from time import sleep
from lobe import ImageModel
from gpiozero import Motor
from enum import Enum

class State(Enum):
    APPLE = 0,
    PEAR = 1

camera = PiCamera()
model = ImageModel.load('/home/pi/Downloads/Hopper/Tflite files/Apples')

motor_state = State.APPLE
motor = Motor(forward=4, backward=14)
if motor.value == 1:
    motor.stop()

def take_photo():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/Pictures/image.jpg')
    camera.stop_preview()
    sleep(1)

def change_state(state):
    global motor_state
    if motor_state == state:
        return
    motor_state = state
    if motor_state == State.APPLE:
        motor.forward()
        sleep(1)
        motor.stop()
    else:
        motor.backward()
        sleep(1)
        motor.stop()

def solve(label):
    print(label)
    if label == "Apples":
        change_state(State.APPLE)
    elif label == "Pears":
        change_state(State.PEAR)
    else:
        raise Exception("No label found")


take_photo()
# Run photo through Lobe TF model
result = model.predict_from_file('/home/pi/Pictures/image.jpg')
solve(result.prediction)
