
# python模块之time

[time官方文档是最好的模块表达说明。](https://docs.python.org/3.6/library/time.html)

通常处理日期和时间的方式在于时间戳和字符串式时间转换，python里面又加入了结构化时间元组的方式，即存在时间戳、字符串时间戳和时间元组三种方式之间的转换。

# 1、基础

python中时间日期格式化符号：

	%y 		两位数的年份表示（00-99）
	%Y 		四位数的年份表示（000-9999）
	%m 		月份（01-12）
	%d 		月内中的一天（0-31）
	%H 		24小时制小时数（0-23）
	%I 		12小时制小时数（01-12）
	%M 		分钟数（00=59）
	%S 		秒（00-59）
	%a 		本地简化星期名称
	%A 		本地完整星期名称
	%b 		本地简化的月份名称
	%B 		本地完整的月份名称
	%c 		本地相应的日期表示和时间表示
	%j 		年内的一天（001-366）
	%p 		本地A.M.或P.M.的等价符
	%U 		一年中的星期数（00-53）星期天为星期的开始
	%w 		星期（0-6），星期天为星期的开始
	%W 		一年中的星期数（00-53）星期一为星期的开始
	%x 		本地相应的日期表示
	%X 		本地相应的时间表示
	%Z 		当前时区的名称
	%% 		%号本身

时间元组：python函数用一个元组装起来的9组数字处理时间。

	struct_time(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)

| index | attr     | name     | value |
| :---: | :------: | :------: | :---: |
| 0     | tm_year  | 年       | 2008  |
| 1     | tm_mon   | 月       | 1-12  |
| 2     | tm_mday  | 日       | 1-31  |
| 3     | tm_hour  | 时       | 0-23  |
| 4     | tm_min   | 分       | 0-59  |
| 5     | tm_sec   | 秒       | 0-61  |
| 6     | tm_wday  | 周日     | 0-6   |
| 7     | tm_yday  | 年日     | 1-366 |
| 8     | tm_isdst | 夏令时   | 0 1 -1|

- 秒60、61是闰秒。
- 周日：0是周一。
- 年日是儒略历。
- 夏令时：1(夏令时)、0(不是夏令时)、-1(未知)，默认 -1 。

# 2、time

时间操作的3中方式：

- 时间戳：1970年1月1日之后的秒，time.time()
- 格式化的字符串：2017-11-08 13:13 , time.strftime('%Y-%m-%d')
- 结构化时间元组：元组形式见上面基础，time.struct_time()

**1、时间戳**

**time.time()**：返回当前时间的时间戳（1970纪元后经过的浮点秒数）。

	>>> time.time()
	1510119901.2839558
	>>> int(time.time())
	1510119949

**2、结构化时间元组**

**time.localtime([secs])**：接收时间辍（1970纪元后经过的浮点秒数）并返回当地时间下的时间元组t（t.tm_isdst可取0或1，取决于当地当时是不是夏令时）。

	>>> t=time.localtime(time.time())
	>>> print(t)
	time.struct_time(tm_year=2017, tm_mon=11, tm_mday=8, tm_hour=14, tm_min=0, tm_sec=49, tm_wday=2, tm_yday=312, tm_isdst=0)
	>>> t[0]
	2017

**time.gmtime([secs])**：接收时间辍（1970纪元后经过的浮点秒数）并返回格林威治天文时间下的时间元组t。注：t.tm_isdst始终为0。

	>>> t=time.gmtime(time.time())
	>>> print(t)
	time.struct_time(tm_year=2017, tm_mon=11, tm_mday=8, tm_hour=6, tm_min=6, tm_sec=0, tm_wday=2, tm_yday=312, tm_isdst=0)

**time.mktime(tupletime)**：接受时间元组并返回时间辍。

	>>> time.mktime((2017, 11, 8, 14, 0, 49, 2, 312, 0))
	1510120849.0

**3、结构化时间字符串**

**time.strftime(fmt[,tupletime])**：接收时间元组，并返回可读字符串表示的当地时间，格式由fmt指定。

	>>> print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
	2017-11-08 14:10:42

**time.strptime(str,fmt='%a %b %d %H:%M:%S %Y')**：把fmt指定的时间字符串解析为时间元组。

	>>> time.strptime('2017-11-08 14:10:42', '%Y-%m-%d %H:%M:%S')
	time.struct_time(tm_year=2017, tm_mon=11, tm_mday=8, tm_hour=14, tm_min=10, tm_sec=42, tm_wday=2, tm_yday=312, tm_isdst=-1)

**time.asctime([tupletime])**：接收时间元组并返回一个可读形式为'Wed Nov  8 14:14:32 2017'（2017年11月8日 周三14时14分32秒）的24个字符的字符串。

	>>> time.asctime(time.localtime())
	'Wed Nov  8 14:14:32 2017'

**time.ctime([secs])**：作用相当time.asctime([tupletime])，接收时间戳。

	>>> time.ctime()
	'Wed Nov  8 14:15:46 2017'
	>>> time.ctime(time.time())
	'Wed Nov  8 14:16:40 2017'

**time.sleep(secs)**：推迟调用线程的运行，让线程睡一会，secs指秒数。（手速问题，命令行执行的）

	>>> print('start %s' % time.time())
	start 1510122104.372965
	>>> time.sleep(5)
	>>> print('end %s' % time.time())
	end 1510122117.780732

**time.clock()**：用以浮点数计算的秒数返回当前的CPU时间。用来衡量不同程序的耗时，比time.time()更有用。

	>>> time.clock()
	2.4444447548501278e-06

以上只包含通常可能会用到的函数，更多见头部链接官网。

![time表现形式转换](https://i.imgur.com/9AUg98A.png)

另外常用的日期时间模块有datetime和calendar，有兴趣的可以直接去其脚本文件进行查看。

这两个模块同样可以在官网找到，将不做赘述。



