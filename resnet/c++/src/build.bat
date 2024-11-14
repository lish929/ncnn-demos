@REM 编译resnet18 分类动态库

@echo off

set SRC_DIR=D:\project\ncnn-demos\resnet\c++\src
set BUILD_DIR=D:\project\ncnn-demos\resnet\c++\src\build
set INSTALL_DIR=D:\project\ncnn-demos\resnet\c++\src\install

set ARC=x64
set VS=2019

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

cmake %PRE_OP% ^
-S %SRC_DIR% ^
-B %BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 16
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k

