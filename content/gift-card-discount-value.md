Title: 充值卡折现价值分析
Date: 2018-08-06 15:58
Category: 金融笔记
Tags: 折现,最优化
Slug: gift-card-discount-value
Authors: Kevin Chen

前几天，媳妇把收到的一条短信转给我，问我值不值，我的第一反应当然是不值，这种预存方式都是欺负不懂时间价值的人玩的把戏。为了说服她，特地手算折现，但是发现，嗯？好像还是挺值的啊。于是就有了这篇文章，把计算的完整思路和代码贴出来。

![message](http://kevinstuchuang.qiniudn.com/blog-pic/gift-card-message.jpg)

_注：计算全部使用年华利率按月折现_

求真正价值的思路很简单，

> 真实价值 = 充值卡的标称价值向后折现再折回$T_0$ - 付出的价格按类似年金的方式收息后把总利息折回$T_0$时刻

代码如下：

```python
def calculate_value(month_after_use, year_yield, price, value, printlog=True):
    cash_flow = value / 12

    def discount():
        fv = sum(
            cash_flow * (1 + year_yield)**(y / 12) for y in range(1, 12 + 1))
        return fv / (1 + year_yield)**(month_after_use / 12)

    def interest():
        balance = [
            price - price / month_after_use * n
            for n in range(1,
                           int(month_after_use) + 1)
        ]
        return sum(
            b * ((1 + year_yield)**(1 / month_after_use) - 1) for b in balance)

    def real_value():
        if month_after_use >= 12:
            total_i = interest()
        else:
            print('Month afer use must great than 12.')
            exit
        pv = discount()
        return pv, total_i

    pv, total_i = real_value()
    real = pv - total_i
    profit = real - price
    if printlog:
        print(f'real value is {real:.2f}.({pv:.2f} - {total_i:.2f})')
        print(f'You earn {profit:.1f} YUAN.' if profit > 0 else f'You loss {-profit:.1f} YUAN.')
    else:
        return profit
```

假设我办理 12000 套餐，24 个月用完，折现利率（市场利率）年化 4%，模拟一下最后的收益，竟然是赚了 738 元！

`calculate_value(24, 0.04, 10400, 12000)`

```
real value is 11138.01.(11333.62 - 195.61)
You earn 738.0 YUAN.
```

那么是不是办理了就一定稳赚不赔呢？这就要用到 Scipy 中的最优化函数找一找结果。

首先要导入需要用的包

```python
from functools import partial
from scipy.optimize import minimize
```

用偏导函数固定住不变化的参数，lambda 函数用于方便传参

```python
partial_func = partial(calculate_value, price=10400, value=12000, printlog=False)
func = lambda x: partial_func(*x)
```

如果是要固定住三个参数，需要传的参数不在第一位，可以用这种方式创建一个偏导函数

```python
partial_func = partial(lambda a,b,c,d: calculate_value(b,a,c,d),b=24,c=10400,d=12000)
```

函数初始在 18 个月，利率 4%，边界定在 12-36 个月，3%-6%年化利率。因为最优化函数求的是最小值，我们要求的是最大值，所以还对函数的符号进行改变。

```python
x0 = (18, 0.04)
bnds = ((12, 36), (0.03, 0.06))
res = minimize(lambda y:-1 * func((y[0],y[1])), x0, method='SLSQP', bounds=bnds)
```

查看结果，寻找最优解失败，猜想一下，这个函数应该不是凸函数，函数边界为（ -$\infty$, +$\infty$），但在我们给定的范围内，结果停留在了 12 个月，3%年化利率，也就是说越快把充值的钱用完、同时你的资金获得的市场利率越低越有利。
`print(res)`

```
     fun: -1297.8802495375876
     jac: array([  31.28442383, 9879.27038574])
 message: 'Positive directional derivative for linesearch'
    nfev: 16
     nit: 8
    njev: 4
  status: 8
 success: False
       x: array([12.  ,  0.03])
```

说了这么多，还是很抽象，不如画出来容易理解。
我使用 matplotlib 的 3D 图，需要导入相关的包

```python
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
```

利用上面的偏导后`func`函数计算出三个轴的数据

```python
X = np.arange(12, 36 + 1)
Y = np.round(np.linspace(3, 6, len(X)), 4)
loss_list = []
for i in range(12, 36 + 1):
    loss_list.append(
        [func((i, j / 100)) for j in np.round(np.linspace(3, 6, len(X)), 4)])
X, Y = np.meshgrid(X, Y)
Z = np.array(loss_list)
```

最后 plot 出来并做一些美化

```python
fig = plt.figure(figsize=(16, 12), dpi=100)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.rainbow, linewidth=0, antialiased=True)
ax.set_xlabel('Month')
ax.set_ylabel('Yield')
ax.set_zlabel('Profit')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f%%'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.tight_layout()
plt.show()
```

![profit surface](http://kevinstuchuang.qiniudn.com/blog-pic/profit_surface.png)

三维空间的一个平面，其实就是二维空间的一条直线，收益曲线确实不是一个凸函数。找不到最优解实属正常。但是总的来说，这个充值卡还是很值得办理的，在当前 4%的平均利率水平下，他们又不限制使用车辆，所以可以足够快的用完。

最后，虽然这篇文章看起来像个软广，但是我真的不认识发信息的人。
