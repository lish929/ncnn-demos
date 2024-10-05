// ncnn-demo.cpp: 定义应用程序的入口点。
//

#include <ncnn/cpu.h>
#include <ncnn/net.h>
#include <ncnn/gpu.h>
#include <ncnn/benchmark.h>
#include <ncnn/datareader.h>

#include <iostream>
#include<vector>
#include<stdio.h>
#include<algorithm>

#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>

cv::Mat demo(cv::Mat& image, ncnn::Net& detector, int input_width, int input_height) {
	// 拷贝原图
	cv::Mat bgr = image.clone();
	int image_width = bgr.cols;
	int image_height = bgr.rows;
	// pad
	float scale = std::max(float(image_width / float(input_width)), float(image_height / float(input_height)));
	int scale_width = int(image_width / scale);
	int scale_height = int(image_height / scale);
	ncnn::Mat input = ncnn::Mat::from_pixels_resize(bgr.data, ncnn::Mat::PIXEL_BGR2RGB,image_width, image_height, scale_width,scale_height);
	ncnn::Mat input_pad;
	ncnn::copy_make_border(
		input,
		input_pad,
		(input_height - scale_height) / 2,
		(input_height - scale_height) - (input_height - scale_height) / 2,
		(input_width - scale_width) / 2,
		(input_width - scale_width) - (input_width - scale_width) / 2,
		ncnn::BorderType::BORDER_CONSTANT,
		114.0
	);
	// 数据预处理
	const float mean_vals[3] = { 0.f, 0.f, 0.f };
	const float norm_vals[3] = { 1 / 255.f,1 / 255.f,1 / 255.f };
	input_pad.substract_mean_normalize(mean_vals, norm_vals);

	ncnn::Extractor ex = detector.create_extractor();
	// ex.set_num_threads(8);
	ex.input("in0", input_pad);
	ncnn::Mat output;
	ex.extract("out0", output);

	cv::Mat out(output.h, output.w, CV_32F);
	float* data = out.ptr<float>(0);
	for (size_t i = 0; i < output.h; i++)
	{
		for (size_t j = 0; j < output.w; j++)
		{
			float temp = ((float*)output.data)[j + i * output.w];
			*(data + j + i * output.w) = temp;
		}
	}
	// 坐标
	cv::Mat locs = out.rowRange(0, 4);
	// 置信度
	cv::Mat confs = out.rowRange(4, out.rows);

	std::vector<float> class_confs;
	std::vector<int> class_ids;
	std::vector<cv::Rect> boxes;

	for (int i = 0; i < out.cols; i++) {

		// 根据置信度先排除部分目标
		cv::Point minLoc, maxLoc;
		double minVal, maxVal;
		cv::minMaxLoc(confs.col(i), &minVal, &maxVal, &minLoc, &maxLoc);
		
		if (maxVal < 0.8)
		{
			continue;
		}

		float cx = locs.at<float>(0,i);
		float cy = locs.at<float>(1,i);
		float w = locs.at<float>(2,i);
		float h = locs.at<float>(3,i);


		int left = int((cx - 0.5 * w-((input_width - scale_width) / 2)) * scale);
		int top = int((cy - 0.5 * h-((input_height - scale_height) / 2)) * scale);
		int width = int(w * scale);
		int height = int(h * scale);

		class_confs.push_back(maxVal);
		class_ids.push_back(maxLoc.y);
		boxes.push_back(cv::Rect(left, top, w, h));

		cv::rectangle(image, cv::Point(left, top), cv::Point(left+width, top+height), cv::Scalar(0, 0, 0), 1, 1, 0);
	}
	// 计算nms
	
	
	// std::cout << confs.size() << std::endl;
	// std::cout << maxLoc << std::endl;
	// exit(0);
	return image;
}

int main() {
	// 加载模型
	ncnn::Net detector;
	detector.load_param("D:/yolo/ultralytics/yolov8n_ncnn_model/model.ncnn.param");
	detector.load_model("D:/yolo/ultralytics/yolov8n_ncnn_model/model.ncnn.bin");
	// 定义输入图像尺寸
	int input_width = 640;
	int input_height = 640;
	// 读取图像
	// 编译的opencv有错 读取图片为[] 换用opencv-mobile
	cv::Mat image = cv::imread("D:/yolo/ultralytics/ultralytics/assets/bus.jpg");
	// std::cout << image << std::endl;
	// 调用函数开始检测
	cv::Mat image_draw = demo(image, detector, input_width, input_height);
	// 保存检测结果
	cv::imwrite("out.jpg", image_draw);

	return 0;
}

