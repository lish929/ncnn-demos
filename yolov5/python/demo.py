# -*- coding: utf-8 -*-
# @Time    : 2024/9/24 10:16
# @Author  : Lee
# @File    : demo.py
# @Description :


import argparse
import cv2
import ncnn
import numpy as np
import sys

CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
    'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
    'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle',
    'wine glass', 'cup', 'fork', 'knife', 'spoon',
    'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut',
    'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
    'toaster', 'sink', 'refrigerator', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

ANCHORS = [
    [10, 13, 16, 30, 33, 23],
    [30, 61, 62, 45, 59, 119],
    [116, 90, 156, 198, 373, 326]
]

class Processor(object):
    def __init__(self):
        super().__init__()

    def preprocess(self, image_path, input_size):
        # 图片下部分会产生黑边？
        # image = cv2.imdecode(np.fromfile(image_path), cv2.IMREAD_COLOR)
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        max_length = max(height, width)
        ratio = input_size / max_length
        new_height, new_width = int(height * ratio), int(width * ratio)
        mat_in = ncnn.Mat.from_pixels_resize(image, ncnn.Mat.PixelType.PIXEL_BGR2RGB, width, height, new_width,
                                             new_height)
        top, bottom, left, right = (input_size - new_height) // 2, input_size - new_height - (
                input_size - new_height) // 2, (
                                           input_size - new_width) // 2, input_size - new_width - (
                                           input_size - new_width) // 2
        mat_in_pad = ncnn.copy_make_border(mat_in, top, bottom, left, right, ncnn.BorderType.BORDER_CONSTANT, 114)
        mat_in_pad.substract_mean_normalize([0, 0, 0], [1 / 255.0, 1 / 255.0, 1 / 255.0])
        return image, mat_in_pad, top, left, ratio

    def postprocess(self, image, mat, outputs, conf_thresh, nms_thresh, top, left, ratio):
        boxes,confs,classes = None,None,None
        for i, output in enumerate(outputs):
            output = 1 / (1 + np.exp(-output))
            xy, wh, conf,cls = output[:, :, 0:2], output[:, :, 2:4], output[:, :, 4],output[:, :, 5:]
            y,x = np.arange(mat.h / (8 * 2**i)),np.arange(mat.w / (8 * 2**i))
            yv,xv = np.meshgrid(y,x)
            print(yv,xv)
            grids = (np.expand_dims(np.stack((yv,xv),axis=2),axis=0).repeat(3,axis=0)-0.5).reshape(len(ANCHORS[i])//2,-1,2)
            print(grids.shape)
            print(grids)
            xy = (xy * 2+grids)*8*2**i
            anchor_grids = []
            for j in range(len(ANCHORS[i])//2):
                h,w = ANCHORS[i][j*2],ANCHORS[i][j*2+1]
                anchor_grids.append(np.reshape(np.expand_dims(np.expand_dims(np.array([h,w]),axis=0).repeat(mat.h / (8 * 2**i),axis=0),axis=0).repeat(mat.w / (8 * 2**i),axis=0),(-1,2)))
            anchor_grids = np.array(anchor_grids)
            wh = (wh*2)**2*anchor_grids
            if i == 0:
                boxes = np.concatenate((xy.reshape(-1,xy.shape[-1]),wh.reshape(-1,wh.shape[-1])),axis=1)
                confs = conf.reshape(-1)
                classes = cls.reshape(-1,cls.shape[-1])
            else:
                boxes = np.concatenate((boxes,np.concatenate((xy.reshape(-1,xy.shape[-1]),wh.reshape(-1,wh.shape[-1])),axis=1)),axis=0)
                confs = np.concatenate((confs,conf.reshape(-1)),axis=0)
                classes = np.concatenate((classes,cls.reshape(-1,cls.shape[-1])),axis=0)
        indexes = cv2.dnn.NMSBoxes(boxes, confs, conf_thresh, nms_thresh)
        for index in indexes:
            box = boxes[index]
            conf = confs[index]
            cls = np.argmax(classes[index])
            xc, yc, w, h = box
            x1, y1, x2, y2 = int(((xc - w / 2) - left) / ratio), int(((yc - h / 2) - top) / ratio), int(
                ((xc + w / 2) - left) / ratio), int(((yc + h / 2) - top) / ratio)
            cv2.rectangle(image, (x1, y1), (x2, y2),
                          (255 // int((cls + 1)), 255 // int((cls + 1)), 255 // int((cls + 1))), 2, 0)
            cv2.putText(image, "{}".format(CLASSES[cls]), (x1, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "{}".format(conf), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return image


class Detector(object):
    def __init__(self, param_path, bin_path):
        super().__init__()
        self.extractor = self.create_extractor(param_path, bin_path)

    def create_extractor(self, param_path, bin_path):
        net = ncnn.Net()
        net.opt.use_vulkan_compute = False
        net.opt.num_threads = 4
        net.load_param(param_path)
        net.load_model(bin_path)
        extractor = net.create_extractor()

        return extractor

    def infer(self, mat):
        self.extractor.input("in0", mat)
        ret1, output1 = self.extractor.extract("out0")
        ret2, output2 = self.extractor.extract("out1")
        ret3, output3 = self.extractor.extract("out2")
        output1 = np.array(output1)
        output2 = np.array(output2)
        output3 = np.array(output3)
        return [output1, output2, output3]


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, help="", default="../datas/bus.jpg")
    parser.add_argument("--input_size", type=int, help="", default=640)
    parser.add_argument("--param_path", type=str, help="", default="../models/yolov5n.ncnn.param")
    parser.add_argument("--bin_path", type=str, help="", default="../models/yolov5n.ncnn.bin")
    parser.add_argument("--conf_thresh", type=float, help="", default=0.25)
    parser.add_argument("--nms_thresh", type=float, help="", default=0.45)
    return parser.parse_args(argv)


def main(args):
    processor = Processor()
    detector = Detector(args.param_path, args.bin_path)
    image, mat, top, left, ratio = processor.preprocess(args.image_path, args.input_size)
    outputs = detector.infer(mat)
    image = processor.postprocess(image, mat, outputs, args.conf_thresh, args.nms_thresh, top, left, ratio)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
