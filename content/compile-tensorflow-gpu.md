Title: 编译 Tensorflow 1.10 + CUDA9.2 + MKL
Date: 2018-07-30 18:43
Category: 机器学习
Tags: tensorflow, cuda, GPU
Slug: compile-tensorflow-gpu
Authors: Kevin Chen

我的电脑系统是基于 Archlinux 的 Manjaro，软件包更新的比较激进，很早就已经是 CUDA 9.2 了，而目前 Tensorflow 的官方编译版本对 CUDA 的支持还只停留在 CUDA 9.0。由于还不太会用 mxnet 和 pytorch，这时倍加想念 Keras 的简单。最近忙里偷闲研究了一下编译安装 Tensorflow，发现还挺简单的，把成功的喜悦分享出来，也供有需要的朋友参考。

# 查看系统信息

### 查看系统架构和发行版本

我用的 Manjaro x86_64

`uname -m && cat /etc/*release`

```
x86_64
Manjaro Linux
DISTRIB_ID=ManjaroLinux
DISTRIB_RELEASE=17.1.11
DISTRIB_CODENAME=Hakoila
DISTRIB_DESCRIPTION="Manjaro Linux"
Manjaro Linux
NAME="Manjaro Linux"
ID=manjaro
PRETTY_NAME="Manjaro Linux"
ANSI_COLOR="1;32"
HOME_URL="https://www.manjaro.org/"
SUPPORT_URL="https://www.manjaro.org/"
BUG_REPORT_URL="https://bugs.manjaro.org/"
```

### 查看 CPU 支持的指令集

嗯，这个貌似没什么用

`cat /proc/cpuinfo |grep -m1 flags |cut -f2 -d":"`

```
fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb cat_l3 cdp_l3 invpcid_single pti intel_ppin ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm rdt_a rdseed adx smap intel_pt xsaveopt cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts
```

### 查看 Python 环境

我用 Anaconda 构建的虚拟环境，Python 3.6.6。这里要注意记住`base environment`环境路径。

`conda info`

```
     active environment : None
       user config file : /home/kevin/.condarc
 populated config files : /home/kevin/.condarc
          conda version : 4.5.8
    conda-build version : 3.12.0
         python version : 3.6.6.final.0
       base environment : /opt/Anaconda3  (writable)
           channel URLs : https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/linux-64
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/noarch
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/linux-64
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/noarch
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/linux-64
                          https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/noarch
          package cache : /opt/Anaconda3/pkgs
                          /home/kevin/.conda/pkgs
       envs directories : /opt/Anaconda3/envs
                          /home/kevin/.conda/envs
               platform : linux-64
             user-agent : conda/4.5.8 requests/2.19.1 CPython/3.6.6 Linux/4.18.0-1-MANJARO manjaro/17.1.11 glibc/2.27
                UID:GID : 1000:1000
             netrc file : None
           offline mode : False
```

### 查看 GPU 信息

如果你执行不了下面这个命令，那么证明你的驱动装的有问题，要用闭源的 Nvidia 驱动，不要用开源的。Manjaro 安装驱动太简单了，就不详细说了。

其次你还要去[CUDA GPU](https://developer.nvidia.com/cuda-gpus)根据显卡型号查询你 GPU 的算力，这个算力后面会用到。如果你的显卡是 Nvidia 1000 系列，且型号大于 1050，那么算力就是 6.1。

`nvidia-smi`

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 396.45                 Driver Version: 396.45                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 108...  Off  | 00000000:03:00.0  On |                  N/A |
|  0%   59C    P5    26W / 250W |    672MiB / 11170MiB |      3%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0       625      G   /usr/lib/xorg-server/Xorg                    370MiB |
|    0      3527      G   /usr/bin/kwin_x11                             53MiB |
|    0      3569      G   /usr/bin/krunner                               2MiB |
|    0      3573      G   /usr/bin/plasmashell                          99MiB |
|    0      6489      G   ...-token=3E0EB0339C426519FCEB41A77A4FE74E    75MiB |
|    0      9846      G   /opt/Anaconda3/bin/python                     28MiB |
|    0     13026      G   ...-token=F6A861CA29AB37BD6D50C064EC6A95F0    40MiB |
+-----------------------------------------------------------------------------+
```

# 安装编译依赖

### 安装显卡相关依赖

```
yaourt -S --needed linux418-nvidia cuda cudnn
```

安装好之后你还需要记住 cuDNN 的版本和路径

`yaourt -Ql cudnn |grep libcudnn.so`

```
cudnn /opt/cuda/lib64/libcudnn.so
cudnn /opt/cuda/lib64/libcudnn.so.7
cudnn /opt/cuda/lib64/libcudnn.so.7.1.4
```

一般来说 CUDA 和 cuDNN 的动态链接库文件都在同一个路径下，版本的话，自己安装的什么版本心里没点 B 数吗？

`yaourt -Ql cuda |grep libcudart.so`

```
cuda /opt/cuda/lib64/libcudart.so
cuda /opt/cuda/lib64/libcudart.so.9.2
cuda /opt/cuda/lib64/libcudart.so.9.2.148
cuda /usr/share/man/man7/libcudart.so.7.gz
```

你还应该确认 CUDA、cuDNN、Python 的执行文件路径或库文件路径已经加入到了`$PATH`变量中

`echo $PATH`

```
/opt/bin:/opt/cuda/bin:/opt/Anaconda3/bin:/opt/android-sdk/platform-tools:/opt/android-sdk/tools:/opt/android-sdk/tools/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/android-sdk/platform-tools:/opt/android-sdk/tools:/opt/android-sdk/tools/bin:/opt/cuda/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl
```

### 安装编译工具

Tensorflow 需要使用 bazel 构建，gcc7 编译，当前我的系统 gcc 版本是 8.1 我已经帮你试过了，Tensorflow 不允许 gcc 版本高于 7。

```
yaourt -S bazel gcc7 gcc7-libs
```

### 下载源码

```
git clone https://github.com/tensorflow/tensorflow
```

### 选择安装版本

当前稳定版本为 1.9，1.10 处于 rc2 阶段，编译哪个版本自己选择。

```
cd tensorflow
git checkout r1.10
```

# 编译安装

### 编译配置

如没有特殊要求，按照我的选择就可以，注意路径要换成自己的。

```
$ ./configure
Extracting Bazel installation...
WARNING: --batch mode is deprecated. Please instead explicitly shut down your Bazel server using the command "bazel shutdown".
You have bazel 0.15.1- (@non-git) installed.
Please specify the location of python. [Default is /opt/Anaconda3/bin/python]:


Found possible Python library paths:
  /opt/Anaconda3/lib/python3.6/site-packages
Please input the desired Python library path to use.  Default is [/opt/Anaconda3/lib/python3.6/site-packages]

Do you wish to build TensorFlow with jemalloc as malloc support? [Y/n]:
jemalloc as malloc support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Google Cloud Platform support? [Y/n]: n
No Google Cloud Platform support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Hadoop File System support? [Y/n]: n
No Hadoop File System support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Amazon AWS Platform support? [Y/n]: n
No Amazon AWS Platform support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Apache Kafka Platform support? [Y/n]: n
No Apache Kafka Platform support will be enabled for TensorFlow.

Do you wish to build TensorFlow with XLA JIT support? [y/N]:
No XLA JIT support will be enabled for TensorFlow.

Do you wish to build TensorFlow with GDR support? [y/N]:
No GDR support will be enabled for TensorFlow.

Do you wish to build TensorFlow with VERBS support? [y/N]:
No VERBS support will be enabled for TensorFlow.

Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]:
No OpenCL SYCL support will be enabled for TensorFlow.

Do you wish to build TensorFlow with CUDA support? [y/N]: y
CUDA support will be enabled for TensorFlow.

Please specify the CUDA SDK version you want to use. [Leave empty to default to CUDA 9.0]: 9.2


Please specify the location where CUDA 9.2 toolkit is installed. Refer to README.md for more details. [Default is /opt/cuda]:


Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 7.0]: 7


Please specify the location where cuDNN 7 library is installed. Refer to README.md for more details. [Default is /opt/cuda]:


Do you wish to build TensorFlow with TensorRT support? [y/N]:
No TensorRT support will be enabled for TensorFlow.

Please specify the NCCL version you want to use. If NCCL 2.2 is not installed, then you can use version 1.3 that can be fetched automatically but it may have worse performance with multiple GPUs. [Default is 2.2]: 1.3


Please specify a list of comma-separated Cuda compute capabilities you want to build with.
You can find the compute capability of your device at: https://developer.nvidia.com/cuda-gpus.
Please note that each additional compute capability significantly increases your build time and binary size. [Default is: 6.1]


Do you want to use clang as CUDA compiler? [y/N]:
nvcc will be used as CUDA compiler.

Please specify which gcc should be used by nvcc as the host compiler. [Default is /usr/bin/gcc-7]:


Do you wish to build TensorFlow with MPI support? [y/N]:
No MPI support will be enabled for TensorFlow.

Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native]:


Would you like to interactively configure ./WORKSPACE for Android builds? [y/N]:
Not configuring the WORKSPACE for Android builds.

Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See tools/bazel.rc for more details.
        --config=mkl            # Build with MKL support.
        --config=monolithic     # Config for mostly static monolithic build.
Configuration finished
```

### 开始编译

`--config=mkl`可以选择不添加，Intel CPU 加了也没什么坏处。

```
bazel build --config=opt --config=cuda --config=mkl //tensorflow/tools/pip_package:build_pip_package
```

最终耗时 50 分钟编译完成

```
INFO: Elapsed time: 3049.910s, Critical Path: 248.40s
INFO: 8105 processes: 8105 local.
INFO: Build completed successfully, 8292 total actions
```

### 导出为 wheel 文件

```
$ bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
$ ls -lh /tmp/tensorflow_pkg
-rw-r--r-- 1 kevin kevin 135M Jul 30 14:03 tensorflow-1.10.0rc1-cp36-cp36m-linux_x86_64.whl
```

### pip 安装

```
pip install /tmp/tensorflow_pkg/tensorflow-1.10.0rc1-cp36-cp36m-linux_x86_64.whl
```

# 测试

安装好之后，可以通过下面两种不同的方法查看是否已经开启了 GPU。

### 方法一

```python
import tensorflow as tf
with tf.device('/gpu:0'):
  a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
  b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tf.matmul(a, b)
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
print(sess.run(c))
```

### 方法二

```python
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")
```

# 参考

[从源代码安装 TensorFlow](https://www.tensorflow.org/install/install_sources?hl=zh-cn)
