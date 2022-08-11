IMAGE_MOD = True
IMAGE_PATH = "test_image"
import glob
import os
import sys

import cv2
import pandas as pd
import pymysql
import torch

from box2number import Inference_result

mapping = Inference_result(None, None)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='miraes/exp2/weights/last.pt')
video = "test.mov"
# test_db = pymysql.connect(
#     user='root',
#     passwd='mysql',
#     host='192.168.0.5',
#     db='TESTDB',
#     charset='utf8'
# )
frame_cnt = 0
cap = cv2.VideoCapture(video)
if not cap.isOpened():
    print("Error opening video stream or file")
print("Starting Needle Detection...\n")

if IMAGE_MOD:
    # cursor = test_db.cursor()
    image_list = glob.glob(os.path.abspath(IMAGE_PATH+"/*.jpg"))
    print("image_list", image_list)
    frame_cnt = 0
    for image_path in image_list:

        image = cv2.imread(image_path)
        results = model(image, size=640)
        # results.show()
        pandas_results = results.pandas().xyxy[0]
        df = pd.DataFrame(pandas_results)
        df_list = df[['xmin', 'ymin', 'xmax', 'ymax', 'class']].values.tolist()
        print(image_path)
        result_pos = mapping.result(df_list)
        cv2.putText(image, str(result_pos), (10, 110), fontFace=0, fontScale=2, thickness=3, color=(0, 0, 0))
        for df in df_list:
            cv2.rectangle(image, (int(df[0]), int(df[1])), ((int(df[2]), int(df[3]))), color=(0, 0, 255))
            if df[4] == 1:
                a = df[0]
                b = df[1]*0.66+df[3]*0.34
                c = df[2]
                d = b

                cv2.line(image, (int(a), int(b)), (int(c), int(d)), color=(255,0,0), thickness=1)
        # sql = "INSERT INTO tb VALUES (%s)"
        # try:
        #     cursor.execute(sql, result_pos)
        # except:
        #     cursor.execute(sql, -1)
        # test_db.commit()
        # data_list=cursor.fetchall()
        save_dir = os.path.abspath("test_result/" + image_path.split("\\")[-1] + ".jpg")
        cv2.imwrite(save_dir, image)
        frame_cnt+=1
#     test_db.close()
    sys.exit()


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
    df = pd.DataFrame(pandas_results)
    df_list = df[['xmin', 'ymin', 'xmax', 'ymax', 'class']].values.tolist()

    result_pos = mapping.result(df_list)
    cv2.putText(image, str(result_pos),(10, 110),fontFace=0, fontScale=2, thickness=3, color=(0, 0, 0))
    for df in df_list:
        cv2.rectangle(image, (int(df[0]), int(df[1])),((int(df[2]), int(df[3]))),color=(0,0,255))
    save_dir = os.path.abspath("result/"+str(frame_cnt)+".jpg")
    print(save_dir)
    cv2.imwrite(save_dir, image)
    # [
    # [126.19498443603516, 39.42572021484375, 477.67144775390625, 1080.0, 0.0],
    # [840.2291259765625, 31.248046875, 1086.451904296875, 1080.0, 0.0],
    # [1453.159423828125, 46.44621276855469, 1780.2269287109375, 1080.0, 0.0]
    # ]



