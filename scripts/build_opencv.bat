@Rem 编译opencv静态库

set ARC=x64
set VS=2022
set BUILD_TYPE=Release
set OPENCV_ROOT=D:\ncnn_demos\opencv
set BUILD_DIR=D:\ncnn_demos\opencv\build
set INSTALL_DIR=D:\ncnn_demos\opencv\install

@echo off

if %ARC% == x86 (
	echo "build x86"
	call "C:\Program Files\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
@REM 	set VS_ARC=Win32
) else (
	echo "build x64"
	call "C:\Program Files\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
@REM 	set VS_ARC=x64
)

if exist "%BUILD_DIR%" rd /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

@REM -DBUILD_opencv_world=ON

cmake %OPENCV_SOURCES_PATH% ^
-DBUILD_SHARED_LIBS=OFF ^
-DCMAKE_BUILD_TYPE=%BUILD_TYPE% ^
-DCMAKE_SYSTEM_NAME=Windows ^
-DBUILD_WITH_STATIC_CRT=ON ^

-DBUILD_TESTS=OFF ^
-DBUILD_PREF_TESTS=OFF ^
-DBUILD_EXAMPLES=ON ^
-DBUILD_DOCS=OFF ^

-DWITH_CUDA=OFF ^
-DWITH_OPENCL=OFF ^
-Dwith_ZLIB=OFF ^
-DWITH_FFMPEG=OFF ^
-DWITH_JASPER=OFF ^
-DWITH_TIFF=OFF ^

-DBUILD_opencv_apps=OFF ^
-DBUILD_opencv_contrib=OFF ^
-DBUILD_opencv_calib3d=OFF ^
-DBUILD_opencv_gpu=OFF ^
-DBUILD_opencv_photo=OFF ^
-DBUILD_opencv_superres=OFF ^
-DBUILD_opencv_ts=OFF ^
-DBUILD_opencv_flann=OFF ^
-DBUILD_opencv_features2d=OFF ^
-DBUILD_opencv_nonfree=OFF ^
-DBUILD_opencv_ml=OFF ^
-DBUILD_opencv_ocl=OFF ^
-DBUILD_opencv_objdetect=OFF ^
-DBUILD_opencv_python=OFF ^
-DBUILD_opencv_stitching=OFF ^
-DBUILD_opencv_video=OFF ^
-DBUILD_opencv_videostab=OFF ^

-DBUILD_PACKAGE=OFF ^
-B%BUILD_DIR% ^
-H%OPENCV_ROOT% ^
-GNinja

ninja -C %BUILD_DIR%

timeout /T 3 /NOBREAK

cmake --install %BUILD_DIR% --prefix %INSTALL_DIR% -v

cmd.exe /k
