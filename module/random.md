# python模块之random

# 1、random

python中的random模块用于生成随机数。下面介绍常用的一些函数。

[random官方文档是最好的模块表达说明。](https://docs.python.org/3.6/library/random.html)


**dir(random)**：查看random模块下面有哪些函数。

	>>> import random
	>>> dir(random)
	['BPF', 'LOG4', 'NV_MAGICCONST', 'RECIP_BPF', 'Random', 'SG_MAGICCONST', 'SystemRandom', 'TWOPI', '_Builti
	nMethodType', '_MethodType', '_Sequence', '_Set', '__all__', '__builtins__', '__cached__', '__doc__', '__f
	ile__', '__loader__', '__name__', '__package__', '__spec__', '_acos', '_bisect', '_ceil', '_cos', '_e', '_
	exp', '_inst', '_itertools', '_log', '_pi', '_random', '_sha512', '_sin', '_sqrt', '_test', '_test_generat
	or', '_urandom', '_warn', 'betavariate', 'choice', 'choices', 'expovariate', 'gammavariate', 'gauss', 'get
	randbits', 'getstate', 'lognormvariate', 'normalvariate', 'paretovariate', 'randint', 'random', 'randrange
	', 'sample', 'seed', 'setstate', 'shuffle', 'triangular', 'uniform', 'vonmisesvariate', 'weibullvariate']

常用函数有：

## 1.1 产生一个随机数（元素）

**random.random()**：用于产生一个0到1 的随机浮点数，0<=n<1。

	>>> random.random()
	0.052603181609407135				
	>>> round(random.random(), 2)
	0.13								# 四舍五入取两位小数

**random.uniform(a, b)**：用于生成一个指定范围内的随机符点数，两个参数其中一个是上限，一个是下限。如果a>b，则生成的随机数n:a<=n<=b。如果a<b，则 b<=n<=a。

	>>> random.uniform(10, 20)
	18.269306458836333
	>>> random.uniform(20, 10)
	10.804263239022113

**random.randint(a, b)**：用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，a、b不可颠倒、生成的随机数:a<=n<=b。

	>>> random.randint(10, 20)
	13
	>>> random.randint(20, 10)
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	  File "C:\software\python\lib\random.py", line 220, in randint
	    return self.randrange(a, b+1)
	  File "C:\software\python\lib\random.py", line 198, in randrange
	    raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))
	ValueError: empty range for randrange() (20,11, -9)

**random.randrange([start], stop[, step])**：从指定范围内，按指定基数递增的集合中获取一个随机数。

	>>> random.randrange(10, 20, 2)
	14									# 即从[10, 12, 14, 16, …18]序列中获取一个随机数。在结果上与 random.choice(range(10, 100, 2)等效。

**random.choice(sequence)**：从指定序列随机获取元素。参数sequence表示一个有序类型，见数据类型。

	>>> random.choice(('daocoder', 'mudai', 'godao'))
	'daocoder'
	>>> random.choice(['daocoder', 'mudai', 'godao'])
	'godao'


## 1.2 产生一个随机序列

**random.shuffle(x[, random])**：用于将一个列表中的元素打乱。修改原有序列。

	>>> a=['daocoder', 'mudai', 'godao']
	>>> random.shuffle(a)
	>>> a
	['daocoder', 'godao', 'mudai']

**random.sample(sequence, k)**：从指定序列中随机获取指定长度的片断。不会修改原有序列。

	>>> a=['daocoder', 'mudai', 'godao', 'zhangsan', 'lisi', 'wangwu']
	>>> random.sample(a, 5)
	['godao', 'zhangsan', 'daocoder', 'lisi', 'mudai']
	>>> random.sample(a, 4)
	>>>> a
	['daocoder', 'mudai', 'godao', 'zhangsan', 'lisi', 'wangwu']