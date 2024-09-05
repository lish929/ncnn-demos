# 编译ncnn

**参考文档：[ncnn/docs/how-to-build/how-to-build.md at master · Tencent/ncnn (github.com)](https://github.com/Tencent/ncnn/blob/master/docs/how-to-build/how-to-build.md#build-for-windows-x64-using-visual-studio-community-2017)**

### Windows编译

- 编译protobuf

  - 下载protobuf：https://github.com/google/protobuf/archive/v3.11.2.zip
  - 编写脚本进行编译

  ```bat
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
  ```

- ~~下载安装vulkan SDK：https://vulkan.lunarg.com/sdk/home~~

- 编译ncnn

  - 拉取ncnn：https://github.com/Tencent/ncnn.git
  - 编写脚本进行编译（关闭了vulcan选项）：

  ```
  @Rem 编译opencv静态库
  
  set ARC=x64
  set VS=2019
  set BUILD_TYPE=Release
  set NCNN_ROOT=D:\yolo\ncnn
  set BUILD_DIR=D:\yolo\ncnn\ncnn_build
  set INSTALL_DIR=D:\yolo\ncnn\ncnn_install
  
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
  -Dprotobuf_DIR=D:\yolo\protobuf-3.11.2\protobuf_build\cmake ^
  -DNCNN_VULKAN=OFF ^
  -B%BUILD_DIR% ^
  -H%NCNN_ROOT%
  
  cmake --build %BUILD_DIR% --config Release
  
  cmake --install %BUILD_DIR% --prefix %INSTALL_DIR% -v
  
  cmd.exe /k
  ```

**注意：**

- 文档中所展示的zlib+protobuf+ncnn的编译没有通过（在编译带有zlib的protobuf时失败）
- ncnn编译选项：[ncnn/docs/how-to-use-and-FAQ/build-minimal-library.md at master · Tencent/ncnn (github.com)](https://github.com/Tencent/ncnn/blob/master/docs/how-to-use-and-FAQ/build-minimal-library.md)，根据需求选择编译选项，以减小编译库文件的大小