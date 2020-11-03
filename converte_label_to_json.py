#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 下午9:02
# @Author  : ChengLu
# @File    : converte_label_to_json.py
# @Contact : 2854859592@qq.com
import json
import os

import numpy as np


def poly2rbox_single(poly):
    """
    poly:[x0,y0,x1,y1,x2,y2,x3,y3]
    to
    rrect:[x_ctr,y_ctr,w,h,angle]
    """
    poly = np.array(poly[:8], dtype=np.float64)
    pt1 = (poly[0], poly[1])
    pt2 = (poly[2], poly[3])
    pt3 = (poly[4], poly[5])
    pt4 = (poly[6], poly[7])
    edge1 = np.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) +
                    (pt1[1] - pt2[1]) * (pt1[1] - pt2[1]))
    edge2 = np.sqrt((pt2[0] - pt3[0]) * (pt2[0] - pt3[0]) +
                    (pt2[1] - pt3[1]) * (pt2[1] - pt3[1]))
    angle = 0
    width = 0
    height = 0
    if edge1 > edge2:

        width = edge1
        height = edge2
        angle = np.arctan2(
            np.float(pt2[1] - pt1[1]), np.float(pt2[0] - pt1[0]))
    elif edge2 >= edge1:
        width = edge2
        height = edge1
        angle = np.arctan2(
            np.float(pt4[1] - pt1[1]), np.float(pt4[0] - pt1[0]))
    if angle > np.pi*3/4:
        angle -= np.pi
    if angle < -np.pi/4:
        angle += np.pi
    x_ctr = np.float(pt1[0] + pt3[0]) / 2
    y_ctr = np.float(pt1[1] + pt3[1]) / 2
    rbox = [x_ctr, y_ctr, width, height, angle]
    return rbox

def convert(src, des):
    """
    txt 转化 为json
    :param src: txt的文件夹路径
    :param des: json文件名
    :return:
    """
    label_files = os.listdir(src)
    annotations = []
    for label_file in label_files:
        with open(os.path.join(src, label_file), 'r') as f:
            labels_txt = f.readlines()
            # img = Image.open(os.path.join(image_save_path, data['HRSC_Image']['Img_FileName'] + ".tif"))
            # w = img.width
            # h = img.height
            bboxes = []
            labels = []
            for label_txt in labels_txt:
                data = label_txt.split(' ')
                poly = [int(data[i]) for i in range(1, 9)]
                rbox = poly2rbox_single(poly)
                bboxes.append(rbox)
                labels.append(data[0])

                label = {
                    "filename": label_file.split('.')[0] + ".tif",
                    "id": int(label_file.split('.')[0]),
                    "width": 1024,
                    "height": 1024,
                    "annotations": {
                        "bboxes": bboxes,
                        "labels": labels,
                        "bboxes_ignore": [],
                        "labels_ignore": []
                    }
                }
            annotations.append(label)
        with open(des, 'w') as f:
            f.write(json.dumps(annotations))


if __name__ == '__main__':
    src = r"C:\Users\DF\Desktop\newLabel"
    des = r"C:\Users\DF\Desktop\annotation_new.json"
    convert(src, des)



