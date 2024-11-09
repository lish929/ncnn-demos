@Rem 编译protobuf
@echo off

set ARC=x64
set VS=2022

set PROTOBUF_DIR=D:\codes\protobuf-3.11.2\cmake
set BUILD_DIR=D:\codes\protobuf-3.11.2\build
set INSTALL_DIR=D:\codes\protobuf-3.11.2\install

@REM if %ARC% == x64 (
    @REM echo "build x64"
    @REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
	@REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
@REM ) else (
    @REM echo "build x86"
    @REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
	@REM call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\BuildTools\VC\Auxiliary\Build\vcvars32.bat"
@REM )

if %VS% == 2019 (
    set PRE_OP=-G "Visual Studio 16 2019" -A %ARC%
) else (
    set PRE_OP=-G "Visual Studio 17 2022" -A %ARC%
)

if exist %BUILD_DIR% (
    rd /q /s %BUILD_DIR%
    md %BUILD_DIR%
) else (
    md %BUILD_DIR%
)
if exist %INSTALL_DIR% (
    rd /q /s %INSTALL_DIR%
    md %INSTALL_DIR%
) else (
    md %INSTALL_DIR%
)

cmake %PRE_OP% ^
-Dprotobuf_BUILD_TESTS=OFF ^
-Dprotobuf_MSVC_STATIC_RUNTIME=OFF ^
-S=%PROTOBUF_DIR% ^
-B=%BUILD_DIR%

cmake --build %BUILD_DIR% --config Release -j 8
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR%

cmd.exe /k