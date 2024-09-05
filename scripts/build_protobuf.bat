@Rem 编译opencv静态库

set ARC=x64
set VS=2019
set BUILD_TYPE=Release
set PROTOBUF_ROOT=D:\yolo\protobuf-3.11.2\cmake
set BUILD_DIR=D:\yolo\protobuf-3.11.2\protobuf_build
set INSTALL_DIR=D:\yolo\protobuf-3.11.2\protobuf_install

@echo off

if %ARC% == x86 (
	echo "build x86"
	call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
	set VS_ARC=Win32
) else (
	echo "build x64"
	call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
	set VS_ARC=x64
)

if %VS% == 2019 (
@REM 	set CM_PRE_OP=-G "Visual Studio 16 2019" -A %VS_ARC%
	set CM_PRE_OP=-A %VS_ARC%
)

if exist "%BUILD_DIR%" rd /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

if exist "%INSTALL_DIR%" rd /s /q "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%"

cmake %CM_PRE_OP% ^
-DCMAKE_SYSTEM_NAME=Windows ^
-DCMAKE_BUILD_TYPE=%BUILD_TYPE% ^
-Dprotobuf_BUILD_TESTS=OFF ^
-Dprotobuf_MSVC_STATIC_RUNTIME=OFF ^
-B%BUILD_DIR% ^
-H%PROTOBUF_ROOT%

cmake --build %BUILD_DIR% --config Release

cmake --install %BUILD_DIR% --prefix %INSTALL_DIR% -v

cmd.exe /k