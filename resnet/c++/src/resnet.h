#ifndef _MODEL_H_
#define _MODEL_H_

#include <string>
#include <vector>

#include <opencv2/core/core.hpp>
#include <ncnn/net.h>


class ResNet{
public:
    ResNet();
    ~ResNet();
    // 模型初始化
    int Init(const char* model_name,int input_size,const float* means,const float* stds,bool use_gpu);
    // 推理
    int Infer(const cv::Mat& image,cv::Mat& outputs);

private:
    ncnn::Net net;
    // 推理输入尺寸
    int input_size;
    // normalize data
    float means[3];
    float stds[3];

};


#endif