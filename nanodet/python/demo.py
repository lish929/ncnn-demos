# -*- coding: utf-8 -*-
# @Time    : 2024/9/23 21:29
# @Author  : Lee
# @Project ：nanodet 
# @File    : demo.py


import argparse
import cv2
import ncnn
import numpy as np
import sys


class Processor(object):
    def __init__(self):
        super().__init__()

    def preprocess(self, image_path, input_size):
        image = cv2.imdecode(np.fromfile(image_path), cv2.IMREAD_COLOR)
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
        # [[103.53, 116.28, 123.675], [57.375, 57.12, 58.395]]
        mat_in_pad.substract_mean_normalize([103.53, 116.28, 123.675], [1 / 57.375, 1 / 57.12, 1 / 58.395])
        return image, mat_in_pad, top, left, ratio

    def postprocess(self,output,conf_thresh,nms_thresh):
        output = np.transpose(output,(1,0))
        classes = output[:,0:80]
        confs = np.max(classes,axis=1)
        print(confs.shape)
        classes = np.argmax(classes,axis=1)
        print(classes.shape)
        print(classes)
        boxes = output[:,80:]
        regs = np.arange(8)
        for i,conf in enumerate(confs):
            if conf > conf_thresh:
                box = boxes[i]
                box = np.exp(box) / np.sum(np.exp(box))
                box = box.reshape(-1,8)
                print(classes[i])


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
    parser.add_argument("--image_path", type=str, help="", default="../datas/zidane.jpg")
    parser.add_argument("--input_size", type=int, help="", default=320)
    parser.add_argument("--param_path", type=str, help="", default="../models/nanodet_m_0.5x.torchscript.ncnn.param")
    parser.add_argument("--bin_path", type=str, help="", default="../models/nanodet_m_0.5x.torchscript.ncnn.bin")
    parser.add_argument("--conf_thresh", type=float, help="", default=0.25)
    parser.add_argument("--nms_thresh", type=float, help="", default=0.45)
    return parser.parse_args(argv)


def main(args):
    processor = Processor()
    detector = Detector(args.param_path, args.bin_path)
    image, mat, top, left, ratio = processor.preprocess(args.image_path, args.input_size)
    output = detector.infer(mat)
    processor.postprocess(output,args.conf_thresh,args.nms_thresh)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
