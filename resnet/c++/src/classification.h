#ifndef _CLASSIFICATION_H_
#define _CLASSIFICATION_H_

#ifdef LIB_EXPORTS
    #define LIB_API __declspec(dllexport)
#else
    #define LIB_API __declspec(dllimport)
#endif

#include <opencv2/core/core.hpp>

extern "C"{
    LIB_API int init();
    LIB_API int infer(const cv::Mat& image,cv::Mat& outputs);
    LIB_API int draw(const cv::Mat& image,cv::Mat& outputs);
}

#endif
