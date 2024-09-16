# -*- coding: utf-8 -*-
# @Time    : 2024/9/16 21:59
# @Author  : Lee
# @Project ：yolov7 
# @File    : demo.py


import argparse
import cv2
import ncnn
import numpy as np
import os
import sys


def preprocess(image_path,length):
    image = cv2.imdecode(np.fromfile(image_path),cv2.IMREAD_COLOR)
    height, width, _ = image.shape
    max_length = max(height, width)
    ratio = length / max_length
    new_height,new_width = int(height*ratio),int(width*ratio)
    mat_in = ncnn.Mat.from_pixels_resize(image,ncnn.Mat.PixelType.PIXEL_BGR2RGB,width,height,new_width,new_height)
    top,bottom,left,right = (length-new_height)//2,length-new_height-(length-new_height)//2,(length-new_width)//2,length-new_width-(length-new_width)//2
    mat_in_pad = ncnn.copy_make_border(mat_in,top,bottom,left,right,ncnn.BorderType.BORDER_CONSTANT,114)
    mat_in_pad.substract_mean_normalize([0, 0, 0], [1 / 225, 1 / 225, 1 / 225])
    return mat_in_pad

def infer(param_path,bin_path,mat):
    net = ncnn.Net()

    net.opt.use_vulkan_compute = False
    net.opt.num_threads = 4

    net.load_param(param_path)
    net.load_model(bin_path)
    extractor = net.create_extractor()

    extractor.input("in0",mat)
    ret,output = extractor.extract("out0")

    output = np.array(output)
    return output

def postprocess(output):
    output = output.reshape(3,85,20,20)

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path",type=str,help="",default="inference/images/bus.jpg")
    parser.add_argument("--length",type=int,help="",default=640)
    parser.add_argument("--param_path",type=str,help="",default="yolov7.torchscript.ncnn.param")
    parser.add_argument("--bin_path",type=str,help="",default="yolov7.torchscript.ncnn.bin")
    return parser.parse_args(argv)

def main(args):
    mat = preprocess(args.image_path,args.length)
    output = infer(args.param_path,args.bin_path,mat)
    print(output.shape)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))