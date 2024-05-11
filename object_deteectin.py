from imageai.Detection import ObjectDetection
from PIL import Image

obj_detect = ObjectDetection()
obj_detect.setModelPath("yolov3.pt")
obj_detect.loadModel()

detected_obj = obj_detect.detectObjectsFromImage(
    input_image="c2.jpg",
    output_image_path="c22.jpg"
)

for obj in detected_obj:
    print(obj["name"] + "-"
          +str(obj["percentage_probability"]),
          obj["box_points"])


im = Image.open("c1.jpg")
im.show()