@Rem 编译ncnn
@echo off

set ARC=x64
set VS=2022

set NCNN_DIR=D:\codes\ncnn
set BUILD_DIR=D:\codes\ncnn\build
set INSTALL_DIR=D:\codes\ncnn\install
set PROTOBUF_DIR=D:\codes\protobuf-3.11.2\install\cmake

if %ARC% == x64 (
    echo "build x64"
    @REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
	call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
) else (
    echo "build x86"
    @REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
	call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\BuildTools\VC\Auxiliary\Build\vcvars32.bat"
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

if not exist %PROTOBUF_DIR% (
    echo "protobuf dir not exist"
    pause
)

cmake %PRE_OP% ^
-DNCNN_SHARED_LIB=ON ^
-DNCNN_ENABLE_LTO=ON ^
-DNCNN_BENCHMARK=ON ^
-DNCNN_VULKAN=ON ^
-DNCNN_BUILD_TESTS=ON ^
-Dprotobuf_DIR=%PROTOBUF_DIR% ^
-S %NCNN_DIR% ^
-B %BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 8
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k