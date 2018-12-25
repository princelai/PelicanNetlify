Title: 对比三种tf-idf提取关键词的效果
Date: 2018-12-25 18:25
Category: 机器学习
Tags: 分词,tf-idf,python
Slug: compare-tfidf
Authors: Kevin Chen



> **tf-idf**（英语：**t**erm **f**requency–**i**nverse **d**ocument **f**requency）是一种用于信息检索与文本挖掘的常用加权技术。tf-idf是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。tf-idf加权的各种形式常被搜索引擎应用，作为文件与用户查询之间相关程度的度量或评级。除了tf-idf以外，互联网上的搜索引擎还会使用基于链接分析的评级方法，以确定文件在搜索结果中出现的顺序。([WikiPedia](https://zh.wikipedia.org/wiki/Tf-idf))



在我的工作流程中，中文分词后往往最重要的事情是提取关键词，正如文章开头写到的，tf-idf法作为历史悠久的统计方法，效果优秀，原理和实现简单，成为必须尝试的提取关键词方法之一。而Python中能提供该方法的库有很多，哪种效果最优，哪种速度最快一直是我想要比较的，今天抽出时间写个对比小程序来看看结果，本次测试对比三种方法：jieba、sklearn、gensim。



### 测试方法

1. 数据使用我自己爬的投融资类新闻，共计14100篇。
2. 使用jieba_fast替代结巴，加快分词和tf-idf速度，jieba使用默认词频文件，不需建模。
3. 所有需要建模的方法都提前对新闻数据使用jieba分词，使用精确模式，同时加载我自己的词库，用于发现未登录词。
4. 随机选择三篇文章，每篇文章最后要得出前五高词频的词，即为该文章的关键词，同时给出tf-idf值。

注：由于jieba提取关键词需要使用句子从零提取，而其他方法使用之前已经分好词的序列，故虽然jieba不需要建模，但是提取关键词时间可能会更长。



### 建模时间

对于14000+篇文章，十几万甚至几十万的有效词来说，sklearn和gensim的建模时间不算太长，毕竟还有很大一部分时间花在了循环和稀疏矩阵转数组的过程。而两个方法时差也不足1秒，这部分水平接近。

> ###############生成模型时间###############
>    jieba      sklearn      gensim    
>    0.000       18.689      19.312    
>
> ########################################



### 提取关键词效果

#### 第一篇文章

从耗时上看，由于只保留了小数点后三位，只能得出大致的结论，jieba提取关键词需要的时间是sklearn的4倍，是gensim的2倍。tf-idf值也是后两种更为接近，jieba使用默认的词频文件对很多生僻词的文章来说不太准确。给出的前五个关键词也是后两种更为接近，也更准确一点，但整体来说区别不大。

> 第3581号文章
>
> 标题：EZZY、友友用车之后，途歌会是下一家倒下的共享汽车公司吗？
>
> ###############jieba###############
>
> 排名   词                   TF-IDF
>
> 1    共享汽车                0.257
>
> 2    途歌                  0.231
>
> 3    共享单车                0.103
>
> 4    分时租赁                0.103
>
> 5    融资                  0.100
>
> 耗时：       0.004      
>
>
> ###############sklearn###############
>
> 排名   词                   TF-IDF
>
> 1    途歌                  0.474
>
> 2    共享汽车                0.427
>
> 3    王利峰                 0.177
>
> 4    分时租赁                0.176
>
> 5    押金                  0.146
>
> 耗时：       0.001      
>
>
> ###############gensim###############
>
> 排名   词                   TF-IDF
>
> 1    途歌                  0.506
>
> 2    共享汽车                0.437
>
> 3    王利峰                 0.194
>
> 4    分时租赁                0.182
>
> 5    mocar               0.165
>
> 耗时：       0.002      
>
>
>
>
> 第7443号文章
>
> 标题：你的流量，变现了吗？
>
> ###############jieba###############
>
> 排名   词                   TF-IDF
>
> 1    用户                  0.213
>
> 2    裂变                  0.092
>
> 3    产品                  0.086
>
> 4    营销                  0.075
>
> 5    漏斗                  0.074
>
> 耗时：       0.019      
>
>
> ###############sklearn###############
>
> 排名   词                   TF-IDF
>
> 1    漏斗                  0.312
>
> 2    用户                  0.312
>
> 3    裂变                  0.288
>
> 4    他们                  0.190
>
> 5    产品                  0.181
>
> 耗时：       0.003      
>
>
> ###############gensim###############
>
> 排名   词                   TF-IDF
>
> 1    漏斗                  0.377
>
> 2    裂变                  0.321
>
> 3    用户                  0.173
>
> 4    营销                  0.156
>
> 5    热爱                  0.155
>
> 耗时：       0.007     



#### 第二篇文章

用时上，jieba耗时是后两者的6.3倍和2.7倍。tf-idf值还是同样的问题，后面不在赘述。准确度方面，jieba和gensim结果相同，而sklearn出现了“我们”这个词明显不应该是高频关键词，当然最优的做法还是在分词的时候就把这类词加入stop word。

> 第7443号文章
> 标题：你的流量，变现了吗？
> ###############jieba###############
> 排名   词                   TF-IDF
> 1    用户                  0.213
> 2    裂变                  0.092
> 3    产品                  0.086
> 4    营销                  0.075
> 5    漏斗                  0.074
> 耗时：       0.019      
> ###############sklearn###############
> 排名   词                   TF-IDF
> 1    漏斗                  0.312
> 2    用户                  0.312
> 3    裂变                  0.288
> 4    他们                  0.190
> 5    产品                  0.181
> 耗时：       0.003      
> ###############gensim###############
> 排名   词                   TF-IDF
> 1    漏斗                  0.377
> 2    裂变                  0.321
> 3    用户                  0.173
> 4    营销                  0.156
> 5    热爱                  0.155
> 耗时：       0.007     



#### 第三篇文章

耗时方面jieba是sklearn的8.5倍，是gensim的3.4倍。准确度方面，jieba和sklearn更为相似，但往往我们期望的结果更倾向于gensim那样，所以哪种好哪种坏还是见仁见智。

> 13453号文章
> 标题：VC/PE如何掘金医疗健康？
> ###############jieba###############
> 排名   词                   TF-IDF
> 1    我们                  0.120
> 2    佛山                  0.064
> 3    一个                  0.060
> 4    医疗行业                0.056
> 5    这个                  0.051
> 耗时：       0.017      
> ###############sklearn###############
> 排名   词                   TF-IDF
> 1    我们                  0.320
> 2    佛山                  0.282
> 3    政策                  0.160
> 4    一个                  0.159
> 5    医疗行业                0.153
> 耗时：       0.002      
> ###############gensim###############
> 排名   词                   TF-IDF
> 1    佛山                  0.339
> 2    薛轶                  0.205
> 3    医疗行业                0.179
> 4    姜阳                  0.171
> 5    张寅                  0.171
> 耗时：       0.005     



### 结论

为了节约篇幅，测试到此打住，下面给出代码，愿意自己测试的可以拿去修改。由于我自己测试了几十篇文章不能全部贴到这里，所以结论会结合本篇文章+过往我看过的结果。

**准确度：**gensim $\approx$ sklearn $\gt$ jieba，如果要是为jieba单独计算tf-df词频，那结果可能更接近，如果非要在这三个里选注一个准确度最好的，那我**推荐gensim**。

**速度：**首先要分两种情况，需要提取关键词的文章大于5000篇，那么需要计算tf-idf模型的sklearn和gensim更有优势，因为这两种建模后提取关键词更快，如果只有少量文章，那么你真的会在乎那三五秒的模型时间吗？



### 代码

```python
import re
import time
from functools import wraps
from random import randint

import jieba_fast as jieba
import jieba_fast.analyse as analyse
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

# 预加载
tqdm.pandas()
jieba.load_userdict("your userdict.txt")
onlyNum = re.compile("^[\\d.]+$")

# mongo中存着新闻
client = MongoClient('mongodb://localhost:27017/')
db = client['db_mongo']
collection = db["news"]

# 获取全部新闻，格式为DataFrame
dfnews = pd.DataFrame(list(collection.find({}, {"_id": 0, "title": 1, "contents": 1})))
dfnews.title = dfnews.title.astype(str)
dfnews.contents = dfnews.contents.astype(str)

# 为后续tf-idf建模准备分词
segement_all = dfnews.contents.progress_apply(
    lambda x: [i.lower().strip() for i in jieba.cut(x) if (len(i) >= 2) and (not bool(onlyNum.search(i)))])
segement_all_sk = segement_all.progress_apply(lambda x: ' '.join(x))

# sklearn tf-idf建模
t1_start = time.time()
vectorizer = TfidfVectorizer()
tfidf_sk = vectorizer.fit_transform(segement_all_sk.values)
weight_sk = tfidf_sk.toarray()
t1_end = time.time()

# gensim tf-idf建模
t2_start = time.time()
dictionary = Dictionary(segement_all)
corpus = [dictionary.doc2bow(text) for text in segement_all.values]
tfidf_gensim = TfidfModel(corpus)
id2token = {v: k for k, v in dictionary.token2id.items()}
t2_end = time.time()

print("{0}{1}{0}".format("#" * 15, "生成模型时间"))
print("{0:^12s}{1:^12s}{2:^12s}".format("jieba", "sklearn", "gensim"))
print("{0:^12.3f}{1:^12.3f}{2:^12.3f}".format(0.0, t1_end - t1_start, t2_end - t2_start))
print("{0}".format("#" * 40))


def header(alias):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("{0}{1}{0}".format("#" * 15, alias))
            print("{0:<5}{1:<20s}{2}".format("排名", "词", "TF-IDF"))
            t_func = time.time()
            func(*args, **kwargs)
            print("{0:<10s}{1:<10.3f}\n".format("耗时：", time.time() - t_func))

        return wrapper

    return decorate


def compare_result(idx, top=5):
    formatter = "{0:<5}{1:<20s}{2:.3f}"
    title = dfnews.title.iloc[idx]
    segment = dfnews.contents.iloc[idx]
    text = [i.lower() for i in list(jieba.cut(segment)) if (len(i) >= 2) and (not bool(onlyNum.search(i)))]
    segment_clean = ' '.join(text)
    print(f"\n第{idx}号文章\n标题：{title}")

    @header("jieba")
    def jieba_result():
        for i, (w, n) in enumerate(jieba.analyse.extract_tags(segment_clean, topK=top, withWeight=True), 1):
            print(formatter.format(i, w, n))

    @header("sklearn")
    def sklearn_result():
        sklearn_dict = {}
        for t in text:
            try:
                vocab = vectorizer.vocabulary_.get(t)
                assert vocab is not None
            except AssertionError:
                continue
            else:
                sklearn_dict[t] = weight_sk[idx][vocab]
        for i, (w, n) in enumerate(sorted(sklearn_dict.items(), key=lambda x: x[1], reverse=True)[:top], 1):
            print(formatter.format(i, w, n))

    @header("gensim")
    def gensim_result():
        gensim_dict = {}
        for w, n in tfidf_gensim[corpus[idx]]:
            gensim_dict[id2token.get(w)] = n
        for i, (w, n) in enumerate(sorted(gensim_dict.items(), key=lambda x: x[1], reverse=True)[:top], 1):
            print(formatter.format(i, w, n))

    jieba_result()
    sklearn_result()
    gensim_result()


if __name__ == "__main__":
    for _ in range(3):
        compare_result(randint(0, dfnews.index.size))

```

