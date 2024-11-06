### VSCODE 搭建开发环境

- Android开发环境

  - 配置JDK8

    - 下载JDK8：[https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.oracle.com%2Fjava%2Ftechnologies%2Fjavase%2Fjavase-jdk8-downloads.html)

    - 解压压缩包并配置环境变量
  
      ```
      JAVA_HOME D:\Android\jdk
      CLASSPATH .;%JAVA_HOME%\lib;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;
      Path %JAVA_HOME%\bin %JAVA_HOME%\jre\bin
      ```
  
    - 注意：在设置Path变量时，如果是分行显示则一行填写一个，不用添加任何符号（分行显示使用.;%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin的形式有的电脑上不行）
  
    ![image-20241104223957358](assets/image-20241104223957358.png)
  
  - 安装Android命令行工具
  
    - 下载链接：https://links.jianshu.com/go?to=https%3A%2F%2Fdeveloper.android.google.cn%2Fstudio%3Fhl%3Dzh-cn
  
    - 注意：命令行工具需要根据jdk版本决定，参考：[Android cmdline-tools 版本与其最小JDK关系-CSDN博客](https://blog.csdn.net/ys743276112/article/details/134024106)
  
    - jdk8命令行工具下载地址：https://dl.google.com/android/repository/commandlinetools-win-9123335_latest.zip
  
    - 解压下载安装包并注册环境变量
  
      ![image-20241104224700284](assets/image-20241104224700284.png)
  
      ![image-20241104224841696](assets/image-20241104224841696.png)
  
  - 配置Android环境
  
    - 安装platform-tools：app调试需要用到的工具，比如adb、fastboot等
  
      ```
      sdkmanager --install platform-tools --sdk_root=D:\Android\sdk
      ```
  
    - 安装build-tools以及platform：build-tools是编译时对应的编译工具，platforms系统的jar包
  
      API对应参考：[Android 版本号、版本名称、api版本对照表（持续更新）_android版本对照表-CSDN博客](https://blog.csdn.net/wangsheng5454/article/details/117119402)
  
      ```
      sdkmanager --install build-tools;29.0.3 platforms;android-29 --sdk_root=D:\Android\sdk
      ```
  
    - 安装仿真镜像以及模拟器：emulator是模拟器，system-images系统的镜像文件，镜像可以随意，支持android-29的就行
  
      ```
      sdkmanager --install emulator system-images;android-29;google_apis_playstore;x86_64 --sdk_root=D:\Android\sdk
      ```
  
  - vscode环境搭建
  
    **踩坑记录**
  
    - 插件安装
  
      ![image-20241106232540294](assets/image-20241106232540294.png)
  
      ![image-20241106232602768](assets/image-20241106232602768.png)
  
    - Android Full Surpport模板修改
  
      C:\Users\Windows\.vscode\extensions\antonydalmiere.android-support-0.6.0\template\newProject路径
  
      - app/build.gradle
  
        修改sdk版本
  
        ```
        plugins {
            id 'com.android.application'
        }
        
        android {
            compileSdk 29
        
            defaultConfig {
                applicationId "{{package}}"
                minSdk 21
                targetSdk 29
                versionCode 1
                versionName "1.0"
        
                testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
            }
        
            buildTypes {
                release {
                    minifyEnabled false
                    proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
                }
            }
            compileOptions {
                sourceCompatibility JavaVersion.VERSION_1_8
                targetCompatibility JavaVersion.VERSION_1_8
            }
        }
        
        dependencies {
        
            implementation 'androidx.appcompat:appcompat:1.3.1'
            implementation 'com.google.android.material:material:1.4.0'
            testImplementation 'junit:junit:4.+'
            androidTestImplementation 'androidx.test.ext:junit:1.1.3'
            androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
        }
        ```
  
      - gradle/wrapper/gradle-wrapper.properties
  
        修改gradle版本
  
        ```
        #Mon Oct 18 19:16:13 CEST 2021
        distributionBase=GRADLE_USER_HOME
        distributionUrl=https\://services.gradle.org/distributions/gradle-5.6.4-all.zip
        distributionPath=wrapper/dists
        zipStorePath=wrapper/dists
        zipStoreBase=GRADLE_USER_HOME
        ```
  
      - build.gradle
  
        修改gradle plugin版本
  
        ```
        // Top-level build file where you can add configuration options common to all sub-projects/modules.
        buildscript {
            repositories {
                google()
                mavenCentral()
            }
            dependencies {
                classpath "com.android.tools.build:gradle:3.6.4"
        
                // NOTE: Do not place your application dependencies here; they belong
                // in the individual module build.gradle files
            }
        }
        
        task clean(type: Delete) {
            delete rootProject.buildDir
        }
        ```
  
        gradle gradle plugin jsk版本对应参考：[Android Gradle Plugin与Gradle版本、JDK版本对应关系_gradle7.5.1 对应的jdk-CSDN博客](https://blog.csdn.net/qq_42690281/article/details/131643663)
  
    - 错误1：Could not find method dependencyResolutionManagement() for arguments [settings_9fx48amztt7ox9m2z9cru9bm0$_run_closure1@15291da] on settings 'android_test' of type org.gradle.initialization.DefaultSettings.参考：[Android studio报错Could not find method dependencyResolutionManagement() for arguments的解决方法-CSDN博客](https://blog.csdn.net/wddptwd28/article/details/123008860)
  
      ```
      // dependencyResolutionManagement {
      //     repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
      //     repositories {
      //         google()
      //         mavenCentral()
      //         jcenter() // Warning: this repository is going to shut down soon
      //     }
      // }
      rootProject.name = "test"
      include ':app'
      ```
  
    - 错误2：Cannot resolve external dependency androidx.appcompat:appcompat:1.3.1 because no repositories are defined.参考：[Gradle7.0 降到Gradle4.2出现的问题_cannot resolve external dependency androidx.appcom-CSDN博客](https://blog.csdn.net/qq_41811862/article/details/121114332)
  
      ```
      // Top-level build file where you can add configuration options common to all sub-projects/modules.
      buildscript {
          repositories {
              google()
              mavenCentral()
          }
          dependencies {
              classpath "com.android.tools.build:gradle:4.2.0"
      
              // NOTE: Do not place your application dependencies here; they belong
              // in the individual module build.gradle files
          }
      }
      
      allprojects {
          repositories {
              google()
              mavenCentral()
          }
      }
      
      task clean(type: Delete) {
          delete rootProject.buildDir
      }
      ```
  
    - 错误3：SDK location not found. Define location with an ANDROID_SDK_ROOT environment variable or by setting the sdk.dir path in your project's local properties file at 'D:\codes\android_test\local.properties'.参考：[解决“SDK location not found. Define location with sdk.dir in the local.properties“-CSDN博客](https://blog.csdn.net/u010775335/article/details/109615223)
  
      这里有点奇怪，在环境变量与vscode的setting中设置了ANDROID_SDK_ROOT，但并未起效，最终创建local.properties解决
  
      ```
      sdk.dir=D:\Android\sdk
      ```
  
    - 错误4：Could not determine the dependencies of task ':app:processDebugResources'. > java.io.IOException: �ļ�����Ŀ¼��������﷨����ȷ��
  
      网上搜索到了许多的解决方法，有清理项目重新构建、代理设置问题等等解决方法，同时也更换了gradle与gradle plugin的版本，但是并未解决问题，个人考虑可能是因为graddle与gradle plugin的版本问题。由于jdk的版本是1.8，参考上面的关系对照表，graddle与gradle plugin版本都比较低，考虑更换jdk版本来解决问题
  
      注意：在android的开发上，vscode搭建环境确实比较的困难，更加建议的是使用android studio来进行开发（使用android studio搭建环境没有遇到这么多错误），由于需要在移动端设备上进行算法的部署，需要涉及到python、java以及c++语言，使用pycharm+visual studio+android studio未免太过沉重，故尝试使用vscode来集成进行开发
  
    

### android交叉译ncnn

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

