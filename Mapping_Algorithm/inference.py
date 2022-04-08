import torch
import cv2
import pandas as pd
from box2number import Inference_result
import os
import glob
import time
mapping = Inference_result(None, None)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='miraes/exp2/weights/best.pt')
video = "test.mov"

frame_cnt = 0
cap = cv2.VideoCapture(video)
if not cap.isOpened():
    print("Error opening video stream or file")
print("Starting Needle Detection...\n")

while cap:
    frame_cnt+=1
    ret, image = cap.read()
    if frame_cnt%10 !=0:
        continue
    print(frame_cnt)
    if not ret:
        print("No Frame")
        break
    results = model(image, size=640)
    # results.show()
    pandas_results = results.pandas().xyxy[0]
    print(pandas_results)
    df = pd.DataFrame(pandas_results)
    df_list = df[['xmin', 'ymin', 'xmax', 'ymax', 'class']].values.tolist()
    result_pos = mapping.result(df_list)
    print(result_pos)
    # cv2.putText(image, str(result_pos),(10, 110),fontFace=0, fontScale=2, thickness=3, color=(0, 0, 0))
    # for df in df_list:
    #     cv2.rectangle(image, (int(df[0]), int(df[1])),((int(df[2]), int(df[3]))),color=(0,0,255))
    # save_dir = os.path.abspath("result/"+str(frame_cnt)+".jpg")
    # print(save_dir)
    # cv2.imwrite(save_dir, image)
    # [
    # [126.19498443603516, 39.42572021484375, 477.67144775390625, 1080.0, 0.0],
    # [840.2291259765625, 31.248046875, 1086.451904296875, 1080.0, 0.0],
    # [1453.159423828125, 46.44621276855469, 1780.2269287109375, 1080.0, 0.0]
    # ]



