<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解super

	super(type[, object-or-type])

- type 类。
- object-or-type 类，一般是 self。

# 1、super

在类的继承中，如果重定义某个方法，该方法会覆盖父类的同名方法，但有时，我们希望能同时实现父类的功能，这时，我们就需要调用父类的方法了，可通过super()来实现，比如：

	class Animal(object):
	    def __init__(self, name):
	        self.name = name
	
	    def greet(self):
	        print('the animal name is %s' % self.name)
	
	
	class Dog(Animal):
	    def greet(self):
	        super(Dog, self).greet()
	        print('wangwang')
	
	
	dog = Dog('huang')
	dog.greet()

结果：

	the animal name is huang
	wangwang

上面Animal是父类，Dog是子类，我们现在Dog类重定义了greet方法，为了能同时实现父类的功能，有利用super调用了父类的greet方法。

super一个常见的用法就是在子类中调用父类的初始化方法了，如：

	class Base(object):
	    def __init__(self, a, b):
	        self.a = a
	        self.b = b
	
	
	class Inherit(Base):
	    def __init__(self, a, b, c):
	        # super(Inherit, self).__init__(a, b)
	        super().__init__(a, b) # py3支持的写法
	        self.c = c
	        print(self.a)
	        print(self.b)
	        print(self.c)
	
	
	test = Inherit('daocoder', 'mudai', 'dao')

结果：

	daocoder
	mudai
	dao

# 2、深入理解super

上面基本是一般的用法和理解：获取父类，然后调用父类的方法。其实在上面的例子中，super获取的类恰好是父类而已，但在其它情况下就不一样了，**super实质上和父类没有关联**。

	class Base(object):
	    def __init__(self):
	        print('enter base')
	        print('leave base')
	
	
	class A(Base):
	    def __init__(self):
	        print('enter A')
	        super(A, self).__init__()
	        print('leave A')
	
	
	class B(Base):
	    def __init__(self):
	        print('enter B')
	        super(B, self).__init__()
	        print('leave B')
	
	
	class C(A, B):
	    def __init__(self):


	c = C()

结果为：

	enter C
	enter A
	enter B
	enter base
	leave base
	leave B
	leave A
	leave C

Base是父类，A，B继承自Base，C继承自A，B。

如果按照之前的super代表是“调用父类的方法”，那么很可能会疑惑enter A的下一句不是enter Base而是enter B。（**新式类是广度优先,旧式类是深度优先**)。原因是**super和父类没有实质性的关联。**下面说明super是怎么运作的。

# 3、MRO列表

MRO（method resolution order），事实上，对于你定义的每个类，python都会计算出一个方法解析顺序，它代表了类继承的顺序。我们可以利用下面的方式获得某个类的MRO列表。

同样上面的代码。

	print(C.mro())
	print(C.__mro__)
	print(c.__class__.mro())

结果为：

	[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>]
	(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)
	[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>]

那么这个MRO列表的顺序是怎么定的呢，它是通过一个[C3线性化算法](https://www.python.org/download/releases/2.3/mro/)来实现的，这里不讨论这个算法，简单来说，一个MRO列表就是合并所有父类的列表，并遵循下面几点：

- 子类永远在父类的前面。
- 如果有多个父类，会根据它们在列表中的顺序去检查。
- 如果对下一个类存在两种不同的合法选择，那么选择第一个父类。

# 4、super原理

super的工作原理如下：

	def super(cls, inst):
		mro = inst.__class__.mro()
		return mro[mro.index(cls) + 1]

cls代表类，inst代表实例，可以看出上面的代码做了两件事：

- 获取inst的MRO列表。
- 查找cls在MRO的index，并返回它的下一个类，即mro[index + 1]

当你使用super(cls, inst)时，python会在inst的MRO列表上搜索下cls的下一个类。

现在再回答前面的例子：

	super(C, self).__init__()

这里的self是C的实例，self.__class__.mro()的结果是；

	[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>]

可以看到C的下一个类是A，于是，跳到了A的__init__，这时会打印enter A，并且执行下面一行代码：

	super(A, self).__init__()

注意这里的**self也是当前C的实例，MRO列表和之前是一样的**。搜索A在MRO中下的一个类，发现是B，于是又跳到了B的__init__，这时会打印enter B，而不是enter Base。

上面整个过程还是比较清晰的，关键在于理解super的工作方式，而不是想当然的理解为super调用父类的方法。

总结：

- super和父类没有实质性的关联。
- **super(cls, inst)获得的是cls在inst的MRO列表中下一个类**。

[原文出处](http://python.jobbole.com/86787/)

