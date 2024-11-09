@Rem 编译opencv
@echo off

set ARC=x64
set VS=2022

set OPENCV_DIR=D:\codes\opencv-mobile-4.10.0
set BUILD_DIR=D:\codes\opencv-mobile-4.10.0\build
set INSTALL_DIR=D:\codes\opencv-mobile-4.10.0\install
set OPTIONS_PATH=D:\codes\opencv-mobile-4.10.0\options.txt

if %ARC% == x64 (
    echo "build x64"
    call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
) else (
    echo "build x86"
    call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
)

if %VS% == 2019 (
    set PRE_OP=-G "Visual Studio 16 2019" -A %ARC%
) else (
    set PRE_OP=-G "Visual Studio 17 2022" -A %ARC%
)

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
%options% ^
-DBUILD_opencv_world=OFF ^
-S %OPENCV_DIR% ^
-B %BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 8
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k