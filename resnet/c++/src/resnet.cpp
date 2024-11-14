#include "resnet.h"

#include <ncnn/cpu.h>
#include <ncnn/mat.h>

ResNet::ResNet(){

}

int ResNet::Init(const char* model_name,int input_size_,const float* means_,const float* stds_,bool use_gpu){
    // 清空网络
    net.clear();
    // 网络配置
    net.opt = ncnn::Option();

// 设置是否使用vulkan加速
#if NCNN_VULKAN
    net.opt.use_vulkan_compute = use_gpu;
#endif
    // 设置线程数  
    net.opt.num_threads = ncnn::get_big_cpu_count();
    // 加载模型
    char param_path[256];
    char bin_path[256];
    sprintf(param_path,"./models/%s.ncnn.param",model_name);
    sprintf(bin_path,"./models/%s.ncnn.bin",model_name);
    net.load_param(param_path);
    net.load_model(bin_path);    
    // 初始化 input size normalize data
    input_size = input_size_;
    std::copy(means_,means_+3,means);
    std::copy(stds_,stds_+3,stds);

    return 0;
}

int ResNet::Infer(const cv::Mat& image,cv::Mat& outputs){
    // 获取图像宽高
    int width = image.cols;
    int height = image.rows;
    // 图像预处理
    ncnn::Mat mat = ncnn::Mat::from_pixels_resize(image.data,ncnn::Mat::PixelType::PIXEL_BGR2RGB,width,height,input_size,input_size);
    mat.substract_mean_normalize(means,stds);
    // 创建extractor
    ncnn::Extractor ex = net.create_extractor();
    // 推理
    ex.input("in0",mat);
    // 获取结果
    ncnn::Mat results;
    ex.extract("out0",results);
    // ncnn mat转opencv mat
    memcpy((uchar*)outputs.data,results.data,results.w*results.h*sizeof(float));

    return 0;
}


