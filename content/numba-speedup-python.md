Title: 使用Numba为Python提速10+倍
Date: 2019-05-14 17:15
Category: 金融与算法
Tags: python, numba, pandas
Slug: numba-speedup-python
Authors: Kevin Chen




前一阵写了一个获取股票数据的程序，准备玩玩预测，在添加指标时，有一个指标我是这么定义的

> 指标名称：当前位置
>
> 描述：当天收盘价在过去300天内的位置百分比
>
> 算法：(当前收盘价 - 过去300天内最低价的最小值) / (过去300天内最高价的最大值- 过去300天内最低价的最小值 )

按说这么容易的一个指标，一个Pandas rolling函数就搞定了，但是我为什么没选择rolling函数？原因如下：

1. rolling函数只能操作一列数据，比如只能在close这一列应用函数，而无法同时处理三列（low,high,close）。

2. rolling函数会使你的数据减少window-1个天数，类似于MA指标，但是MA我最大只用到60日线，而这个window要被设置为300天，为了这么一个指标平白损失299个数据我觉得不值得。

综上，所以我决定手撸一个方法，修改一点规则作为变通

> 如果当前日之前的数据个数不足window个，那么就取[0,T]这段时间

   



数据如下，这个指标其实只用到了三列，这里用了上证指数作为例子，数据都存储为DataFrame格式。

```python
from read_data import ReadData

TIME_STEP = 300
index_day = ReadData.index_day()
szzs = index_day.loc[index_day.ts_code == '000001.SH']
szzs.head()
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ts_code</th>
      <th>close</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>vol</th>
      <th>amount</th>
      <th>total_mv</th>
      <th>float_mv</th>
      <th>total_share</th>
      <th>float_share</th>
      <th>free_share</th>
      <th>turnover_rate</th>
      <th>turnover_rate_f</th>
      <th>pe_ttm</th>
      <th>pb</th>
    </tr>
    <tr>
      <th>trade_date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2007-01-10</th>
      <td>000001.SH</td>
      <td>2825.576</td>
      <td>2838.113</td>
      <td>2841.741</td>
      <td>2770.988</td>
      <td>111769365.0</td>
      <td>7.9e+07</td>
      <td>8.9e+12</td>
      <td>1.7e+12</td>
      <td>1.2e+12</td>
      <td>2.1e+11</td>
      <td>1.9e+11</td>
      <td>5.06</td>
      <td>5.69</td>
      <td>38.25</td>
      <td>3.38</td>
    </tr>
    <tr>
      <th>2007-01-11</th>
      <td>000001.SH</td>
      <td>2770.110</td>
      <td>2819.367</td>
      <td>2841.180</td>
      <td>2763.886</td>
      <td>121598717.0</td>
      <td>8.3e+07</td>
      <td>8.7e+12</td>
      <td>1.7e+12</td>
      <td>1.2e+12</td>
      <td>2.1e+11</td>
      <td>1.9e+11</td>
      <td>5.48</td>
      <td>6.17</td>
      <td>37.44</td>
      <td>3.31</td>
    </tr>
    <tr>
      <th>2007-01-12</th>
      <td>000001.SH</td>
      <td>2668.110</td>
      <td>2745.321</td>
      <td>2782.025</td>
      <td>2652.578</td>
      <td>107303768.0</td>
      <td>7.3e+07</td>
      <td>8.4e+12</td>
      <td>1.7e+12</td>
      <td>1.2e+12</td>
      <td>2.1e+11</td>
      <td>1.9e+11</td>
      <td>4.80</td>
      <td>5.40</td>
      <td>36.05</td>
      <td>3.18</td>
    </tr>
    <tr>
      <th>2007-01-15</th>
      <td>000001.SH</td>
      <td>2794.701</td>
      <td>2660.070</td>
      <td>2795.331</td>
      <td>2658.879</td>
      <td>91761561.0</td>
      <td>6.6e+07</td>
      <td>8.8e+12</td>
      <td>1.7e+12</td>
      <td>1.2e+12</td>
      <td>2.1e+11</td>
      <td>1.9e+11</td>
      <td>4.10</td>
      <td>4.62</td>
      <td>37.76</td>
      <td>3.33</td>
    </tr>
    <tr>
      <th>2007-01-16</th>
      <td>000001.SH</td>
      <td>2821.017</td>
      <td>2818.663</td>
      <td>2830.803</td>
      <td>2757.205</td>
      <td>111178574.0</td>
      <td>8.3e+07</td>
      <td>8.8e+12</td>
      <td>1.8e+12</td>
      <td>1.2e+12</td>
      <td>2.1e+11</td>
      <td>1.9e+11</td>
      <td>4.96</td>
      <td>5.59</td>
      <td>38.04</td>
      <td>3.36</td>
    </tr>
  </tbody>
</table>


### Python List


我的第一版实现方法，其实我是故意转换为list的，因为我知道这样会最慢。

```python
def percent_position_list(data, window):
    position = []
    low = data[:, 0].tolist()
    high = data[:, 1].tolist()
    close = data[:, 2].tolist()
    for i in range(len(close)):
        llv = min(low[max(0, i - window):i + 1])
        hhv = max(high[max(0, i - window):i + 1])
        c = close[i]
        if llv == hhv:
            position.append(100)
        else:
            position.append((c - llv) / (hhv - llv) * 100)
    return position
```

该方法就是单纯的循环list实现，调用方法特地封装在一个函数中，这样方便测试，但并没有返回数据，使用ipython的`%timeit`魔术方法测得的时间写在`docstring`中。

```python
def python_list(stock):
    """
    36.5 ms ± 99.1 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    """
    result = percent_position_list(stock[['low', 'high', 'close']].values, TIME_STEP)
```



本来不添加这个指标之前我的程序运行速度还能接受，但是加上之后，作用在3500+支股票上真是慢到令人发指，所以不得不开启我的优化之旅。





### Rolling + Numpy

注意，单独使用Pandas rolling函数不能得到准确的结果，而且会损失数据，测量这个方法只是为了作为一个基准。

```python
def pandas_rolling(stock):
    """
    24.9 ms ± 337 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    """
    result = stock.rolling(TIME_STEP).close.apply(lambda x: (x[-1] - x.min())/(x.max() - x.min()), raw=True) * 100
```





虽然上面的方法不是我要的结果，但是我可以稍微改造一下，弥补其中的一个缺陷。在rolling函数返回的`NaN`数据上再次调用循环方法计算，这样数据是全的，只是rolling计算的结果还是有误差的。



计算函数，这次没转换为list，使用Numpy来计算

```python
def percent_position_plain(data, window):
    position = []
    low = data[:, 0]
    high = data[:, 1]
    close = data[:, 2]
    for i in range(close.size):
        llv = low[max(0, i - window):i + 1].min()
        hhv = high[max(0, i - window):i + 1].max()
        c = close[i]
        if llv == hhv:
            position.append(100)
        else:
            position.append((c - llv) / (hhv - llv) * 100)
    return position
```



调用函数，这个版本的思想是能使用rolling的就用rolling，不能的再单独计算。从结果上看，比list版本性能稍好，速度提升大概21%，不算太理想。

```python
def pandas_rolling_plain(stock):
    """
    28.7 ms ± 247 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    """
    result = stock.rolling(TIME_STEP).close.apply(lambda x: (x[-1] - x.min())/(x.max() - x.min()), raw=True) * 100
    result.iloc[:TIME_STEP - 1] = percent_position_plain(stock.loc[:stock.index[TIME_STEP - 2], ['low', 'high', 'close']].values, TIME_STEP)

```





### Numpy

如果不混合Pandas rolling和Numpy，直接使用Numpy计算呢？上面的`percent_position_plain`函数还可以复用，只需要修改下调用函数即可。

```python
def numpy_plain(stock):
    """
    23.7 ms ± 161 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    """
    result = percent_position_plain(stock[['low', 'high', 'close']].values, TIME_STEP)
```



精简了代码，速度还得到提升，简直两开花，遗憾的是提升幅度并不大。不过能看出来Numpy的计算速度比Pandas的计算速度还是有优势的，毕竟数据格式简单，所以大规模计算还是从Pandas转换到Numpy来处理更合适。





### Numba jit

在进入正题前先导入相关库

```python
from numba import guvectorize, int64, float64, void, njit
import numpy as np
```



计算函数与之前Numpy版本的区别只有两个，一个是使用了Numba的`njit`装饰器，这个装饰器与`jit(nopython=True)`等价，另一个区别是之前的计算函数使用list存储结果，而这个函数使用Numpy分配了一个空向量存储结果，这是因为Numba识别不了Python的list结构。

```python
@njit
def percent_position_jit(data, window):
    low = data[:, 0]
    high = data[:, 1]
    close = data[:, 2]
    position = np.empty(close.size)
    for i in range(close.size):
        llv = low[max(0, i - window):i + 1].min()
        hhv = high[max(0, i - window):i + 1].max()
        c = close[i]
        if llv == hhv:
            position[i] = 100
        else:
            position[i] = (c - llv) / (hhv - llv) * 100
    return position
```



来看看结果，在几乎没有什么修改的情况下，速度提升了10倍。

```python
def numba_git(stock):
    """
    2.85 ms ± 13.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    """
    result = percent_position_jit(stock[['low', 'high', 'close']].values, TIME_STEP)
```





### Numba guvectorize

Numba还提供了ufunc函数的装饰器，由于该装饰器只能传入向量，不能是矩阵，所以装饰器写起来有些复杂，但是其实函数内部并没有本质的变化。

```python
@guvectorize([void(float64[:], float64[:], float64[:], int64, float64[:])], '(n),(n),(n),()->(n)')
def percent_position_guv(low, high, close, window, position):
    for i in range(low.size):
        llv = low[max(0, i-window):i + 1].min()
        hhv = high[max(0, i-window):i + 1].max()
        c = close[i]
        if llv == hhv:
            position[i] = 100
        else:
            position[i] = (c - llv) / (hhv - llv) * 100
```



向量化函数速度更快一些，但是相比Numba jit优势没有那么大。

```python
def numba_guv(stock):
    """
    2.07 ms ± 46.7 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    """
    result = percent_position_guv(stock.low.values, stock.high.values, stock.close.values, TIME_STEP)

```





### 结语

通过上面的对比可以看出Numba速度上的实力，简单的改写，真实的提升。其实在优化的过程中，任何使用Pandas的`apply`和`rolling`方法中的匿名函数都可以用Numba改写。虽然Python的for循环很慢，但是经过Numba（LLVM）优化过的代码并没有这方面的问题，再加上编译器预先知道变量数据类型，速度与静态编译类型语言并无二致。