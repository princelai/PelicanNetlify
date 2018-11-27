Title: 用股票数据说明方差和标准差的特性
Date: 2018-01-15 15:35
Category: 金融与算法
Tags: python,数学,统计学
Slug: using-python-descript-vaiance-std
Authors: Kevin Chen

[方差][1]（Variance），应用数学里的专有名词。在概率论和统计学中，一个随机变量的方差描述的是它的离散程度，也就是该变量离其期望值的距离。一个实随机变量的方差也称为它的二阶矩或二阶中心动差，恰巧也是它的二阶累积量。这里把复杂说白了，就是将各个误差将之平方（而非取绝对值，使之肯定为正数），相加之后再除以总数，透过这样的方式来算出各个数据分布、零散（相对中心点）的程度。继续延伸的话，方差的算术平方根称为该随机变量的标准差（此为相对各个数据点间）。

[标准差][2]（Standard Deviation，SD），数学符号 $\sigma$（sigma），在概率统计中最常使用作为测量一组数值的离散程度之用。标准差定义：为方差开算术平方根，反映组内个体间的离散程度；标准差与期望值之比为标准离差率。

### 1.定义

方差的定义如下公式：
$$Var(X)=\sigma^2=E[(X-\mu)^2]$$
对上式化简后可得到如下公式：
$$\sigma^2=E[X^2]-(E[X])^2$$
上面两个公式也可以写为下面这样：
$$\sigma^2=\frac{1}{N}\sum*{i=1}^{N}(x_i-\mu)^2=\frac{(\sum*{i=1}^{N}x_i^2-\mu^2)}{N}$$

标准差的定义和公式和方差类似，就是对方差开平方根即可得到。

$$SD(X) = \sigma = \sqrt{E(X-E(X))^2}$$
$$\sigma = \sqrt{\frac{\sum*{i=1}^NX_i^2}{N}-\mu^2}$$
$$\sigma = \sqrt{\frac{(\sum*{i=1}^{N}x_i^2-\mu^2)}{N}}$$

### 2.准备数据

这里使用一个开源免费的股票数据模块 tushare，获取贵州茅台的数据，并截取数据的前 600 天，把数据平分为 2 部分。获取后的数据格式为 DataFrame。

```python
import tushare as ts
import numpy as np

stock = ts.get_k_data('600519')
stock = stock.iloc[:600,stock.columns.get_loc('close')]
stock_part1 = stock.iloc[:stock.index.size//2]
stock_part2 = stock.iloc[stock.index.size//2:]
stock_part2.index = range(300)
```

### 3.特性验证

对于方差的计算，我们可以把数据带入公式直接计算，python 代码可以这样写，这里使用的是无偏估计，所以分母是 N-1。

```python
((stock - stock.mean())**2).sum()/(stock.size-1)
```

不过幸好 Numpy 和 Pandas 都提供了快速计算方差和标准差的方法，我们可以调用<code>var()</code>方法和<code>std()</code>方法使用。

**性质 1，一个常数被加至变量数列中，此数列方差不变。**
$$Var(X+c) = Var(X)$$
$$SD(X+c) = SD(X)$$

```python
In [1]:np.isclose((stock+5).var(),stock.var())
Out[1]:True #方差
In [2]:np.isclose((stock+8).std(),stock.std())
Out[2]:True #标准差
```

**性质 2，数列被放大一个常数倍，此数列的方差变大常数的平方倍**
$$Var(cX) = c^2 \times Var(X)$$
$$SD(cX) = c \times SD(X)$$

```python
In [3]:np.isclose((stock*3).var(),3**2*stock.var())
Out[3]:True #方差
In [4]:np.isclose((stock*4).std(),4*stock.std())
Out[4]: True #标准差
```

**性质 3，两个数列和（差）的方差**

$$Var(aX+bY)=a^2Var(X)+b^2Var(Y)+2 \times ab \times Cov(X,Y)$$
$$Var(X-Y)=Var(X)+Var(Y)-2 \times Cov(X,Y)$$

标准差也有同样的性质

$$SD(X+Y)=\sqrt{\sigma^2(X)+\sigma^2(Y)+2 \times Cov(X,Y)}$$

```python
In [5]:np.isclose((stock_part1 + stock_part2).var(),stock_part1.var() + stock_part2.var() + 2*stock_part1.cov(stock_part2))
Out[5]:True #方差
In [6]:np.isclose((stock_part1 + stock_part2).std(),np.sqrt(stock_part1.var() + stock_part2.var() + 2*stock_part1.cov(stock_part2)))
Out[6]:True #标准差
```

[1]: https://zh.wikipedia.org/zh-cn/%E6%96%B9%E5%B7%AE
[2]: https://zh.wikipedia.org/zh-cn/%E6%A8%99%E6%BA%96%E5%B7%AE
