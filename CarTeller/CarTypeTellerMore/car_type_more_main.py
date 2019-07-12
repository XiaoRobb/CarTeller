from imageai.Detection import ObjectDetection, VideoObjectDetection
import matplotlib.pyplot as plt
import os
import cv2
import base64

def car_type_more_tell_video(path):
    execution_path = os.getcwd()

    detector = VideoObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel("fast")

    detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, path),
                                                 output_file_path=os.path.join(execution_path, "test"),
                                                 frames_per_second=20, log_progress=True)
    print("success")

def car_type_more_tell(img):
    """
    汽车类型识别（多车）：
    :param img: cv2格式
    :return: 返回预测图片， 和各类车的种类
    """
    type_dict = {"car_count": 0,
                 "bus_count": 0,
                 "motorcycle_count": 0,
                 "bicycle_count": 0,
                 "truck_count": 0}

    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections_img, detections_list = detector.detectObjectsFromImage(input_image=img,
                                                                      input_type="array", output_type="array")
    for eachObject in detections_list:
        if eachObject["name"] == 'car':
            type_dict["car_count"] += 1
        if eachObject["name"] == 'truck':
            type_dict["truck_count"] += 1
        if eachObject["name"] == 'bus':
            type_dict["bus_count"] += 1
        if eachObject["name"] == 'motorcycle':
            type_dict["motorcycle_count"] += 1
        if eachObject["name"] == 'bicycle':
            type_dict["bicycle_count"] += 1
    return detections_img, type_dict


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code

if __name__ == "__main__":
     #img = cv2.imread("./test.jpg")
     #detections_img, type_dict = car_type_more_tell(img)
     #print(detections_img)
     #string=image_to_base64(detections_img)
     #print(string)
     #plt.figure()
     #plt.imshow(detections_img)
     #plt.show()
     #print(type_dict)
     car_type_more_tell_video("./videoplayback.avi")
