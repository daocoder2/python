<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解`__new__`、`__init__`和`__call__`

# 1、从type看其解释

所有的对象都可以看作由type出发，那么就先type关于这几个函数的解释。

	class type(object):
	
	    def __call__(self, *args, **kwargs):  # real signature unknown
	        """ Call self as a function. """
	        pass
	
	    def __init__(cls, what, bases=None, dict=None):  # known special case of type.__init__
	        """
	        type(object_or_name, bases, dict)
	        type(object) -> the object's type
	        type(name, bases, dict) -> a new type
	        # (copied from class doc)
	        """
	        pass
	
	    @staticmethod # known case of __new__
	    def __new__(*args, **kwargs):  # real signature unknown
	        """ Create and return a new object.  See help(type) for accurate signature. """
	        pass

1、`__call__`：Call self as a function，即当实例对象被当作函数调用时，会自动触发这个函数。
2、`__new__`：Create and return a new object，静态方法，创建并返回一个对象。
3、`__init__`：实例化对象时，自动调用。

# 2、实践说明

借用下面的例子说明：

	class A(object):
	    _dict = {}
	
	    def __new__(cls, *args, **kwargs):
	        if 'keys' in cls._dict:
	            print('old')
	            return cls._dict['keys']
	        else:
	            print('new object')
	            return super(A, cls).__new__(cls)
	
	    def __init__(self):
	        print('init object')
	        self._dict['keys'] = self
	        print('')
	
	    def __call__(self, *args, **kwargs):
	        print(args)
	        print(kwargs)
	
	
	a1 = A()
	a2 = A()
	a3 = A()
	a3(('daocoder', 'python'), name='daocoder', hobby='python')

结果：

	new object
	init object
	
	old
	init object
	
	old
	init object
	
	(('daocoder', 'python'),)
	{'name': 'daocoder', 'hobby': 'python'}

用到`__new__`的情况是当你想去控制去创建一个实例，`__init__`的情况是你想去在实例对象后初始化执行一个方法。在应用单例的时候可能会用到这些，单例在之后会看看。

`__call__`，如上面所示，当实例对象被当作函数调用时，触发这个方法。

## 2.1 args与kwargs

顺带记录下这两个东西，用`args`和`kwargs`只是为了方便，并没有强制使用它们。

当你不确定你的函数要传多少参数时，你可以**使用args。它可以接收任意多的参数，接收到的参数将会以元组的形式展示。kwargs允许你使用没有事先定义的参数名，它将以字典的形式展示。**

注意点：

- `*args`和`**kargs`可以同时出现在函数定义中，但`*args`必须在`**kwargs`之前。
- 调用时，可以使用`*`和`**`的语法。他们后面是列表或元组和字典。

# 3、感谢

[Why is __init__() always called after __new__()?](https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new#)







