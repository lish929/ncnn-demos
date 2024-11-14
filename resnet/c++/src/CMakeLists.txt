cmake_minimum_required(VERSION 3.20)

project(resnet)

add_definitions(-DLIB_EXPORTS)

# set(OpenCV_DIR D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib)
# find_package(OpenCV REQUIRED)
set(OpenCV_INCLUDE_DIRS D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/include)
set(NCNN_INCLUDE_DIRS D:/project/ncnn-demos/resnet/c++/src/res/ncnn/include)

include_directories(${OpenCV_INCLUDE_DIRS} ${NCNN_INCLUDE_DIRS})

aux_source_directory(D:/project/ncnn-demos/resnet/c++/src SOURCES)

add_library(${PROJECT_NAME} SHARED ${SOURCES})

set(NCNN_LIBS D:/project/ncnn-demos/resnet/c++/src/res/ncnn/lib/ncnn.lib)

target_link_libraries(${PROJECT_NAME} ${NCNN_LIBS})
target_link_libraries(${PROJECT_NAME} D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib/opencv_core4100.lib)
target_link_libraries(${PROJECT_NAME} D:/project/ncnn-demos/resnet/c++/src/res/opencv-mobile/lib/opencv_imgproc4100.lib)

