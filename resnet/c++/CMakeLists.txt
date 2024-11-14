cmake_minimum_required(VERSION 3.20)

project(main)

set(INCLUDE_DIR D:/project/ncnn-demos/resnet/c++/src)
set(OpenCV_DIR D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/include)

include_directories(${INCLUDE_DIR} ${OpenCV_DIR})

add_executable(main main.cpp)

set(LIB D:/project/ncnn-demos/resnet/c++/src/build/Release/resnet.lib)

target_link_libraries(main ${LIB})
target_link_libraries(${PROJECT_NAME} D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib/opencv_highgui4100.lib)
target_link_libraries(${PROJECT_NAME} D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib/opencv_core4100.lib)
target_link_libraries(${PROJECT_NAME} D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib/opencv_imgproc4100.lib)
