@REM Android交叉编译ncnn
@echo off

set PRE_OP="-G Unix Makefiles"

set NCNN_DIR=D:\codes\ncnn
set BUILD_DIR=D:\codes\ncnn\build-android
set INSTALL_DIR=D:\codes\ncnn\install-android

set TOOL_CHAIN=D:\Android\sdk\ndk\21.4.7075529\build\cmake\android.toolchain.cmake
set MAKE_PROGRAM=D:\Android\sdk\ndk\21.4.7075529\prebuilt\windows-x86_64\bin\make.exe

set ABI=armeabi-v7a
set ANDROID_PLATFORM=android-26

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

cmake %PRE_OP% ^
-DNCNN_SHARED_LIB=ON ^
-DCMAKE_TOOLCHAIN_FILE=%TOOL_CHAIN% ^
-DCMAKE_MAKE_PROGRAM=%MAKE_PROGRAM% ^
-DANDROID_ABI=%ABI% ^
-DANDROID_PLATFORM=%ANDROID_PLATFORM% ^
-DNCNN_VULKAN=ON ^
-DANDROID_ARM_NEON=ON ^
-S %NCNN_DIR% ^
-B %BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 8
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k