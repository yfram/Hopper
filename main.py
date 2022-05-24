from picamera import PiCamera
from time import sleep
from lobe import ImageModel
from gpiozero import Motor
from enum import Enum


MODEL_PATH = '/home/pi/Downloads/Hopper/Tflite files/Apples'
RECORDS_PATH = "/home/pi/Documents/records.txt"


class State(Enum):
    APPLE = 0,
    PEAR = 1


def take_photo():
    global camera
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/Pictures/image.jpg')
    camera.stop_preview()
    sleep(1)


def document_in_file(label):
    with open(RECORDS_PATH, "r+") as f:
        current = f.readlines()
        f.seek(0, 0)
        flag = False
        for line in current:
            if label not in line:
                f.write(line)
            else:
                f.write(
                    label + ": " + str(int(line.removeprefix(label + ": ").removesuffix('\n')) + 1) + "\n")
                flag = True
        if not flag:
            f.write(label + ": 1\n")


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
    document_in_file(label)
    if label == "Apples":
        change_state(State.APPLE)
    elif label == "Pears":
        change_state(State.PEAR)
    else:
        raise Exception("No label found")


motor_state = State.PEAR
motor = Motor(forward=4, backward=14)
if motor.value == 1:
    motor.stop()
camera = PiCamera()
model = ImageModel.load(MODEL_PATH)
take_photo()
# Run photo through Lobe TF model
result = model.predict_from_file('/home/pi/Pictures/image.jpg')
solve(result.prediction)
