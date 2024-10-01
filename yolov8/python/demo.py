# -*- coding: utf-8 -*-
# @Time    : 2024/9/16 21:59
# @Author  : Lee
# @Project ：yolov7 
# @File    : demo.py


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


def preprocess(image_path, length):
    image = cv2.imdecode(np.fromfile(image_path), cv2.IMREAD_COLOR)
    height, width, _ = image.shape
    max_length = max(height, width)
    ratio = length / max_length
    new_height, new_width = int(height * ratio), int(width * ratio)
    mat_in = ncnn.Mat.from_pixels_resize(image, ncnn.Mat.PixelType.PIXEL_BGR2RGB, width, height, new_width, new_height)
    top, bottom, left, right = (length - new_height) // 2, length - new_height - (length - new_height) // 2, (
            length - new_width) // 2, length - new_width - (length - new_width) // 2
    mat_in_pad = ncnn.copy_make_border(mat_in, top, bottom, left, right, ncnn.BorderType.BORDER_CONSTANT, 114)
    mat_in_pad.substract_mean_normalize([0, 0, 0], [1 / 225, 1 / 225, 1 / 225])
    return image, mat_in_pad, top, left, ratio


def infer(param_path, bin_path, mat):
    net = ncnn.Net()

    net.opt.use_vulkan_compute = False
    net.opt.num_threads = 4

    net.load_param(param_path)
    net.load_model(bin_path)
    extractor = net.create_extractor()

    extractor.input("in0", mat)
    ret, output = extractor.extract("out0")
    output = np.array(output)

    return output


def postprocess(image, output, conf_thresh, iou_thresh, top, left, ratio):
    boxes = output[:, :4]
    confs = output[:, 4]

    classes = output[:, 5:]
    boxes = boxes[np.where(confs > conf_thresh)]
    confs = confs[np.where(confs > conf_thresh)]
    classes = classes[np.where(confs > conf_thresh)]

    indexes = cv2.dnn.NMSBoxes(boxes, confs, conf_thresh, iou_thresh)

    for index in indexes:
        cls = np.argmax(classes[index])
        print(classes[index].shape)
        print(cls)
        conf = confs[index]
        box = boxes[index]
        x, y, w, h = box[0], box[1], box[2], box[3]
        x1, y1, x2, y2 = int((x - w / 2 - left) / ratio), int((y - h / 2 - top) / ratio), int(
            (x + w / 2 - left) / ratio), int(
            (y + h / 2 - top) / ratio)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255 // int((cls + 1)), 255 // int((cls + 1)), 255 // int((cls + 1))), 2, 0)
        cv2.putText(image, "{}".format(CLASSES[cls]), (x1, y1+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(image, "{}".format(conf), (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return image


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, help="", default="inference/images/image2.jpg")
    parser.add_argument("--length", type=int, help="", default=640)
    parser.add_argument("--param_path", type=str, help="", default="yolov7.torchscript.ncnn.param")
    parser.add_argument("--bin_path", type=str, help="", default="yolov7.torchscript.ncnn.bin")
    parser.add_argument("--conf_thresh", type=float, help="", default=0.25)
    parser.add_argument("--iou_thresh", type=float, help="", default=0.45)
    return parser.parse_args(argv)


def main(args):
    image, mat, top, left, ratio = preprocess(args.image_path, args.length)
    output = infer(args.param_path, args.bin_path, mat)
    image = postprocess(image, output, args.conf_thresh, args.iou_thresh, top, left, ratio)
    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
