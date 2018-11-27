Title: matplotlib 中文字体配置
Date: 2017-12-18 16:01
Category: 玩电脑
Tags: python,matplotlib
Slug: matplotlib-chinese-fonts
Authors: Kevin Chen

matplotlib 是 Python 的优秀绘图包，但是不论是在 Windows 还是 Linux 中默认都是不支持中文的，尤其是在 Linux 中设置更加复杂一点，设置方法如下：

首先我们需要获取到 matplotlib 配置文件的文件夹

```bash
python -c "import matplotlib as mpl;print(mpl.get_configdir())"
/home/kevin/.config/matplotlib
```

然后需要一个默认的 matplotlibrc 文件用于修改

```bash
python -c "import matplotlib as mpl;print(mpl.matplotlib_fname())"
/opt/anaconda/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc
```

这个位置会根据每个人安装位置不同而改变

然后把默认的 rc 文件拷贝到用户的配置文件夹

```bash
cp /opt/anaconda/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc ~/.config/matplotlib
```

之后的工作都是围绕这个 rc 文件，一般情况下只需要修改如下两个字段，把注释打开。

```
font.sans-serif     : DejaVu Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva
axes.unicode_minus  : False
```

第一个字段负责中文字体显示，但是目前还没有，第二个负责正负号的显示。

由于 matplotlib 不使用系统字体，所以需要找到一个 matplotlib 支持的字体且已在系统中

```
fc-list :lang=zh |grep -i ttf
```

在 shell 中执行这个命令，就能找到几个字体，选择一个填到上面第一行第一个即可，通常建议选择`Droid Sans Fallback`

修改好后重启整个 python 或 ipython 之后应该就可以看到中文，不过还是不可以的话可以使用下面方案二查找，这个方法出自[segmentfault][1]。

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib.font_manager import FontManager
import subprocess

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)

output = subprocess.check_output(
    'fc-list :lang=zh -f "%{family}\n"', shell=True)
output = output.decode('utf8')

zh_fonts = set(f.split(',', 1)[0] for f in output.split('\n'))
available = mat_fonts & zh_fonts

print('*' * 10, '可用的字体', '*' * 10)
for f in available:
    print(f)
```

如果不想使用 rc 文件来配置，那么可以在每次使用的时候在 python 中执行以下命令即可。

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['Droid Sans Fallback']
plt.rcParams['axes.unicode_minus']=False
```

[1]: https://segmentfault.com/a/1190000000621721
