import streamlit as st
import cv2
from PIL import Image
import numpy as np
MODEL = "model/MobileNetSSD_deploy.caffemodel "
PROTOTXT = "model/MobileNetSSD_deploy.prototxt.txt "


def process_image(image):
    blob = cv2 . dnn . blobFromImage(
        cv2 . resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net = cv2 . dnn . readNetFromCaffe(PROTOTXT, MODEL)
    net . setInput(blob)
    detections = net . forward()
    return detections


def annotate_image(image, detection, confidence_threshold=0.5):
    (h, w) = image.shape[:2]
    for i in np.arange(0, detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > confidence_threshold:
            box = detection[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = box . astype("int")
            cv2 . rectangle(image, (start_x, start_y), (end_x, end_y), 70, 2)
    return image


st.title("Object detection")
file = st.file_uploader('Upload Image File: ', type=['jpg', 'png', 'jpeg'])

if file is not None:
    st.image(file)
    image = Image.open(file)
    image = np.array(image)
    detection = process_image(image)
    process_image = annotate_image(image, detection)
    st.image(process_image)
