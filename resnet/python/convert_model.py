import argparse
import os
import torch


def convert_torchscript(model_path,input_shape):
    model = torch.load(model_path)
    model.eval()
    x = torch.randn(input_shape)
    model = torch.jit.trace(model,x)
    model.save("../models/resnet_18.torchscript")
    return model

# 使用pnnx进行转换
def convert_ncnn(env_name,model_path,):
    cmd = "conda activate {} && pnnx {} inputshape=[1,3,224,224]".format(env_name,model_path)
    print(cmd)
    try:
        os.system(cmd)
    except Exception as e:
        print(e)
        return "model convert failed!"
    return "model convert success!"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_name",type=str,help="",default="yolov5")
    parser.add_argument("--pt_path",type=str,help="",default="../models/resnet_18.pt")
    parser.add_argument("--torchscript_path",type=str,help="",default="../models/resnet_18.torchscript")
    parser.add_argument("--input_shape",type=list,help="",default=[1,3,224,224])
    args = parser.parse_args()

    model = convert_torchscript(args.pt_path,args.input_shape)
    print(model)
    info = convert_ncnn(args.env_name,args.torchscript_path)
    print(info)