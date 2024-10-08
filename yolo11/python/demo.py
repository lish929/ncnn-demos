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

class Processor(object):
    def __init__(self):
        super().__init__()

    def preprocess(self, image_path, input_shape):
        # 图片下部分会产生黑边？
        # image = cv2.imdecode(np.fromfile(image_path), cv2.IMREAD_COLOR)
        image = cv2.imread(image_path)
        shape,new_shape,top,bottom,left,right,r=self.letterbox(image,input_shape)
        mat_in = ncnn.Mat.from_pixels_resize(image, ncnn.Mat.PixelType.PIXEL_BGR2RGB, shape[1], shape[0], new_shape[0],
                                             new_shape[1])

        mat_in_pad = ncnn.copy_make_border(mat_in, top, bottom, left, right, ncnn.BorderType.BORDER_CONSTANT, 114)
        mat_in_pad.substract_mean_normalize([0, 0, 0], [1 / 255.0, 1 / 255.0, 1 / 255.0])
        return image, mat_in_pad, top, left, r

    def letterbox(self,image,input_shape,stride=32,auto=False,center=True):

        shape = image.shape[:2]
        if isinstance(input_shape,int):
            input_shape = input_shape,input_shape
        r = min(input_shape[0] / shape[0], input_shape[1] / shape[1])

        new_shape = int(round(shape[1] * r)), int(round(shape[0] * r))

        pad_w, pad_h = input_shape[1] - new_shape[0], input_shape[0] - new_shape[1]
        if auto:
            pad_w, pad_h = np.mod(pad_w, stride), np.mod(pad_h, stride)

        if center:
            pad_w /= 2
            pad_h /= 2

        top, bottom = int(round(pad_h - 0.1)) if center else 0, int(round(pad_h + 0.1))
        left, right = int(round(pad_w - 0.1)) if center else 0, int(round(pad_w + 0.1))

        return shape,new_shape,top,bottom,left,right,r


    def postprocess(self, image, output, conf_thresh, nms_thresh, top, left, ratio):
        output = np.transpose(output,(1,0))
        indexes = np.where(np.max(output[:,4:],axis=1)>=conf_thresh)
        output = output[indexes]
        boxes,confs,classes = output[:,:4],np.max(output[:,4:],axis=1),np.argmax(output[:,4:],axis=1)
        ids = cv2.dnn.NMSBoxes(boxes,confs,conf_thresh,nms_thresh)
        for id in ids:
            box = boxes[id]
            conf = confs[id]
            cls = classes[id]
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
        ret, output = self.extractor.extract("out0")
        output = np.array(output)
        return output


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, help="", default="../../datas/bus.jpg")
    parser.add_argument("--input_shape", type=int, help="", default=640)
    parser.add_argument("--param_path", type=str, help="", default="../models/model.ncnn.param")
    parser.add_argument("--bin_path", type=str, help="", default="../models/model.ncnn.bin")
    parser.add_argument("--conf_thresh", type=float, help="", default=0.25)
    parser.add_argument("--nms_thresh", type=float, help="", default=0.7)
    return parser.parse_args(argv)


def main(args):
    processor = Processor()
    detector = Detector(args.param_path, args.bin_path)
    image, mat, top, left, ratio = processor.preprocess(args.image_path, args.input_shape)
    output = detector.infer(mat)
    image = processor.postprocess(image, output, args.conf_thresh, args.nms_thresh, top, left, ratio)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
