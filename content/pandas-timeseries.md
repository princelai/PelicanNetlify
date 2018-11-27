Title:Pandas 时间处理函数速度对比
Date: 2018-06-08 10:36
Category: 金融与算法
Tags: python, pandas
Slug: pandas-timeseries
Authors: Kevin Chen

Pandas 非常擅长处理时间序列，拥有多种处理时间序列的函数和方法，自己做了几个小测试，看看内置函数都能适配哪种格式、哪种情况，速度又有多快。

我用到的时间处理主要是对细粒度的时间重采样至粗粒度，之后再对重采样后的时间进行分组再进行后续操作，如求和、求平均或取最后值。

所以我就设计两个场景，第一个场景是对频率为秒的时间序列重采样至一分钟然后求平均；第二个场景就是对频率为秒的时间序列重采样至 3 分钟然后对新的时间序列取每个时间的最新值。

所以首先是要生成一组数据

```python
import pandas as pd

rng = pd.date_range(start='2018-04-07',end='2018-04-08',freq='s')
df = pd.DataFrame(pd.np.random.randn(rng.size),index=rng)
ser = pd.Series(pd.np.random.randn(rng.size),index=rng)
df.columns = ['random']
ser.name = 'random'
```

df 和 ser 分别对应 DataFrame 和 Series，查看下数据格式

`df.head()`

```
                       random
2018-04-07 00:00:00  0.163995
2018-04-07 00:00:01  0.756485
2018-04-07 00:00:02 -0.179441
2018-04-07 00:00:03  0.120944
2018-04-07 00:00:04 -1.558763
```

`ser.tail()`

```
2018-04-07 23:59:56    1.276893
2018-04-07 23:59:57    0.275050
2018-04-07 23:59:58    1.029358
2018-04-07 23:59:59    0.461299
2018-04-08 00:00:00    1.222731
Freq: S, Name: random, dtype: float64
```

接下来定义六个函数方法

```python
def method1(data):
    data.index = data.index.to_period('Min').to_timestamp()
    data.groupby(data.index).mean()

def method2(data):
    data.index = pd.to_datetime(data.index.strftime('%Y-%m-%d %H:%M'))
    data.groupby(data.index).mean()

def method3(data):
    ser_idx = pd.Series(data.index)
    data.index = pd.to_datetime(ser_idx.apply(lambda x:str(x)[:-2]+'00'))
    data.groupby(data.index).mean()

def method4(data):
    data.resample('Min').mean()

def method5(data):
    data.asfreq('3Min',method='ffill')

def method6(data):
    data.resample('3Min').last()
```

方法 1-方法 4 适用于场景一，方法 5-方法 6 适用于场景二，接下来具体说说这六个函数和为什么要这么设计场景。

方法 1 使用的是内置 to_period 方法转换周期，to_timestamp 方法是为了后续操作使用 timestamp 更方便。

方法 2 对索引日期进行字符串格式化然后再用内置的 to_datetime 方法转换回日期格式达到重采样效果。

方法 3 看似复杂，其实和方法二类似，我之所以加上方法三是因为我本以为这个办法处理会慢很多，但是最终结果还是有点出乎我的意料的。

方法 4 是内置的 resample 方法

方法 5 是内置的 asfreq 方法

方法 6 还是内置的 resample 方法

可以看到 resample 方法适用范围最广，既可以对时间采取多种细粒度的操作，也能对重采样后的数据进行后续操作；而 asfreq 方法只能对数据进行重采样，无法进行复杂的后续操作，只能用向前/向后填充数值；to_period 方法和字符串操作只能对时间进行整数采样，像 45 分钟，1 小时 30 分这种更细腻的操作是不支持的。

### 比较速度

**场景 1**

```
%timeit method1(df)
%timeit method2(df)
%timeit method3(df)
%timeit method4(df)

16.4 ms ± 391 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
439 ms ± 2.52 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
485 ms ± 10.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
2.13 ms ± 9.92 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

```
%timeit method1(ser)
%timeit method2(ser)
%timeit method3(ser)
%timeit method4(ser)

23.8 ms ± 72.2 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
446 ms ± 2.71 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
492 ms ± 3.61 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
1.63 ms ± 15.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

从上面对比数据得出结论，resample 方法最快，to_period 方法其次，两种字符串方法最慢，最快和最慢差距巨大。

**场景 2**

```
%timeit method5(df)
%timeit method6(df)

746 µs ± 32.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
2.42 ms ± 24 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

```
%timeit method5(ser)
%timeit method6(ser)

772 µs ± 20.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
1.87 ms ± 50.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

在场景二的测试中 asfreq 比 resample 快 2 倍多，如果不需要更多的后续操作，asfreq 是很好的选择，否则 resample 方法更为全能。

下方的表格总结了几种方法的优劣：

| 函数      | 时间细粒度操作 | 时间分组后续操作 | 速度 |
| --------- | -------------- | ---------------- | ---- |
| asfreq    | X              | X                | ✓    |
| resample  | ✓              | ✓                | ✓    |
| to_period | X              | ✓                | ✓    |
| 字符串    | X              | ✓                | X    |

### Pandas Offset Aliases

| Alias    | Description                                      |
| -------- | ------------------------------------------------ |
| B        | business day frequency                           |
| C        | custom business day frequency                    |
| D        | calendar day frequency                           |
| W        | weekly frequency                                 |
| M        | month end frequency                              |
| SM       | semi-month end frequency (15th and end of month) |
| BM       | business month end frequency                     |
| CBM      | custom business month end frequency              |
| MS       | month start frequency                            |
| SMS      | semi-month start frequency (1st and 15th)        |
| BMS      | business month start frequency                   |
| CBMS     | custom business month start frequency            |
| Q        | quarter end frequency                            |
| BQ       | business quarter end frequency                   |
| QS       | quarter start frequency                          |
| BQS      | business quarter start frequency                 |
| A, Y     | year end frequency                               |
| BA, BY   | business year end frequency                      |
| AS, YS   | year start frequency                             |
| BAS, BYS | business year start frequency                    |
| BH       | business hour frequency                          |
| H        | hourly frequency                                 |
| T, min   | minutely frequency                               |
| S        | secondly frequency                               |
| L, ms    | milliseconds                                     |
| U, us    | microseconds                                     |
| N        | nanoseconds                                      |

### 参考

[官方文档](https://pandas.pydata.org/pandas-docs/stable/timeseries.html)
