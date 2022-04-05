import torch
import cv2
import pandas as pd
from box2number import Inference_gauge
mapping = Inference_gauge(None, None)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
video = "many_40cm.mp4"

frame_cnt = 0
cap = cv2.VideoCapture(video)
if not cap.isOpened():
    print("Error opening video stream or file")
print("Starting Needle Detection...\n")

while cap:
    frame_cnt+=1
    ret, image = cap.read()
    if not ret:
        print("No Frame")
        break
    results = model(image, size=640)
    pandas_results = results.pandas().xyxy[0]
    df = pd.DataFrame(pandas_results)
    df_list = df[['xmin', 'ymin', 'xmax', 'ymax', 'class']].values.tolist()
    mapping.result(df_list)
    # [
    # [126.19498443603516, 39.42572021484375, 477.67144775390625, 1080.0, 0.0],
    # [840.2291259765625, 31.248046875, 1086.451904296875, 1080.0, 0.0],
    # [1453.159423828125, 46.44621276855469, 1780.2269287109375, 1080.0, 0.0]
    # ]

