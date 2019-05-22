Title: 几种Python脚本性能分析工具的介绍
Date: 2019-05-22 17:42
Category: 玩电脑
Tags: python, profile
Slug: python-profiler
Authors: Kevin Chen
Status: draft





## 获取数据

由于我有自己的股票数据库，直接从库里提取出单支股票数据，这里用的是601519大智慧，数据总共1813行，43列。查看数据格式：

`df.tail()`

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ts_code</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>vol</th>
      <th>amount</th>
      <th>turnover_rate</th>
      <th>turnover_rate_f</th>
      <th>pe_ttm</th>
      <th>pb</th>
      <th>ps_ttm</th>
      <th>total_share</th>
      <th>float_share</th>
      <th>free_share</th>
      <th>total_mv</th>
      <th>circ_mv</th>
      <th>MA1</th>
      <th>MA2</th>
      <th>MA3</th>
      <th>DIFFC1</th>
      <th>DIFFC2</th>
      <th>DIFFC3</th>
      <th>DIFF12</th>
      <th>DIFF23</th>
      <th>SLOPE2</th>
      <th>SLOPE3</th>
      <th>ret</th>
      <th>DIF</th>
      <th>DEA</th>
      <th>MACD</th>
      <th>vma2</th>
      <th>volrate1</th>
      <th>position</th>
      <th>upshadow</th>
      <th>downshadow</th>
      <th>entity</th>
      <th>vchuge</th>
      <th>vcextreme</th>
      <th>vrmean</th>
      <th>ret_std</th>
      <th>ADJ_DIFF12</th>
      <th>ADJ_DIFF23</th>
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
      <th>2019-05-15</th>
      <td>601519.SH</td>
      <td>7.28</td>
      <td>7.37</td>
      <td>6.95</td>
      <td>7.09</td>
      <td>1534411.60</td>
      <td>1096057.990</td>
      <td>7.7195</td>
      <td>20.5508</td>
      <td>140.6910</td>
      <td>9.8648</td>
      <td>23.4643</td>
      <td>198770.0</td>
      <td>198770.0</td>
      <td>74664.3341</td>
      <td>1409279.3</td>
      <td>1409279.3</td>
      <td>7.976602</td>
      <td>9.646350</td>
      <td>9.620733</td>
      <td>-11.115037</td>
      <td>-26.500699</td>
      <td>-26.304988</td>
      <td>-17.309634</td>
      <td>0.266276</td>
      <td>-1.236415</td>
      <td>0.446042</td>
      <td>2.604920</td>
      <td>-0.128341</td>
      <td>-0.094126</td>
      <td>-0.136857</td>
      <td>727309.1935</td>
      <td>2.109710</td>
      <td>37.359551</td>
      <td>3.949224</td>
      <td>4.748201</td>
      <td>-2.609890</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.391803</td>
      <td>7.345512</td>
      <td>-2.356491</td>
      <td>0.036250</td>
    </tr>
    <tr>
      <th>2019-05-16</th>
      <td>601519.SH</td>
      <td>7.00</td>
      <td>7.04</td>
      <td>6.80</td>
      <td>6.92</td>
      <td>920730.10</td>
      <td>634875.573</td>
      <td>4.6321</td>
      <td>12.3316</td>
      <td>137.3176</td>
      <td>9.6283</td>
      <td>22.9017</td>
      <td>198770.0</td>
      <td>198770.0</td>
      <td>74664.3341</td>
      <td>1375488.4</td>
      <td>1375488.4</td>
      <td>7.713686</td>
      <td>9.536999</td>
      <td>9.656366</td>
      <td>-10.289319</td>
      <td>-27.440485</td>
      <td>-28.337433</td>
      <td>-19.118309</td>
      <td>-1.236155</td>
      <td>-1.133606</td>
      <td>0.370385</td>
      <td>-2.397743</td>
      <td>-0.126630</td>
      <td>-0.100627</td>
      <td>-0.104013</td>
      <td>742112.9675</td>
      <td>1.240687</td>
      <td>35.767790</td>
      <td>-0.571429</td>
      <td>1.764706</td>
      <td>1.156069</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.366581</td>
      <td>6.909756</td>
      <td>-2.766857</td>
      <td>-0.178900</td>
    </tr>
    <tr>
      <th>2019-05-17</th>
      <td>601519.SH</td>
      <td>6.87</td>
      <td>7.18</td>
      <td>6.42</td>
      <td>6.61</td>
      <td>938072.30</td>
      <td>641530.728</td>
      <td>4.7194</td>
      <td>12.5639</td>
      <td>131.1661</td>
      <td>9.1970</td>
      <td>21.8758</td>
      <td>198770.0</td>
      <td>198770.0</td>
      <td>74664.3341</td>
      <td>1313869.7</td>
      <td>1313869.7</td>
      <td>7.456458</td>
      <td>9.429382</td>
      <td>9.680729</td>
      <td>-11.352015</td>
      <td>-29.899964</td>
      <td>-31.720015</td>
      <td>-20.923147</td>
      <td>-2.596364</td>
      <td>-1.128416</td>
      <td>0.252293</td>
      <td>-4.479769</td>
      <td>-0.128100</td>
      <td>-0.106122</td>
      <td>-0.087913</td>
      <td>759415.6275</td>
      <td>1.235255</td>
      <td>32.865169</td>
      <td>-4.512373</td>
      <td>2.959502</td>
      <td>3.933434</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.243143</td>
      <td>6.405541</td>
      <td>-3.266414</td>
      <td>-0.405331</td>
    </tr>
    <tr>
      <th>2019-05-20</th>
      <td>601519.SH</td>
      <td>6.70</td>
      <td>6.74</td>
      <td>5.95</td>
      <td>6.36</td>
      <td>824367.64</td>
      <td>514372.878</td>
      <td>4.1473</td>
      <td>11.0410</td>
      <td>126.2052</td>
      <td>8.8491</td>
      <td>21.0484</td>
      <td>198770.0</td>
      <td>198770.0</td>
      <td>74664.3341</td>
      <td>1264177.2</td>
      <td>1264177.2</td>
      <td>7.198229</td>
      <td>9.326603</td>
      <td>9.691819</td>
      <td>-11.644935</td>
      <td>-31.807966</td>
      <td>-34.377643</td>
      <td>-22.820458</td>
      <td>-3.768294</td>
      <td>-1.089987</td>
      <td>0.114560</td>
      <td>-3.782148</td>
      <td>-0.131423</td>
      <td>-0.111182</td>
      <td>-0.080964</td>
      <td>773292.9800</td>
      <td>1.066048</td>
      <td>30.524345</td>
      <td>-0.597015</td>
      <td>6.890756</td>
      <td>5.345912</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.243143</td>
      <td>5.760118</td>
      <td>-3.961804</td>
      <td>-0.654204</td>
    </tr>
    <tr>
      <th>2019-05-21</th>
      <td>601519.SH</td>
      <td>6.31</td>
      <td>7.00</td>
      <td>6.31</td>
      <td>7.00</td>
      <td>687176.52</td>
      <td>461821.481</td>
      <td>3.4571</td>
      <td>9.2035</td>
      <td>138.9051</td>
      <td>9.7396</td>
      <td>23.1665</td>
      <td>198770.0</td>
      <td>198770.0</td>
      <td>74664.3341</td>
      <td>1391390.0</td>
      <td>1391390.0</td>
      <td>7.001422</td>
      <td>9.241095</td>
      <td>9.696182</td>
      <td>-0.020314</td>
      <td>-24.251404</td>
      <td>-27.806637</td>
      <td>-24.236014</td>
      <td>-4.693463</td>
      <td>-0.916810</td>
      <td>0.045020</td>
      <td>10.062893</td>
      <td>-0.123773</td>
      <td>-0.113700</td>
      <td>-0.040290</td>
      <td>781475.7515</td>
      <td>0.879332</td>
      <td>36.516854</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>10.935024</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.197808</td>
      <td>6.736810</td>
      <td>-3.597550</td>
      <td>-0.696689</td>
    </tr>
  </tbody>
</table>



## 测试函数

### Pandas版本

```python
def detonate(window, df):
    error_ret = 0.7 if window < 20 else 0.12
    onelimitup = df.loc[df.low == df.high].index
    maxidx = df.index.size - window
    result = []
    for i in range(0, maxidx, max(2, window // 10)):
        data = df.close.iloc[i:i + window]
        ret = data.pct_change()
        if any(ret > error_ret):
            continue
        pct = (data.iloc[-1] - data) / data
        if not any(pct >= 1.0):
            continue
        sqrt_day = np.sqrt((data.index[-1] - data.index).days + 1)
        value = pct[:-1] / sqrt_day[:-1]
        value = value.loc[~value.index.isin(onelimitup)]
        if value.empty or (value.max() < 0.1):
            continue
        detonate_date = value.idxmax()
        max_ret = pct.loc[detonate_date]
        max_value = value.loc[detonate_date]
        result.append([detonate_date, max_ret, max_value])
    if len(result) == 0:
        return None
    result_df = pd.DataFrame(result)
    result_df.columns = ['trade_date', 'window_return', 'value_rate']
    # 同日合并取最大
    result_df = result_df.groupby('trade_date').max()
    result_df['ts_code'] = df.ts_code.iloc[-1]
    result_df.set_index(['ts_code', result_df.index], inplace=True)
    result_df = result_df.sort_values('value_rate', ascending=False).iloc[:10]
    return result_df.where(result_df.window_return >= 1.0).dropna()
```



### Numpy版本

```python
def detonate2(window, index, close, low, high):
    error_ret = 0.7 if window < 20 else 0.12
    onelimitup = index[low == high]
    maxidx = index.size - window
    result = np.zeros((30, 3))
    ri = 0
    for i in range(0, maxidx, max(2, window // 5)):
        _close = close[i:i + window]
        _index = index[i:i + window]
        ret = (_close[1:] - _close[:-1]) / _close[:-1]
        if np.any(ret > error_ret):
            continue
        pct = (_close[-1] - _close) / _close
        if not np.any(pct >= 1.0):
            continue
        sqrt_day = np.sqrt((_index[-1] - _index).astype('timedelta64[D]').astype(int) + 1)
        value = pct / sqrt_day
        value = np.where(np.array([i not in onelimitup for i in _index]), value, 0)
        if value.max() < 0.1:
            continue
        detonate_date = _index[value.argmax()]
        max_ret = pct[value.argmax()]
        max_value = value.max()
        result[ri] = np.array([detonate_date, max_ret, max_value])
        ri += 1
        if ri >= 30:
            return result
    return result


def numpy_detonate(df):
    t = detonate2(20, df.index.values, df.close.values, df.low.values, df.high.values)
    result_df = pd.DataFrame(t[t[:, 0] > 0])
    result_df.columns = ['trade_date', 'window_return', 'value_rate']
    result_df['trade_date'] = pd.to_datetime(result_df.trade_date)
    result_df = result_df.groupby('trade_date').max()
    result_df['ts_code'] = df.ts_code.iloc[-1]
    result_df.set_index(['ts_code', result_df.index], inplace=True)
    result_df = result_df.sort_values('value_rate', ascending=False).iloc[:10]
    return result_df.where(result_df.window_return >= 1.0).dropna()
```



## 性能测试

### timeit

如果你使用的是ipython，那么自带的`%timeit`魔术方法就是最简单最直接的一种性能分析方式

```python
%timeit detonate(20, df.loc[:, ['ts_code', 'low', 'high', 'close']])
1.46 s ± 11.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit numpy_detonate(df)
17.7 ms ± 225 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```



### line_profiler



### vprof