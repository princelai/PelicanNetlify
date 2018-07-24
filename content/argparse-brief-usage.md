Title: argparse模块简要用法
Date: 2018-01-08 17:41
Category: IT笔记
Tags: python,argparse
Slug: argparse-brief-usage
Authors: Kevin Chen

argparse是Python用于解析命令行参数的模块，拥有更强大的功能、更友好的使用方法，用来替代原始的sys.argv。

argparse的大致用法如下：

```python
import argparse #导入模块
parser = argparse.ArgumentParser() #创建解析器
parser.add_argument() #添加参数
args = parser.parse_args() #解析参数
```

创建解析器时的可选参数很多，但没有特殊需求的情况下，默认参数就能很好的工作，所以这部分使用时临时查文档就能解决，不做过多记录。

这里仅记录下添加参数时的各种选项搭配，使用方法和选项如下：

```python
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
```

每一个参数的含义：

> -   name or flags - 名称或选项字符串列表，例如。foo或-f, --foo。

-   action - 在命令行遇到此参数时要执行的操作的基本类型。
-   nargs - 应该使用的命令行参数数。
-   const - 某些动作和nargs选择所需的常量值。
-   default - 如果参数在命令行中不存在，则生成的值。
-   type - 应转换命令行参数的类型。
-   choices - 参数的允许值的容器。
-   required - 是否可以省略命令行选项（仅针对可选参数）。
-   help - 参数的简要说明。
-   metavar - 使用消息中参数的名称。
-   dest - 要添加到由parse_args()返回的对象的属性的名称。

### 1. name or flags

唯一的必填参数，可以创建位置参数（必填）和可选参数

```python
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-s','--save')
parser.add_argument('db')
parser.parse_args(['mysql'])
Out[1]: Namespace(db='mysql', save=None)
```

可选参数以`-`或`--`开始，其余的均为位置参数
大部分情况下，未填的可选参数默认都是`None`,如果有`--`开始的参数，则参数名以后面的字符串命名。

### 2. action

action用于将命令和动作关联起来，常用的动作有如下几种：

-   store - 仅保存参数后的值
-   store_const - 保存一个常量，由const参数给出
-   store_true - 给出参数则保存True值，不给出则为False
-   store_false - 与上面相反
-   append - 把多次调用的值保存为一个列表
-   append_const - 把多次调用的常量保存为一个列表
-   count - 计算参数出现的次数
-   help - 打印帮助信息，默认自动添加
-   version - 打印版本信息，配合version选项使用

举几个例子

```python
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-sh','--show',action='store_true')
parser.parse_args(['-sh'])
Out[2]: Namespace(show=True)
```

给出`-sh`参数，则show值为True

```python
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-a1','--arg1',action='store_const',const=0)
parser.add_argument('-a2','--arg2',action='store_const',const=10,default=None)
parser.add_argument('-a3','--arg3',action='store_const',const=True,default=False)
parser.parse_args(['-a1'])
Out[22]: Namespace(arg1=0, arg2=None, arg3=False)
```

只给出a1参数，arg1的值为0。
没有给出a2参数，则a2的const没有被调用，使用default的值，当然default默认就是None，不写也可以。
a3参数其实就是store_true的实现。
const和default的区别就是当命令给出但是后面未接值时，使用const值，如果命令那个都没有给出，则使用default的值。

### 3. nargs

nargs定义参数后面值的个数，可选值有几种：

> -   N (一个整数)
> -   ?
> -   \*
> -   \+

如果懂正则表达式，那nargs的参数就很好理解，这里就不做过多解释，不过要注意一点，当nargs=1的时候，他的行为和不给出nargs是不一样的，前者是一个列表，后者是一个值。直接看例子：

```python
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('a1',nargs=2)
parser.add_argument('-a2','--args2',nargs='?',const=0)
parser.add_argument('-a3','--args3',nargs='+',default=False)
parser.parse_args(['a','b','-a3','aa','bb'])
Out[3]: Namespace(a1=['a', 'b'], args2=None, args3=['aa', 'bb'])
```

结果很好理解，?可以配合const使用，其他的可以配合default使用，调用了就是一个列表，使用const或default就是一个值。

### 4. type和metavar

这两个参数偶尔能用到，

```python
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('a1',type=float)
parser.add_argument('-a2','--args2',metavar='STR',default=argparse.SUPPRESS)
parser.parse_args(['3'])
```

<code>default=argparse.SUPPRESS</code>指出不给参数不存储变量，否则默认是None，
打印help说明看看

```python
parser.print_help()
usage: PROG [-h] [-a2 STR] a1

positional arguments:
  a1

optional arguments:
  -h, --help            show this help message and exit
  -a2 STR, --args2 STR
```

metavar仅改变了help说明里的变量名。

### 参考文档

1.  [官方文档][1]
2.  [中文文档][2]

[1]: https://docs.python.org/3/library/argparse.html

[2]: http://python.usyiyi.cn/translate/python_352/library/argparse.html
