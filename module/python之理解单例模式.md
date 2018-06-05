<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解单例模式

# 1、单例模式

**单例模式（Singleton Pattern）是一种常见的软件设计模式，该模式的主要目的是确保一个类只能有一个实例存在。**当你希望在整个系统中，某个类只有一个实例对象出现时，这种模式就派上用场了。通过单例模式可以保证系统的一个类只有一个实例且该实例易于被外界访问，从而方便对实例个数的控制去节约系统资源。

# 2、python实现单例、

## 2.1 使用__new__方法

	class Singleton(object):
	    _instance = None
	
	    def __new__(cls, *args, **kwargs):
	        if cls._instance:
	            return cls._instance
	        else:
	            cls._instance = super(Singleton, cls).__new__(cls)
	            return cls._instance
	
	
	singleton1 = Singleton()
	singleton2 = Singleton()
	
	print(singleton1)
	print(singleton2)

结果：

	<__main__.Singleton object at 0x0000000001F59D30>
	<__main__.Singleton object at 0x0000000001F59D30>

## 2.2 使用metaclass

	class Singleton(type):
	    _instances = {}
	
	    def __call__(cls, *args, **kwargs):
	        if cls in cls._instances:
	            return cls._instances[cls]
	        else:
	            cls._instances[cls] = super(Singleton, cls).__call__(*args, *kwargs)
	            return cls._instances[cls]
	
	
	class SingletonTest(metaclass=Singleton):
	    pass
	
	
	singleton1 = SingletonTest()
	singleton2 = SingletonTest()
	
	print(singleton1)
	print(singleton2)

结果：

	<__main__.SingletonTest object at 0x00000000024DFC18>
	<__main__.SingletonTest object at 0x00000000024DFC18>

这里对理解`__init__`和`__call__`的使用很有帮助，敲黑板，划重点。

## 2.3 共享属性（疑惑）

	class Singleton(object):
	    _state = {}
	
	    def __new__(cls, *args, **kwargs):
	        ob = super(Singleton, cls).__new__(cls, *args, **kwargs)
	        ob.__dict__ = cls._state
	        return ob
	
	
	class SingletonTest(Singleton):
	    name = 'daocoder'
	    pass
	
	
	singleton1 = SingletonTest()
	singleton2 = SingletonTest()
	
	print(singleton1)
	print(singleton2)

这里来自github的一处，即下面的参阅地址，感觉有点问题。

## 2.4 装饰器

	def singleton(cls, *args, **kwargs):
	    _instance = {}
	
	    def get_instance():
	        if cls not in _instance:
	            _instance[cls] = object.__new__(cls, *args, **kwargs)
	        return _instance[cls]
	    return get_instance
	
	
	@singleton
	class SingletonTest(object):
	    name = 'daocoder'
	    pass
	
	
	singleton1 = SingletonTest()
	singleton2 = SingletonTest()
	
	print(singleton1)
	print(singleton2)

装饰器在之后会再次讨论学习下，@singleton指调用singleton方法，参数为SingletonTest，利用singleton内返回的方法get_instance，SingletonTest为参数，返回结果。

## 2.5 import 自然萌

**python的模块就是天然的单例模式。**因为模块第一次导入时，会生成`.pyc`的文件，当第二次导入时，会直接加载这个文件，而不会再次加载代码。因此，我们只需要把相关的代码和数据定义在一个模块中，就可以获取一个单例对象了。

	# singleton.py
	class SingletonTest(object):
	    def foo(self):
	        pass
	
	my_singleton = SingletonTest()

将上面代码放在`singleton.py`中，其它文件这么引入：

	from singleton import my_singleton
	 
	my_singleton.foo()

# 3、感谢

[Python 中的单例模式](http://python.jobbole.com/87294/)

[单例模式](https://github.com/taizilongxu/interview_python?hmsr=pycourses.com&utm_source=pycourses.com&utm_medium=pycourses.com#16-%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F)







