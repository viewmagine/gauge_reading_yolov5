import argparse
import glob

import cv2
import torch
import random
from detectors.gauge_detector import gauge_detector as GD
from detectors.needle_detector import needle_detector as ND
from helper.inference_gauge_by_box import Inference_gauge
from json_parser import json2path



def inference(DISPLAY, SAVE_CROPPED=True):
    gauge_detector = GD(gauge_model, gauge_label, video, device=device)
    needle_detector = ND(needle_model, needle_label, video, device=device)
    Gboxes, gauge_image = gauge_detector.bboxes()
    Gboxes = adjust_crop_pos(Gboxes, gauge_image)

    if DISPLAY is True:
        gauge_detector.show_gauge(Gboxes, gauge_image)
    frame_cnt = 0
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("Error opening video stream or file")
    print("Starting Needle Detection...\n")

    while True:
        frame_cnt += 1
        ret, image = cap.read()
        if not ret:
            print("No Frame")
            break
        box_num = 0
        for box in Gboxes:
            cropped_image = image[int(box[1]):int(box[3]),
                            int(box[0]):int(box[2])]
            if SAVE_CROPPED:
                if random.random()<0.005:
                    cv2.imwrite('dataset/needle_dataset/annotate_here/'+str(random.randint(10000, 100000))+'.jpg', cropped_image)
            pos, labels, probs = needle_detector.bboxes(cropped_image)
            if len(pos) == 0:
                print("Nothing Out! from ", box_num)
            else:
                print("Out! from", box_num)
            box_num+=1
            for i in range(pos.size(0)):
                box = pos[i, :]
                label = f"{labels[i]}: {probs[i]:.2f}"
                cv2.rectangle(cropped_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 255, 0), 4)

                cv2.putText(cropped_image, label,
                            (int(box[0]) + 20, int(box[1]) + 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,  # font scale
                            (255, 0, 255),
                            2)  # line type
                cv2.imshow("sda", cropped_image)
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
    cap.release()
    cv2.destroyAllWindows()


def adjust_crop_pos(crop_pos, image):
    for single_crop_pos in crop_pos:
        if single_crop_pos[2] > image.shape[1]:
            single_crop_pos[2] = image.shape[1]
        if single_crop_pos[3] >= image.shape[0]:
            single_crop_pos[3] = image.shape[0]
        if single_crop_pos[0] < 0:
            single_crop_pos[0] = 0
        if single_crop_pos[1] <= 0:
            single_crop_pos[1] = 0
    return crop_pos


if __name__ == "__main__":
    NUM_OF_GAUGES = 3
    json_path 2= "settings.json"
    device = ['cuda:0' if torch.cuda.is_available() else 'cpu']
    p_dataset, p_exp, video, gauge_model, needle_model = json2path(json_path).parse2()
    gauge_label = "labels/gauge_label.txt"
    needle_label = "labels/needle_label.txt"
    inference(DISPLAY=True)
    # python main.py --gauge_exp 10016 --gauge_epoch 119 --needle_exp 10012 --needle_epoch 40
    # needle_cutter()