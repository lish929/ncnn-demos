@Rem Ωª≤Ê±‡“Îandroid ncnn

set ARC=x64
set VS=2019
set TOOLCHAIN=C:\SDK\ndk\28.0.12433566\build\cmake\android.toolchain.cmake
set ABI=armeabi-v7a
set PLATFORM=android-26
set NCNN_ROOT=D:\ncnn-demos\environment\ncnn
set BUILD_DIR=D:\ncnn-demos\environment\ncnn\build_ncnn_armv7
set INSTALL_DIR=D:\ncnn-demos\environment\ncnn\install_ncnn_armv7

@echo off

if %ARC% == x86(
    echo "build x86"
	call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars32.bat"
	set VS_ARC=Win32
)else(
    echo "build x64"
    call "C:\Program Files (x86)\Microsoft Visual Studio\%VS%\Community\VC\Auxiliary\Build\vcvars64.bat"
	set VS_ARC=x64
)

if exist "%BUILD_DIR%" rd /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

if exist "%INSTALL_DIR%" rd /s /q "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%"

cmake ^
-A %VS_ARC% ^
-DCMAKE_SYSTEM_NAME=Windows ^
-DCMAKE_TOOLCHAIN_FILE=%TOOLCHAIN% ^
-DANDROID_ABI=%ABI% ^
-DANDROID_ARM_NEON=ON ^
-DANDROID_PLATFORM=%PLATFORM% ^
-DNCNN_VULKAN=OFF ^
-B %BUILD_DIR% ^
-H %NCNN_ROOT%

cmake --build %BUILD_DIR%
cmake --install %BUILD_DIR% --prefix %INSTALL_DIR% -v

cmd.exe /k