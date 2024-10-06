# CMakeList.txt: ncnn-demo 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)

# include_directories("D:/yolo/ncnn-demos/opencv/include")
include_directories("D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/include")
# include_directories("D:/opencv-mobile-4.10.0-windows-vs2019/x64/include")
include_directories("D:/yolo/ncnn-demos/ncnn/include")

#link_directories("D:/opencv-mobile-3.4.20-windows-vs2019/x64/x64/vc16/staticlib")
# link_directories("D:/opencv-mobile-4.10.0-windows-vs2019/x64/x64/vc16/staticlib")
# link_directories("D:/ncnn-20240820-windows-vs2019/x64/lib")

# 将源代码添加到此项目的可执行文件。
add_executable (ncnn-demo "ncnn-demo.cpp" "ncnn-demo.h")

target_link_libraries(ncnn-demo PUBLIC "D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/x64/vc16/staticlib/opencv_core2413.lib")
target_link_libraries(ncnn-demo PUBLIC "D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/x64/vc16/staticlib/opencv_highgui2413.lib")
target_link_libraries(ncnn-demo PUBLIC "D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/x64/vc16/staticlib/opencv_imgproc2413.lib")
target_link_libraries(ncnn-demo PUBLIC "D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/x64/vc16/staticlib/opencv_photo2413.lib")
target_link_libraries(ncnn-demo PUBLIC "D:/opencv-mobile-2.4.13.7-windows-vs2019/x64/x64/vc16/staticlib/opencv_video2413.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/opencv_core249.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/opencv_highgui249.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/opencv_imgproc249.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/opencv_photo249.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/opencv_video249.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/opencv/staticlib/zlib.lib")

target_link_libraries(ncnn-demo PUBLIC "D:/yolo/ncnn-demos/ncnn/lib/ncnn.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/glslang.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/glslang-default-resource-limits.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/GenericCodeGen.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/MachineIndependent.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/OGLCompiler.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/OSDependent.lib")
# target_link_libraries(ncnn-demo PUBLIC "D:/ncnn-20240820-windows-vs2019/x64/lib/SPIRV.lib")

# TODO: 如有需要，请添加测试并安装目标。
