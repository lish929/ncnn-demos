@Rem 编译opencv静态库

set ARC=x64
set VS=2022
set BUILD_TYPE=Release
set OPENCV_ROOT=D:\ncnn_demos\opencv-2.4.9
set BUILD_DIR=D:\ncnn_demos\opencv-2.4.9\build
set INSTALL_DIR=D:\ncnn_demos\opencv-2.4.9\install

@echo off

if %ARC% == x86 (
	echo "build x86"
	call "C:\Program Files\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
) else (
	echo "build x64"
	call "C:\Program Files\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
)

if exist "%BUILD_DIR%" rd /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

@REM -DBUILD_opencv_world=ON

cmake %OPENCV_SOURCES_PATH% ^
-DCMAKE_BUILD_TYPE=%BUILD_TYPE% ^
-DCMAKE_SYSTEM_NAME=Windows ^
-DBUILD_WITH_STATIC_CRT=ON ^
-DBUILD_SHARED_LIBS=OFF ^

-DBUILD_opencv_apps=OFF ^
-DBUILD_ANDROID_EXAMPLES=OFF ^
-DBUILD_DOCS=OFF ^
-DBUILD_EXAMPLES=OFF ^
-DBUILD_PACKAGE=OFF ^
-DBUILD_PERF_TESTS=OFF ^
-DBUILD_TESTS=OFF ^
-DBUILD_WITH_DEBUG_INFO=OFF ^
-DBUILD_WITH_STATIC_CRT=OFF ^
-DBUILD_FAT_JAVA_LIB=OFF ^
-DBUILD_ANDROID_SERVICE=OFF ^
-DBUILD_ANDROID_PACKAGE=OFF ^
-DBUILD_TINY_GPU_MODULE=OFF ^
-DBUILD_ZLIB=OFF ^
-DBUILD_TIFF=OFF ^
-DBUILD_JASPER=OFF ^
-DBUILD_JPEG=OFF ^
-DBUILD_PNG=OFF ^
-DBUILD_OPENEXR=OFF ^
-DBUILD_TBB=OFF ^
-DENABLE_DYNAMIC_CUDA=OFF ^
-DENABLE_PRECOMPILED_HEADERS=OFF ^

-DWITH_AVFOUNDATION=OFF ^
-DWITH_CARBON=OFF ^
-DWITH_CUDA=OFF ^
-DWITH_VTK=OFF ^
-DWITH_CUFFT=OFF ^
-DWITH_CUBLAS=OFF ^
-DWITH_EIGEN=OFF ^
-DWITH_FFMPEG=OFF ^
-DWITH_GSTREAMER=OFF ^
-DWITH_GTK=OFF ^
-DWITH_IMAGEIO=OFF ^
-DWITH_IPP=OFF ^
-DWITH_JASPER=OFF ^
-DWITH_JPEG=OFF ^
-DWITH_OPENEXR=OFF ^
-DWITH_PNG=OFF ^
-DWITH_TIFF=OFF ^
-DWITH_QUICKTIME=OFF ^
-DWITH_QTKIT=OFF ^
-DWITH_TBB=OFF ^
-DWITH_OPENMP=ON ^
-DWITH_V4L=OFF ^
-DWITH_LIBV4L=OFF ^
-DWITH_OPENCL=OFF ^

-DBUILD_opencv_java=OFF ^
-DBUILD_opencv_androidcamera=OFF ^
-DBUILD_opencv_ts=OFF ^
-DBUILD_opencv_python2=OFF ^
-DBUILD_opencv_python3=OFF ^
-DBUILD_opencv_gpu=OFF ^
-DBUILD_opencv_dynamicuda=OFF ^
-DBUILD_opencv_ocl=OFF ^
-DBUILD_opencv_imgcodecs=OFF ^
-DBUILD_opencv_videoio=OFF ^
-DBUILD_opencv_calib3d=OFF ^
-DBUILD_opencv_flann=OFF ^
-DBUILD_opencv_objdetect=OFF ^
-DBUILD_opencv_stitching=OFF ^
-DBUILD_opencv_ml=OFF ^
-DBUILD_opencv_superres=OFF ^
-DBUILD_opencv_videostab=OFF ^
-DBUILD_opencv_viz=OFF ^
-DBUILD_opencv_contrib=OFF ^
-DBUILD_opencv_features2d=OFF ^
-DBUILD_opencv_legacy=OFF ^
-DBUILD_opencv_nonfree=OFF ^

-DBUILD_PACKAGE=OFF ^
-B%BUILD_DIR% ^
-H%OPENCV_ROOT% ^
-GNinja

ninja -C %BUILD_DIR%

timeout /T 3 /NOBREAK

cmake --install %BUILD_DIR% --prefix %INSTALL_DIR% -v

cmd.exe /k
