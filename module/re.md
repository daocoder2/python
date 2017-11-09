# python模块之time

[re：官方文档是最好的模块表达说明。](https://docs.python.org/3.6/library/re.html)

Regular expression operations

正则表达式(regular expression)描述了一种字符串匹配的模式，可以用来检查一个串是否含有某种子串、将匹配的子串做替换或者从某个串中取出符合某个条件的子串等。

正则表达式是由普通字符（例如字符a到z）以及特殊字符（称为"元字符"）组成的文字模式。模式描述在搜索文本时要匹配的一个或多个字符串。正则表达式作为一个模板，将某个字符模式与所搜索的字符串进行匹配。

## 1、正则语法

**普通字符包括没有显式指定为元字符的所有可打印和不可打印字符。这包括所有大写和小写字母、所有数字、所有标点符号和一些其他符号。**

| 非打印字符 |                   描述                      |
| :--------: | :------------------------------------------ |
| \f	     | 匹配一个换页符。等价于\x0c和\cL。           |
| \n         | 匹配一个换行符。等价于\x0a和\cJ。           |
| \r         | 匹配一个回车符。等价于\x0d和\cM。           |
| \s         | 匹配任何空白字符，包括空格、制表符、换页符等。等价于[\f\n\r\t\v]。|
| \S         | 匹配任何非空白字符。等价于[^\f\n\r\t\v]。   |
| \t         | 匹配一个制表符。等价于\x09和\cI。           |
| \v         | 匹配一个垂直制表符。等价于\x0b和\cK。       |
| \d         | 匹配ASCII数字，等价[0-9]。                  |
| \D         | 匹配非ASCII数字，等价[^0-9]。               |
| \u         | 匹配十六进制数****指定的unicode字符。      |
| \w         | 匹配ASCII字符组成的单词，等价[a-zA-Z0-9]。  |
| \W         | 匹配非ASCII字符组成的单词，等[^a-zA-Z0-9]。 |

**特殊字符，就是一些有特殊含义的字符。**如上面说的"\*.txt"中的\*，简单的说就是表示任何字符串的意思。如果要查找文件名中有\*的文件，则需要对\*进行转义，即在其前加一个\\。ls \*.txt。

许多元字符要求在试图匹配它们时特别对待。若要匹配这些特殊字符，必须首先使字符"转义"，即，将反斜杠字符 (\\) 放在它们前面。

| 特别字符 |                   描述                      |
| :------: | :------------------------------------------ |
| $	       | 匹配输入字符串的结尾位置。如果设置了RegExp对象的Multiline属性，则$也匹配'\n'或'\r'。要匹配$字符本身，请使用\$。           |
| ()       | 标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符，请使用\\(和\\)。|
| *	       | 匹配前面的子表达式零次或多次。要匹配\*字符，请使用\\*。|
| +	       | 匹配前面的子表达式一次或多次。要匹配+字符，请使用\\+。|
| .	       | 匹配除换行符\n之外的任何单字符。要匹配.，请使用\\.。|
| ?	       | 匹配前面的子表达式零次或一次，或指明一个非贪婪限定符。要匹配?字符，请使用\?。|
| \	       | 将下一个字符标记为或特殊字符、或原义字符、或向后引用、或八进制转义符。例如，'n'匹配字符'n'。'\n'匹配换行符。序列'\\\'匹配"\"，而'\\('则匹配"("。|
| ^	       | 匹配输入字符串的开始位置，除非在方括号表达式中使用，此时它表示不接受该字符集合。要匹配^字符本身，请使用\\^。|
| {	       | 标记限定符表达式的开始。要匹配{，请使用\\{。|
| [	       | 标记一个中括号表达式的开始。要匹配[，请使用\\[。|
| 竖线	   | 指明两项之间的一个选择。要匹配‘竖线’，请使用‘\竖线’。|

> tip：markdown语法问题，上面竖线表示‘|’字符。

**限定符，用来指定正则表达式的一个给定组件必须要出现多少次才能满足匹配。**有*或+或?或{n}或{n,}或{n,m}共6种。

| 限定符 |                   描述                      |
| :----: | :------------------------------------------ |
| *	     | 匹配前面的子表达式零次或多次。例如，zo*能匹配"z"以及"zoo"。*等价于{0,}。                                 |
| +	     | 匹配前面的子表达式一次或多次。例如，'zo+'能匹配"zo"以及"zoo"，但不能匹配"z"。+等价于{1,}。                  |
| ?	     | 匹配前面的子表达式零次或一次。例如，"do(es)?"可以匹配"do"或"does"中的"do"。?等价于{0,1}。                 |
| {n}    | n是一个非负整数。匹配确定的n次。例如，'o{2}'不能匹配"Bob"中的'o'，但是能匹配"food"中的两个o。            |
| {n,}	 | n是一个非负整数。至少匹配n次。例如，'o{2,}'不能匹配"Bob"中的'o'，但能匹配"foooood"中的所有o。'o{1,}'等价于'o+'。'o{0,}'则等价于'o*'。                                    |
| {n,m}  | m和n均为非负整数，其中n<=m。最少匹配n次且最多匹配m次。例如，"o{1,3}"将匹配"fooooood"中的前三个o。'o{0,1}'等价于'o?'。请注意在逗号和两个数之间不能有空格。                     |

**定位符用来描述字符串或单词的边界。**^和$分别指字符串的开始与结束，\b描述单词的前或后边界，\B表示非单词边界。

定位符使您能够将正则表达式固定到行首或行尾。它们还使您能够创建这样的正则表达式，这些正则表达式出现在一个单词内、在一个单词的开头或者一个单词的结尾。

| 定位符 |                   描述                      |
| :----: | :------------------------------------------ |
| ^	     | 匹配输入字符串开始的位置。如果设置了RegExp对象的Multiline属性，^还会与\n或\r之后的位置匹配。           |
| $	     | 匹配输入字符串结尾的位置。如果设置了RegExp对象的Multiline属性，$还会与\n或\r之前的位置匹配。           |
| \b	 | 匹配一个字边界，即字与空格间的位置。        |
| \B     | 非字边界匹配。                              |

**修饰符用以说明高级匹配的规则。**

| 修饰符 |                   描述                      |
| :----: | :------------------------------------------ |
| I	     | 匹配时不区分大小写。                        |
| M	     | 多行匹配模式。                              |
| S   	 | 使‘.’可以匹配所有空白字符，包括换行。     |

**分组选择：用圆括号将所有选择项括起来，相邻的选择项之间用|分隔。**

| 分组        |                   描述                      |
| :---------: | :------------------------------------------ |
| (?P<name>)  | 分组，除了原有的分组再额外指定一个别名。    |
| (?P=name)   | 引用别名为<name>分组匹配到的字符串。        |
| (?<number>) | 引用别名为<number>分组匹配到的字符串。      |
| (?:...)	  | 不捕获分组，后面可用‘竖线’或数量词。      |
| (?#...)	  | #之后的内容将被忽略。                       |
| (?=...)     | 之后的内容需要匹配表达式才能匹配。          |
| (?!...)     | 之后的内容不匹配表达式才能成功。            |
| (?<=...)    | 之前的内容需要匹配表达式才能匹配。          |
| (?<!=...)   | 之前的内容不匹配表达式才能成功。            |
| (?(id/name)Y竖线N)| 编号为id或别名为name的组匹配到字符串，则匹配Y的表达式，否则匹配N的表达式，N可忽略。 |

> tip：markdown语法问题，上面竖线表示‘|’字符。

表达式前缀，在原始字符串表达式的前面有时会加上前缀，代表其特殊的额意义。

| 前缀 |                   描述                      |
| :--: | :------------------------------------------ |
| r	   | r后的表达式字符串，为普通字符，不做转义     |
| u	   | u后的表达式字符串，为unicode编码字符        |

[参阅链接图示同模块说明。](http://www.cnblogs.com/smallmars/p/6935269.html)

## 2、re模块介绍

**python通过re模块提供对正则表达式的支持。使用re的一般步骤是先将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果（一个Match实例），最后使用Match实例获得信息，进行其他的操作。**

### 2.1 Pattren对象

Pattern对象是一个编译好的正则表达式，通过Pattern的一系列方法可以对文本进行匹配查找。它不能直接实例化，必须**通过re.compile()进行构造得到。**

这个对象**提供了几个可读属性用于获取表达式**的相关信息，当然它还有其它方法供匹配字符串用。

- pattren：编译时用的表达式字符串。
- flags：编译时用的匹配模式，即之前的修饰符。
- groups：编译时表达式中分组的数量。
- groupindex：编译时表达式中有别名的组的别名为键、以该组对应的编号为值的字典，没有别名的组不包含在内。

演示代码：

	import re
	p = re.compile(r'(\d)(\w)(?P<sign>.*)', re.S)
	print('p.pattern :  %s' % p.pattern)
	print('p.flags :  %s' % p.flags)
	print('p.groups :  %s' % p.groups)
	print('p.groupindex : %s' % p.groupindex)

其运行结果如下：

	p.pattern :  (\d)(\w)(?P<sign>.*)
	p.flags :  48
	p.groups :  3
	p.groupindex : {'sign': 3}

### 2.2 Match对象

Match对象是一次匹配的结果，即引用re的相关方法后生成的结果即Match对象的实例。其包含了很多关于此次匹配的信息，可以下面的属性或方法获取相关信息。

属性：

- string：匹配时使用的文本。
- re：匹配时使用的Pattern对象。
- pos：文本中正则表达式开始搜索的索引。
- endpos：文本中表达式结束搜索的位置。
- lastindex：最后一个被捕获的分组在文本中的索引。如果没有被捕获的分组，将为None。
- lastgroup：最后一个被捕获的分组的别名。如果这个分组没有别名或者没有被捕获的分组，将为None。

方法:

- group([group1, …]): 获得一个或多个分组截获的字符串；指定一个直接字符串返回，指定多个参数时将以元组形式返回。group1可以使用编号也可以使用别名；编号0代表整个匹配的子串；不填写参数时，返回group(0)；没有截获字符串的组返回None；截获了多次的组返回最后一次截获的子串。
- groups([default]):以元组形式返回全部分组截获的字符串。相当于调用group(1,2,…last)。default表示没有截获字符串的组以这个值替代，默认为None。 
- groupdict([default]): 返回以有别名的组的别名为键、以该组截获的子串为值的字典，没有别名的组不包含在内。default含义同上。 
- start([group]):返回指定的组截获的子串在string中的起始索引（子串第一个字符的索引）。group默认值为0。 
- end([group]): 返回指定的组截获的子串在string中的结束索引（子串最后一个字符的索引+1）。group默认值为0。 
- span([group]): 返回(start(group), end(group))。 
- expand(template):将匹配到的分组代入template中然后返回。template中可以使用\id或\g<id>、\g<name>引用分组，但不能使用编号0。\id与\g<id>是等价的；但\10将被认为是第10个分组，如果你想表达\1之后是字符'0'，只能使用\g<1>0。

测试代码：

	m = re.match(r'(\w+)\s(\w+)(?P<sign>.*)', 'hello python!')
	
	print('m.string : %s' % m.string)
	print('m.re : %s' % m.re)
	print('m.pos : %s' % m.pos)
	print('m.endpos : %s' % m.endpos)
	print('m.lastindex : %s' % m.lastindex)
	print('m.lastgroup : %s' % m.lastgroup)
	
	print('m.group(1, 2) : ', m.group(1, 2))
	print('m.groups() :  ', m.groups())
	print('m.groupdict() :  ', m.groupdict())
	print('m.start(2) :  ', m.start(2))
	print('m.end(2) :  ', m.end(2))
	print('m.span(2) :  ', m.span(2))
	print(r"m.expand(r'\2 \1 \3') : ", m.expand(r'\2 \1 \3'))

运行结果：

	m.string : hello python!
	m.re : re.compile('(\\w+)\\s(\\w+)(?P<sign>.*)')
	m.pos : 0
	m.endpos : 13
	m.lastindex : 3
	m.lastgroup : sign

	m.group(1, 2) :  ('hello', 'python')
	m.groups() :   ('hello', 'python', '!')
	m.groupdict() :   {'sign': '!'}
	m.start(2) :   6
	m.end(2) :   12
	m.span(2) :   (6, 12)
	m.expand(r'\2 \1 \3') :  python hello !

## 2.3 re模块方法（Pattern实例方法）

re提供了众多方法用于完成正则表达式的功能。这些方法可以使用Pattern实例的相应方法替代，唯一的好处是少写一行re.compile()代码，但同时也无法复用编译后的Pattern对象。

看几行re.py的源码，当我们调用match方法时：

	def match(pattern, string, flags=0):
	    """Try to apply the pattern at the start of the string, returning
	    a match object, or None if no match was found."""
	    return _compile(pattern, flags).match(string)

它是先将原始字符串编译成pattern对象，然后再利用其方法进行匹配字符串。

所以re模块的使用（即其方法的使用）要和Pattern实例方法一起介绍。

### 2.3.1 compile

**re.compile(strPattern[, flag])**: Pattern类的构造方法，用于将字符串形式的正则表达式编译成Pattern对象，第二个参数flag是匹配模式，取值时可以使用按位或运算符‘|’表示同时生效，即‘re.I|re.M’；或者直接在字符串中执行模式，re.compile('(?im)pattern')等同re.compile('pattern', re.I|re.M)。

- re.I(re.IGNORECASE): 忽略大小写。
- re.M(re.MULTILINE): 多行模式，改变'^'和'$'的行为。
- re.L(re.LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定。
- re.U(re.UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性 。
- re.X(re.VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释。以下两个正则表达式是等价的：

演示代码：

	import re
	p = re.compile(r'(\d)(\w)(?P<sign>.*)', re.S)
	print('p.pattern :  %s' % p.pattern)
	print('p.flags :  %s' % p.flags)
	print('p.groups :  %s' % p.groups)
	print('p.groupindex : %s' % p.groupindex)

其运行结果如下：

	p.pattern :  (\d)(\w)(?P<sign>.*)
	p.flags :  48
	p.groups :  3
	p.groupindex : {'sign': 3}

### 2.3.2 match

**re.match(pattern, string[, flags]) | pattern.match(string[, pos[, endpos]])**：从string的pos下标处尝试匹配pattern，如果pattern介绍仍可匹配，则返回一个Match对象，如果匹配不成功或匹配没结束就到达endpos，则返回None。

- pos和endpos的默认值为0和len(string)；
- re.match()无法直接指定两个参数，参数flags用于编译pattern时指定匹配模式。

测试代码：

	m = re.match(r'(\w+)\s(\w+)(?P<sign>.*)', 'hello python!')
	
	print('m.string : %s' % m.string)
	print('m.re : %s' % m.re)
	print('m.pos : %s' % m.pos)
	print('m.endpos : %s' % m.endpos)
	print('m.lastindex : %s' % m.lastindex)
	print('m.lastgroup : %s' % m.lastgroup)
	
	print('m.group(1, 2) : ', m.group(1, 2))
	print('m.groups() :  ', m.groups())
	print('m.groupdict() :  ', m.groupdict())
	print('m.start(2) :  ', m.start(2))
	print('m.end(2) :  ', m.end(2))
	print('m.span(2) :  ', m.span(2))
	print(r"m.expand(r'\2 \1 \3') : ", m.expand(r'\2 \1 \3'))

运行结果：

	m.string : hello python!
	m.re : re.compile('(\\w+)\\s(\\w+)(?P<sign>.*)')
	m.pos : 0
	m.endpos : 13
	m.lastindex : 3
	m.lastgroup : sign

	m.group(1, 2) :  ('hello', 'python')
	m.groups() :   ('hello', 'python', '!')
	m.groupdict() :   {'sign': '!'}
	m.start(2) :   6
	m.end(2) :   12
	m.span(2) :   (6, 12)
	m.expand(r'\2 \1 \3') :  python hello !

### 2.3.3 search

**re.search(pattern, string[, flags]) | pattern.search(string[, pos[, endpos]])**：用于查找字符串中可以匹配成功的子串。从string的pos下标处起尝试匹配pattern，若匹配结束仍可匹配，则返回一个Match对象，若无法匹配则pos+1再次匹配，直到pos=endpos时仍无法匹配返回None。

测试代码：

	pattern = re.compile(r'py\w{2,}?', re.I)
	match = pattern.search('hello python', 2, 11)
	print(match)
	if match :
	    print(match.group())

运行结果：

	<_sre.SRE_Match object; span=(6, 10), match='pyth'>
	pyth

### 2.3.4 split

**re.split(pattern, string[, maxsplit]) | pattern.split(string[, maxsplit])**：按照能够匹配的子串将string分割后返回列表，如果不能匹配，则会将整串字符串以唯一元素的列表形式返回。maxsplit用于指定最大的分割次数。

测试代码：

	pattern = re.compile(r'\d+', re.I)
	match = pattern.split('abc1efg2ijk3mno4rst', 3)
	print(match)
	
	pattern = re.compile(r'\d{2}', re.I)
	match = pattern.split('abc1efg2ijk3mno4rst', 3)
	print(match)

运行结果：

	['abc', 'efg', 'ijk', 'mno4rst']
	['abc1efg2ijk3mno4rst']

### 2.3.5 findall

**re.findall(pattern, string[, flags]) | pattern.findall(string[, pos[, endpos]])**：搜索string，以列表形式返回全部匹配的子串。搜索不到返回空的列表。

测试代码：

	pattern = re.compile(r'\d+', re.I)
	match = pattern.findall('abc1efg2ijk3mno4rst', 3, 10)
	print(match)
	
	pattern = re.compile(r'\d+', re.I)
	match = pattern.findall('abc1efg2ijk3mno4rst', 18)
	print(match)

运行结果：

	['1', '2']
	[]

### 2.3.6 finditer

**re.finditer(pattern, string[, flags]) | pattern.finditer(string[, pos[, endpos]])**：搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。

测试代码：

	pattern = re.compile(r'\d+', re.I)
	match = pattern.finditer('abc1efg2ijk3mno4rst', 3, 15)
	for item in match :
	    print(item.group())

运行结果：

	<_sre.SRE_Match object; span=(3, 4), match='1'>
	1
	<_sre.SRE_Match object; span=(7, 8), match='2'>
	2
	<_sre.SRE_Match object; span=(11, 12), match='3'>
	3

### 2.3.7 sub

re.sub(pattern, repl, string[, count]) | pattern.sub(repl, string[, count])：使用repl替换string中每一个匹配的子串后，返回替换后的字符串。

- 当repl是一个字符串时，可以使用\id、\g<id>或\g<name>引用分组，但不能使用编号0.
- 当repl是一个方法时，这个方法应当只接收一个参数（Match对象），并返回一个用于替换的字符串。
- count用于指定替换次数，不指定时替换全部。

测试代码：

	pattern = re.compile(r'(\w+)\s(\w+)', re.I)
	string = 'Daocoder say : hello Python'
	print(pattern.sub(r'\2 \1', string, 2))
	
	def upper_first_letter(match) :
	    return match.group(1).title() + ' ' + match.group(2).title()
	
	print(pattern.sub(upper_first_letter, string, 2))

运行代码：

	say Daocoder : Python hello
	Daocoder Say : Hello Python

### 2.3.8 subn

re.subn(pattern, repl, string[, count]) | pattern.subn(repl, string[, count])：返回结果为(re.sub(pattern, repl, string[, count]), 替换次数)，即元组展示的上方法结果和替换次数。

测试代码：

	pattern = re.compile(r'(\w+)\s(\w+)', re.I)
	string = 'Daocoder say : hello Python'
	print(pattern.subn(r'\2 \1', string, 2))
	
	def upper_first_letter(match) :
	    return match.group(1).title() + ' ' + match.group(2).title()
	
	print(pattern.subn(upper_first_letter, string, 2))

运行结果：

	('say Daocoder : Python hello', 2)
	('Daocoder Say : Hello Python', 2)


 









