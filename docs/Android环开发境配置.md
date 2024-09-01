# Android开发环境配置

**android studio下载地址：[下载 Android Studio 和应用工具 - Android 开发者  | Android Developers](https://developer.android.com/studio?hl=zh-cn)**

**jdk下载安装：[（超详细）2022年最新版java 8（ jdk1.8u321）安装教程_java8下载-CSDN博客](https://blog.csdn.net/JunLeon/article/details/122623465)**

- 第一次运行自动检测Android SDK的位置，会出现以下错误（点击cancel进入下一步）：

![image-20240901211528401](assets/image-20240901211528401.png)

- 选择自定义的安装配置：

![image-20240901211639629](assets/image-20240901211639629.png)

- 根据需求选择相应的选项进行下载：

![image-20240901212056972](assets/image-20240901212056972.png)

- 为HAXM设置可用内存（加速android studio模拟器）：

![image-20240901212413692](assets/image-20240901212413692.png)

- 等待下载完成：

![image-20240901212546038](assets/image-20240901212546038.png)

- 网络出现问题无法进行下载，点击cancel，打开android studio新建项目，打开SDK Manager：

![image-20240901213345304](assets/image-20240901213345304.png)

- 下载

![image-20240901214533750](assets/image-20240901214533750.png)

- 配置HAXM（安装失败）

![image-20240901231350680](assets/image-20240901231350680.png)

![image-20240901231339704](assets/image-20240901231339704.png)

- 配置virtual device

![image-20240901231518008](assets/image-20240901231518008.png)

- 运行项目

![image-20240901231544875](assets/image-20240901231544875.png)