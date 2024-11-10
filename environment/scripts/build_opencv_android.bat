@REM android交叉编译opencv-mobile

@echo off

set PRE_OP="-G Unix Makefiles"

set OPENCV_DIR=D:\codes\opencv-mobile-4.10.0
set BUILD_DIR=D:\codes\opencv-mobile-4.10.0\build-android
set INSTALL_DIR=D:\codes\opencv-mobile-4.10.0\install-android
set OPTIONS_PATH=D:\codes\opencv-mobile-4.10.0\options.txt

set TOOL_CHAIN=D:\Android\sdk\ndk\21.4.7075529\build\cmake\android.toolchain.cmake
set MAKE_PROGRAM=D:\Android\sdk\ndk\21.4.7075529\prebuilt\windows-x86_64\bin\make.exe

set ABI=armeabi-v7a
@REM set ANDROID_PLATFORM=android-26

if exist %BUILD_DIR% (
    rd /s /q %BUILD_DIR%
    md %BUILD_DIR%
) else (
    md %BUILD_DIR%
)

if exist %INSTALL_DIR% (
    rd /s /q %INSTALL_DIR%
    md %INSTALL_DIR%
) else (
    md %INSTALL_DIR%
)

setlocal enabledelayedexpansion
for /f "delims=" %%i in (%OPTIONS_PATH%) do (
    set options=!options! %%i
)

cmake %PRE_OP% ^
-DBUILD_SHARED_LIBS=ON ^
%options% ^
-DCMAKE_TOOLCHAIN_FILE=%TOOL_CHAIN% ^
-DCMAKE_MAKE_PROGRAM=%MAKE_PROGRAM% ^
-DCMAKE_ANDROID_ARCH_ABI=%ABI% ^
@REM -DANDROID_PLATFORM=%ANDROID_PLATFORM% ^
-DANDROID_NATIVE_API_LEVEL=26 ^
@REM -DBUILD_opencv_world=OFF ^
-S %OPENCV_DIR% ^
-B %BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 8
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k