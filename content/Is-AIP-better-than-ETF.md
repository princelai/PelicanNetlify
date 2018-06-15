Title: 用数据验证定投是否优于直接投资
Date: 2018-06-06 17:27
Category: 金融笔记
Tags: 定投, ETF
Slug: Is-AIP-better-than-ETF
Authors: Kevin Chen


一直以来，定投的营销话术都是分批建仓，上涨时投资少降低成本，下跌时投资多赚取低估价值，但定投是否真的如宣传的那么美好？今天就用数据来模拟两种投资方式，看看孰优孰劣。



### 数据说明

本次实验使用三只ETF基金作为投资和定投标的，分别为华夏上证50ETF（510050），华泰柏瑞沪深300ETF（510300），广发中证500ETF（510510），时间区间为2013年5月27日至2018年6月7日。

先上图了解下这段时间ETF基金大致走势。

*50ETF月线*

![上证50ETF](http://kevinstuchuang.qiniudn.com/blog-pic/ETF50close.png)

*500ETF周线*

![500ETF](http://kevinstuchuang.qiniudn.com/blog-pic/ETF500close.png)

这段区间整体来看是上涨的，大盘股涨的多，小盘股涨得少。分段来看2013年中至2014年中，属于震荡行情，2014年中至2015年中是暴涨行情，2015年中至2016年初是暴跌行情，2016年初至2018年中行情分化，大盘股再次进入牛市，中盘股属于慢牛，小盘股是横盘震荡走势。

选择这个区间的行情，是因为这五年属于一个完整的周期，活跃时波动率大，行情过后的低迷时期波动率又小，是典型的中国股市。另外从长期来看，股票波动向上才应该是上市公司内在价值增长的表现。

当然，用这个区间的数据做分析是有一个缺点的，就是这三只ETF基金整体涨幅都在40%-50%之间，如果在一开始就持有至当前日期，那么一定是一次性直接投资要优于定投，不过放心，后面编程不会让这种事情发生，我会加入时间随机项，尽量减小整体上涨带来的影响。



### 开始实验

首先要导入用到的包

```python
import tushare as ts
import pandas as pd
import random
import matplotlib.pyplot as plt
```



之后利用tushare包，获取到三只ETF基金的收盘价，放入一个DataFrame内，这里我创建了一个类，主要是为了代码整洁考虑。

```python
class AutoInvestmentPlan:
    def __init__(self):
        plt.style.use('ggplot')
        self.code_list = ['510050','510300','510510']
        self.start_date = '2013-05-27'
    
    def get_etf_close(self,code,start):
        df = ts.get_k_data(code,start=start)
        df.set_index('date',inplace=True)
        df.index = pd.to_datetime(df.index)
        return df.close

    def combin_to_df(self):
        close_list = []
        for code in self.code_list:
            close_list.append(self.get_etf_close(code,self.start_date))
        self.data = pd.concat(close_list,axis=1)
        self.data.columns = ['ETF50','ETF300','ETF500']

    def get_data(self):
        self.combin_to_df()
        self.monthly = self.data.asfreq('M',method='pad')
        self.weekly = self.data.asfreq('W',method='pad')
```



获取数据需要对类实例化，然后就得到了周和月数据

```python
aip = AutoInvestmentPlan()
aip.get_data()
```



这里需要等待几秒种，运行完成后就可以查看我们的数据了

**周数据最新的5个收盘价**

`aip.weekly.tail()`

```
            ETF50  ETF300  ETF500
date                             
2018-05-06  2.634   3.770   1.646
2018-05-13  2.716   3.873   1.667
2018-05-20  2.733   3.899   1.670
2018-05-27  2.654   3.811   1.649
2018-06-03  2.643   3.777   1.588
```



**月收益率数据**

`aip.monthly.pct_change().describe()`

```
           ETF50     ETF300     ETF500
count  60.000000  60.000000  60.000000
mean    0.008889   0.009014   0.009978
std     0.076945   0.073923   0.081489
min    -0.182533  -0.224457  -0.279845
25%    -0.022543  -0.018264  -0.025160
50%     0.002254   0.006061   0.015203
75%     0.035246   0.041125   0.049516
max     0.334728   0.254035   0.204142
```



接下来在定义用来比较的函数

```python
def compare(underlying,df_period,times=15,money=1000,plot=False):
    df_period[underlying].plot(figsize=(9,6),title='{} close price'.format(underlying))
    result = []
    for _ in range(times):
        start = random.choice(df_period.index[:int(df_period.index.size / 2)])
        end = random.choice(df_period.loc[start + pd.Timedelta(18,unit='M'):].index)
        d = df_period.loc[start:end,:]
        cumsum_values = pd.DataFrame((money / d.loc[:,underlying]))
        cumsum_values.columns = ['share_period']
        cumsum_values['share_cum'] = cumsum_values['share_period'].cumsum()
        cumsum_values['values'] = cumsum_values.share_cum * d.loc[:,underlying]
        cumsum_values['payoff'] = [i*money for i in range(1,cumsum_values.index.size+1)]
        
        a = d.loc[:,underlying] / d.loc[d.index[0],underlying]
        b = cumsum_values['values'] / cumsum_values['payoff']
        b.name = 'AIP'
        df = pd.concat([a,b],axis=1)
        if plot:
            df.plot()
        exceed = pd.np.subtract(*df.iloc[-1])
        print('from {} to {},dirctly invest ETF exceed AIP {:.2%}'.format(start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),exceed))
        result.append(exceed)
    print('\nIn {} times simulation,dirctly invest ETF exceed AIP\'s mean is {:.2%}'.format(times,pd.np.mean(result)))

```

这个比较函数从给定的ETF基金中的前半段时间随机选取一个日期，然后至少持有18个月，至多持有到当前日期，用这段时间的数据分别模拟在初始日期全部投资至结束和在区间内定投的收益情况。使用方法如下：

```
#用每月定投1000元ETF50来比较
compare('ETF50',aip.monthly)

#用每周定投1000元ETF500来比较
compare('ETF500',aip.weekly)

#用每周定投500元ETF300来比较，共模拟10次，每次打印出走势对比图
compare('ETF300',aip.weekly,times=10,money=500,plot=True)
```



### 比较结果

`compare('ETF50',aip.monthly)`

```
from 2015-09-30 to 2017-08-31,dirctly invest ETF exceed AIP 8.07%
from 2014-07-31 to 2016-06-30,dirctly invest ETF exceed AIP 30.34%
from 2014-09-30 to 2017-08-31,dirctly invest ETF exceed AIP 45.93%
from 2015-05-31 to 2017-12-31,dirctly invest ETF exceed AIP -26.74%
from 2014-03-31 to 2017-06-30,dirctly invest ETF exceed AIP 54.43%
from 2015-09-30 to 2017-04-30,dirctly invest ETF exceed AIP 4.29%
from 2015-07-31 to 2017-04-30,dirctly invest ETF exceed AIP -9.27%
from 2014-06-30 to 2016-10-31,dirctly invest ETF exceed AIP 47.17%
from 2015-07-31 to 2017-09-30,dirctly invest ETF exceed AIP -7.44%
from 2014-10-31 to 2016-06-30,dirctly invest ETF exceed AIP 31.91%
from 2014-07-31 to 2017-11-30,dirctly invest ETF exceed AIP 46.67%
from 2015-06-30 to 2017-08-31,dirctly invest ETF exceed AIP -22.72%
from 2014-04-30 to 2017-06-30,dirctly invest ETF exceed AIP 52.55%
from 2014-04-30 to 2016-12-31,dirctly invest ETF exceed AIP 44.92%
from 2014-04-30 to 2015-10-31,dirctly invest ETF exceed AIP 41.97%

In 15 times simulation,dirctly invest ETF exceed AIP's mean is 22.81%
```



`compare('ETF500',aip.weekly)`

```
from 2014-09-28 to 2017-07-09,dirctly invest ETF exceed AIP 28.72%
from 2014-06-08 to 2017-05-07,dirctly invest ETF exceed AIP 56.41%
from 2015-05-10 to 2018-04-29,dirctly invest ETF exceed AIP -20.97%
from 2014-02-09 to 2017-06-18,dirctly invest ETF exceed AIP 45.50%
from 2014-06-29 to 2016-07-17,dirctly invest ETF exceed AIP 55.89%
from 2015-07-12 to 2017-10-15,dirctly invest ETF exceed AIP -15.83%
from 2013-06-02 to 2017-04-30,dirctly invest ETF exceed AIP 40.71%
from 2014-06-08 to 2016-10-02,dirctly invest ETF exceed AIP 57.17%
from 2014-05-11 to 2018-01-07,dirctly invest ETF exceed AIP 64.35%
from 2014-09-07 to 2017-04-02,dirctly invest ETF exceed AIP 33.36%
from 2014-07-20 to 2018-03-25,dirctly invest ETF exceed AIP 47.74%
from 2014-03-30 to 2017-06-11,dirctly invest ETF exceed AIP 50.51%
from 2013-09-15 to 2015-11-22,dirctly invest ETF exceed AIP 44.02%
from 2015-03-08 to 2017-04-09,dirctly invest ETF exceed AIP 6.61%
from 2015-04-05 to 2017-01-29,dirctly invest ETF exceed AIP -13.85%

In 15 times simulation,dirctly invest ETF exceed AIP's mean is 32.02%
```

从上面的运行结果来看，把资金一次性全部投入比定投的平均收益是要高的，如果有兴趣，可以自己修改程序，改变开始和结束时间来验证结果，相信结论应该上面的相差不会太多。

当然，定投也不是一无是处，至少对于当前资金不足，只想从每月工资中拿出一部分来投资的人来说，还是一种很好的投资方式的。



###  完整代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import random
import matplotlib.pyplot as plt

class AutoInvestmentPlan:
    def __init__(self):
        plt.style.use('ggplot')
        self.code_list = ['510050','510300','510510']
        self.start_date = '2013-05-27'
    
    def get_etf_close(self,code,start):
        df = ts.get_k_data(code,start=start)
        df.set_index('date',inplace=True)
        df.index = pd.to_datetime(df.index)
        return df.close

    def combin_to_df(self):
        close_list = []
        for code in self.code_list:
            close_list.append(self.get_etf_close(code,self.start_date))
        self.data = pd.concat(close_list,axis=1)
        self.data.columns = ['ETF50','ETF300','ETF500']

    def get_data(self):
        self.combin_to_df()
        self.monthly = self.data.asfreq('M',method='pad')
        self.weekly = self.data.asfreq('W',method='pad')


def compare(underlying,df_period,times=15,money=1000,plot=False):
    df_period[underlying].plot(figsize=(9,6),title='{} close price'.format(underlying))
    result = []
    for _ in range(times):
        start = random.choice(df_period.index[:int(df_period.index.size / 2)])
        end = random.choice(df_period.loc[start + pd.Timedelta(18,unit='M'):].index)
        d = df_period.loc[start:end,:]
        cumsum_values = pd.DataFrame((money / d.loc[:,underlying]))
        cumsum_values.columns = ['share_period']
        cumsum_values['share_cum'] = cumsum_values['share_period'].cumsum()
        cumsum_values['values'] = cumsum_values.share_cum * d.loc[:,underlying]
        cumsum_values['payoff'] = [i*money for i in range(1,cumsum_values.index.size+1)]
        
        a = d.loc[:,underlying] / d.loc[d.index[0],underlying]
        b = cumsum_values['values'] / cumsum_values['payoff']
        b.name = 'AIP'
        df = pd.concat([a,b],axis=1)
        if plot:
            df.plot()
        exceed = pd.np.subtract(*df.iloc[-1])
        print('from {} to {},dirctly invest ETF exceed AIP {:.2%}'.format(start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),exceed))
        result.append(exceed)
    print('\nIn {} times simulation,dirctly invest ETF exceed AIP\'s mean is {:.2%}'.format(times,pd.np.mean(result)))

```

