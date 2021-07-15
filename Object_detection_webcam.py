# Import packages
import os
import cv2
import numpy as np
import sys
import tensorflow.compat.v1 as tf
from time import sleep
import time
from subprocess import call
import socket, cv2, pickle, struct


tf.disable_v2_behavior()

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = "trained_inference_graph"
VIDEO_NAME = "images_video.mp4"

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, "frozen_inference_graph.pb")

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, "training", "object-detection.pbtxt")

PATH_TO_VIDEO = os.path.join(CWD_PATH, VIDEO_NAME)

# Number of classes the object detector can identify
NUM_CLASSES = 1

## Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True
)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name="")

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name("image_tensor:0")

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name("detection_boxes:0")

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name("detection_scores:0")
detection_classes = detection_graph.get_tensor_by_name("detection_classes:0")

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name("num_detections:0")

# Initialize webcam feed
video = cv2.VideoCapture(PATH_TO_VIDEO)
ret = video.set(3, 1280)
ret = video.set(4, 720)

start = time.time()


while True:

    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    
    ret, frame = video.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_expanded = np.expand_dims(frame_rgb, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded},
    )

    # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60,
    )

    objects = []
    threshold = (
        0.5
    )  # in order to get higher percentages you need to lower this number; usually at 0.01 you get 100% predicted objects
    for index, value in enumerate(classes[0]):
        object_dict = {}
        if scores[0, index] > threshold:
            object_dict[
                (category_index.get(value)).get("name").encode("utf8")
            ] = scores[0, index]
            objects.append(object_dict)
    # print(objects)
    # print(type(objects))

    if objects != []:
        # print(objects[0].keys())
        # print(list(objects[0].keys()))
        if b"Accident" in list(objects[0].keys()):
            if objects[0][b"Accident"] > 0.50:
                print(
                    "WARNING! An Accident has been Detected. Starting the Video Stream."
                )
                end = time.time()
                if int(end - start) >= 6:
                    # print(int(end - start))
                    video.release()
                    cv2.destroyAllWindows()
                    sleep(5)

                    import sender

                    os.system("python3 sender.py")
                    sleep(10)

                    video = cv2.VideoCapture(PATH_TO_VIDEO)
                    ret = video.set(3, 320)
                    ret = video.set(4, 240)
                    continue

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow("Object detector", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord("q"):
        break

# Clean up
video.release()
cv2.destroyAllWindows()

