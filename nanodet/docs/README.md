# nanodet

### 导出模型

- 拉取代码

  ```
  git clone https://github.com/RangiLyu/nanodet.git
  ```

- 环境配置

  在安装requirements时，报错**ERROR: No matching distribution found for cython**，更换清华源下载（注释掉torch相关，避免重新下载为cpu版本）

  ```
  conda create -n nanodet python=3.8 -y
  conda activate nanodet
  conda install pytorch torchvision cudatoolkit=11.1 -c pytorch -c conda-forge
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  python setup.py develop
  ```

- 导出torchscript

  下载权重（选择最小的nanodet-m-0.5x）

  ```
  https://drive.google.com/file/d/1rMHkD30jacjRpslmQja5jls86xd0YssR/view?usp=sharing
  ```

  导出torchscript（注意路径），也可以导出onnx后在转换ncnn，不过现在更推荐使用pnnx及逆行转换

  ```
  python tools/export_torchscript.py --cfg_path config\legacy_v0.x_configs\nanodet-m-0.5x.yml --model_path ..\models\nanodet_m_0.5x.ckpt --out_path ..\models\nanodet_m_0.5x.torchscript.pth
  ```

- 导出ncnn

  ```
  pnnx ../models/nanodet_m_0.5x.torchscript.pth inputshape=[1,3,320,320]fp32
  ```

  