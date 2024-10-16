### android交叉编译ncnn

**参考文档**：[如何构建 ·腾讯/ncnn 维基 (github.com)](https://github.com/Tencent/ncnn/wiki/how-to-build#build-for-android)

- 克隆ncnn：git clone https://github.com/Tencent/ncnn.git

- 下载ndk：[NDK 下载  | Android NDK  | Android Developers](https://developer.android.com/ndk/downloads?hl=zh-cn)

- 编译

  - ```
    cmake -DCMAKE_TOOLCHAIN_FILE="C:\SDK\ndk\28.0.12433566\build\cmake\android.toolchain.cmake" -DANDROID_ABI="armeabi-v7a" -DANDROID_ARM_NEON=ON -DANDROID_PLATFORM=android-26 -DNCNN_VULKAN=OFF -G "Unix Makefiles" -DCMAKE_MAKE_PROGRAM="C:\SDK\ndk\28.0.12433566\prebuilt\windows-x86_64\bin\make.exe" ..
    
    cmake --build . -j 8
    cmake --install
    ```

- 注意

  - 在Windows下需要设置-G “Unix Mkaefiles”，配合ndk下的make进行编译
  - 需要注意自己需要的platform版本
  - 编译选项查看ncnn下的CmakeLists.txt，选择自己所需要的选项

![image-20241016214235770](assets/image-20241016214235770.png)



### 交叉编译opencv-mobile

**参考文档**：https://github.com/nihui/opencv-mobile/blob/master/README.md

- 下载opencv-mobile：https://github.com/nihui/opencv-mobile/releases/download/v30/opencv-mobile-4.10.0.zip

- ```
  cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_opencv_world=OFF -DCMAKE_TOOLCHAIN_FILE="C:\SDK\ndk\28.0.12433566\build\cmake\android.toolchain.cmake" -G "Unix Makefiles" -DCMAKE_MAKE_PROGRAM="C:\SDK\ndk\28.0.12433566\prebuilt\windows-x86_64\bin\make.exe" -DANDROID_PLATFORM=android-26 -DCMAKE_ANDROID_ARCH_ABI=armeabi-v7a -DANDROID_NATIVE_API_LEVEL=26 ..
  
  cmake --build -j 8
  cmake --install
  ```

- 注意

  - 编译选项查看options.txt，选择自己所需要的选项

