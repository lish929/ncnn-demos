#define LIB_EXPORTS

#include "classification.h"
#include "resnet.h"

#include <iostream>

struct ModelOption
{
    char* model_name = "resnet_18";

    int input_size = 224;
    float means[3] = {0.485*255.0,0.456*255.0,0.406*255.0};
    float stds[3] = {1/0.229/255.0, 1/0.224/255.0, 1/0.225/255.0};

    bool use_gpu = true;
};


ResNet* net = 0;
ModelOption opt;

extern "C"{
    LIB_API int init(){
        net->Init(opt.model_name,opt.input_size,opt.means,opt.stds,opt.use_gpu);
        return 0;
    }

    LIB_API int infer(const cv::Mat& image,cv::Mat& outputs){
        net->Infer(image,outputs);
        return 0;
    }

    LIB_API int draw(const cv::Mat& image,cv::Mat& outputs){
        double min_value, max_value;
        cv::Point  min_idx, max_idx;  
        cv::minMaxLoc(outputs,&min_value,&max_value,&min_idx,&max_idx);
        std::cout<<"类别："<<std::to_string(max_idx.x)<<std::endl;
        std::cout<<"置信度："<<std::to_string(max_value)<<std::endl;
        // cv::putText(image,std::to_string(max_value),cv::Point(10,20),1,1.0,cv::Scalar(0,0,255),1);
        // cv::putText(image,std::to_string(max_idx.x),cv::Point(10,20),1,1.0,cv::Scalar(0,0,255),1);
        return 0;
    }
}
