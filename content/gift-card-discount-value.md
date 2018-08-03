Title: 充值卡折现价值分析
Date: 2018-08-03 15:58
Category: 金融笔记
Tags: 折现,最优化
Slug: gift-card-discount-value
Authors: Kevin Chen
Status: draft



![](http://kevinstuchuang.qiniudn.com/blog-pic/gift-card-message.jpg)



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



`calculate_value(24, 0.04, 10400, 12000)`

```
real value is 11138.01.(11333.62 - 195.61)
You earn 738.0 YUAN.
```





```python
from functools import partial
from scipy.optimize import minimize
```

```python
partial_func = partial(calculate_value, price=10400, value=12000, printlog=False)
func = lambda x: partial_func(*x)
```

````python
partial_func = partial(lambda a,b,c,d: calculate_value(b,a,c,d),c=10400,d=12000)
````

```python
x0 = (18, 0.04)
bnds = ((12, 36), (0.03, 0.06))
res = minimize(lambda y:-1 * func((y[0],y[1])), x0, method='SLSQP', bounds=bnds)
```

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



```python
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
```



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



![profit surface](http://kevinstuchuang.qiniudn.com/blog-pic/profit_surf.png)