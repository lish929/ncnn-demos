#include "classification.h"

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>


extern "C" __declspec(dllimport) int init();       
extern "C" __declspec(dllimport) int infer(const cv::Mat& image,cv::Mat& outputs);  
extern "C" __declspec(dllimport) int draw(const cv::Mat& image,cv::Mat& outputs);


int main(){
    cv::Mat image = cv::imread("D:/project/ncnn-demos/resnet/c++/cat.jpg");
    cv::Mat1f outputs;
    init();
    infer(image,outputs);
    draw(image,outputs);
    return 0;
}