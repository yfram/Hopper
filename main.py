from picamera import PiCamera
from time import sleep
from lobe import ImageModel

camera = PiCamera()

model = ImageModel.load('/home/pi/Downloads/Hopper/Tflite files/Apples')

# Take Photo
def take_photo():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/Pictures/image.jpg')
    camera.stop_preview()
    sleep(1)

# # Identify prediction and turn on appropriate LED
# def solve(label):
#     print(label)
#     if label == "Apples":
#         print("Apples")
#     if label == "Pears":
#         print("Pears")
#     else:
#         raise Exception("No label found")

take_photo()
# Run photo through Lobe TF model
result = model.predict_from_file('/home/pi/Pictures/image.jpg')
print(result.Prediction)
