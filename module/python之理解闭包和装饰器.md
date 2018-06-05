<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解闭包和装饰器

# 1、闭包函数

## 1.1 python中函数都是对象

	def shut(word='yes'):
	    print(word.capitalize())
	
	
	shut()
	scream = shut
	scream()
	print(type(shut))
	print(id(shut))
	print(id(scream))
	
	del shut
	scream()
	print(id(scream))

结果：

	Yes
	Yes
	<class 'function'>
	33454008
	33454008
	Yes
	33454008

上面定义一个shut函数，由type获取其类型可知是class，那它当然是一个对象了（具体可参考[理解元类](https://www.jianshu.com/p/698eb999e271)）。

**对象的话，我们就知道可以赋值给另外一个变量，可以在其它函数中定义，且函数可以返回另一个函数。**

`shut()`这里是函数调用，`scream = shut`函数引用，`scream()`调用，然后下面打印它们的内存地址是一样的，再下面删除`del shut`变量，调用`scream()`,内存地址不变，这里可以想到另外一个东西：**python的垃圾回收机制**，其它理解系列会学习下。

## 1.2 函数引用与闭包

这个唠叨要一段时间，详细了解引用js的介绍[javascript之理解闭包](https://www.jianshu.com/p/d7db1d1aa663)。

简单来说，闭包是满足下面几个东西的函数：

- 嵌套函数，即一个函数内部定义另外一个函数，外层函数称为A，内层函数称为B。
- 在嵌套函数中的内层函数B在外层函数A中所在的全局作用域范围被调用。
- 这时调用B函数的作用域有两个：A所在的全局作用域和B所在A中的局部作用域。

再简单来说就是：闭包就是能够读取其它函数内部变量的函数。这里可以理解B是闭包函数，然后A是其它函数。

一个简单例子：

	def talk(name='shut'):
	    who = 'daocoder'
	
	    def shut(word='yes'):
	        print('shut %s to %s' % (word.upper(), who))
	
	    def whisper(word='yes'):
	        print('whisper %s to %s' % (word.lower(), who))
	
	    if name == 'shut':
	        return shut
	    elif name == 'whisper':
	        return whisper
	    else:
	        return shut
	
	
	print(talk())
	talk()(word='mudai')
	talk('whisper')(word='mudai')

结果：

	<function talk.<locals>.shut at 0x0000000001F27840>
	shut MUDAI to daocoder
	whisper mudai to daocoder

**在`talk`函数内部再定义`shut`和`whisper`函数，并且两个函数用到了外边函数的变量`who`和`name`，那么这两个函数以及用到的一些变量称之为闭包。**

## 1.3 闭包啥作用呢

	def line_conf(a, b):
	    def line(x):
	        return a * x + b
	    return line
	
	
	line1 = line_conf(2, 5)
	line2 = line_conf(1, 3)

	print(line1(2))
	print(line2(2))

结果：

	9
	5

上面的例子中，函数`line`和变量`a`、`b`就构成了闭包。在创建闭包的时候，我们通过line_conf(a, b)说明了变量的取值，那么这样就确定了最终闭包函数（y=2x+5和y=x+3）。且我们只需要变换不同的参数就可以获取不同的直线函数表达式。这里体现代码的复用性。另外可以因此隐藏内部实现细节。

**注意：由于闭包引用了外部函数的局部变量，那么外部函数的局部变量就一直会存在于内存中，内存泄漏是一个隐患。**

# 2、装饰器

提到装饰器，应该提及另一个东西**AOP（Aspect Origented Programming）面向切换编程**。它的作用很强大，联想实际业务的场景，我们想用户在开始访问时记录一个日志，即整个框架跑起来初始化的时候，解析请求路由之前做这些事情。另外可用的场景有插入日志、性能测试、事务处理（登录）等。

装饰器即基于AOP思想的一个实现，也利用到了上节说的闭包。有了装饰器，我们就可以抽离出大量与函数本身无关的代码并重复加以利用，概况的说：**装饰器就是为已存在的对象添加额外的功能。**

## 2.1 python里的装饰器

	def makebold(fn):
	    def wrapped():
	        return '<b>' + fn() + '</b>'
	    return wrapped
	
	
	def makeitalic(fn):
	    def wrapped():
	        return '<i>' + fn() + '</i>'
	    return wrapped
	
	
	@makebold
	@makeitalic
	def say():
	    return "Hello"
	
	
	print(say())

结果：

	<b><i>Hello</i></b>

效果就如上，那继续讨论轮子是怎么造的。

## 2.2 手动实现装饰器

	def my_decorator(fn):
	    def wrapped(*args, **kwargs):
	        new_name = kwargs['name'].replace('daocoder', 'mudai')
	        new_age = args[0] + 1
	        return fn(new_age, name=new_name)
	    return wrapped
	
	
	def say_name(*args, **kwargs):
	    return "my name is %s and %d years old" % (kwargs['name'], args[0])
	
	
	print(say_name(26, name='daocoder'))
	print(my_decorator(say_name)(26, name='daocoder'))

结果：

	print(say_name(26, name='daocoder'))
	print(my_decorator(say_name)(26, name='daocoder'))

看着有些别扭、大体想法希望能表达出来。以上的调用过程如下：

1、say_name作为参数传递给my_decorator后，say_name指向my_decorator返回的wrapped；
2、然后wrapped作为一个新的函数去调用。
3、内部函数wrapped被引用，外部函数的变量fn（即say_name）并没有被释放，它保存的还是原来最初的定义。

## 2.3 python语法糖@的用法

稍微修改上面的轮子：

	def my_decorator(fn):
	    def wrapped(*args, **kwargs):
	        new_name = kwargs['name'].replace('daocoder', 'mudai')
	        new_age = args[0] + 1
	        return fn(new_age, name=new_name)
	    return wrapped
	
	
	@my_decorator
	def say_name(*args, **kwargs):
	    return "my name is %s and %d years old" % (kwargs['name'], args[0])
	
	
	print(say_name(26, name='daocoder'))

结果：

	my name is mudai and 27 years old

那说明这个`my_decorator(say_name)`和`@my_decorator`这两个的作用就是一样的。一个语法糖包装吧。

	@my_decorator == my_decorator(say_name)

## 2.4 类装饰器

上面的介绍可以看出，装饰器需要callable对象作为参数，然后返回一个callback对象。一般在python中callable对象都是函数，但也有例外，只有某个类中写了`__call__`方法，那么对象就是callable的。

	class MyDecorator(object):
	    def __init__(self, func):
	        self.func = func
	        pass
	
	    def __call__(self, *args, **kwargs):
	        # print(args)
	        # print(kwargs)
	        # print(self.func)
	        new_name = kwargs['name'].replace('daocoder', 'mudai')
	        new_age = args[0] + 1
	        return self.func(new_age, name=new_name)
	
	
	@MyDecorator
	def say_name(*args, **kwargs):
	    return "my name is %s and %d years old" % (kwargs['name'], args[0])
	
	
	print(say_name(26, name='daocoder'))

结果：

	my name is mudai and 27 years old

以上大体调用过程如下：

1、`MyDecorator`作为装饰器对`say_name`进行装饰的时候，这时先去创建`MyDecorator`这个实例对象。
2、创建对象初始化时，会把`say_name`这个函数名当作参数传递到`__init__`方法中，这里保存`say_name`作为对象的`func`属性。
3、这时`say_name`指向的是`MyDecorator`的实例对象，然后调用`say_name()`，即调用`MyDecorator的实例对象的`__call__`方法。

这里和之前函数作为装饰器的区别就是第3步：**函数作为装饰器时，say_name的指向应该是返回的wrapped方法，而这里say_name的指向是MyDecorator的实例对象。**

# 3、感谢

[Python中如何在一个函数中加入多个装饰器](https://taizilongxu.gitbooks.io/stackoverflow-about-python/content/3/README.html)

某平台培训资料。







