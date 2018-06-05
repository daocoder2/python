<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解元类

# 1、类也是对象

在大多数编程语言中，**类就是一组用来描述如何生成对象的代码段**。在python中，这一点仍然成立。

	class BaseObject(object):
	    pass
	
	
	demo_object = BaseObject()
	print(demo_object)
	print(BaseObject)

结果：

	<__main__.BaseObject object at 0x0000000001DC8780>
	<class '__main__.BaseObject'>

demo_object显而易见的是一个实例对象，那类BaseObject也是一个对象？对的，是一个对象，只要你使用关键字class，python解释器在执行的时候就会创建这个一个对象，如上：`<class '__main__.BaseObject'>`。

解释器将在内存中创建一个对象，名字就叫做BaseObject。这个对象（类对象BaseObject）拥有创建对象（实例对象）能力。但是，它的本质仍旧是一个对象，针对对象类型，我们通常有下面的一些操作：

- 将对象复制给一个变量
- 拷贝对象
- 为对象增加属性
- 将对象作为函数参数传递

---

	class BaseObject(object):
	    pass
	
	
	def echo(o):
	    print(o)
	
	
	echo(BaseObject)
	print(hasattr(BaseObject, 'new_attr'))
	BaseObject.new_attr = 'daocoder'
	print(hasattr(BaseObject, 'new_attr'))
	print(BaseObject.new_attr)
	a = BaseObject
	print(a)

结果：

	<class '__main__.BaseObject'>
	False
	True
	daocoder
	<class '__main__.BaseObject'>

# 2、动态的创建类

因为类也是对象，那么你可以在运行的时候动态创建他们，就像一般实例化对象一样。那么，你可以在函数中创建类，使用class关键字即可。

	def create_object(name):
	    if name == 'Foo':
	        class Foo(object):
	            pass
	        return Foo
	    elif name == 'Bar':
	        class Bar(object):
	            pass
	        return Bar
	
	
	MyClass = create_object('Foo')
	print(MyClass)
	print(MyClass())

结果：

	<class '__main__.create_object.<locals>.Foo'>
	<__main__.create_object.<locals>.Foo object at 0x0000000002B745F8>

由运行结果可以看出确实可以实现这样的需求，但是这样还是需要自己编写整个代码，不够动态，那么我们可以想到对于一门语言，肯定可以自动创建对象，既然类也是一个对象，那么它肯定也是通过什么创建出来的。

**当我们利用class关键字时，python解释器会自动操作这个类对象**，那么和python实现的大多数事情一样，python也提供了手动创建的方法。

回归到我们学习python函数的基础，有一个内建函数用来获取各个变量的类型type()，就像下面这样。

	print(type(1))
	print(type('1'))
	print(type(True))
	print(type(range(1)))
	print(type([]))
	print(type({}))
	print(type(()))
	print(type(MyClass))

结果：

	<class 'int'>
	<class 'str'>
	<class 'bool'>
	<class 'range'>
	<class 'list'>
	<class 'dict'>
	<class 'tuple'>
	<class 'type'>

注意看最后一个，MyClass的类型竟然是type。那么这个type到底是啥东西。

# 3、利用type创建类

type还有一个完全不同的功能，就是动态创建类。

type可以接受一个类的描述符作为参数，然后返回一个类。（通常根据传入参数的不同，同一个函数可以拥有两种完全不同的用法，是很忌讳的事情，但python这里是为了保持向后兼容性）。

所以，type可以像下面这样工作：

	type(类名, 由父类名称组成的元组（继承情况，可为空）， 包含字典的属性（名称和值）)

如下面的代码：

	class Test(object):
	    pass
	
	
	print(Test)
	
	Dog = type('Dog', (), {})
	print(Dog)

结果：

	<class '__main__.Test'>
	<class '__main__.Dog'>

再看帮助：

	help(Test)
	help(Dog)

结果：


	Help on class Test in module __main__:
	
	class Test(builtins.object)
	 |  Data descriptors defined here:
	 |  
	 |  __dict__
	 |      dictionary for instance variables (if defined)
	 |  
	 |  __weakref__
	 |      list of weak references to the object (if defined)
	
	Help on class Dog in module __main__:
	
	class Dog(builtins.object)
	 |  Data descriptors defined here:
	 |  
	 |  __dict__
	 |      dictionary for instance variables (if defined)
	 |  
	 |  __weakref__
	 |      list of weak references to the object (if defined)


一样的。

# 4、利用type创建带有属性、方法的类

**1、创建带属性的类**

	Animal = type('Animal', (), {'name': 'daocoder'})
	animal = Animal()
	print(animal.name)

结果：

	daocoder

**2、创建带属性、方法且继承的类**

	Animal = type('Animal', (), {'name': 'daocoder'})
	animal = Animal()
	print(animal.name)
	
	
	def talk(obj, age):
	    print('my name is %s and %s years old' % (obj.name, age))
	
	
	Dog = type('Dog', (Animal,), {'name': 'huang', 'talk': talk})
	dog = Dog()
	# dog.name = 'da huang'
	dog.talk(10)

结果：

	daocoder
	my name is huang and 10 years old

这里注意：

- type的第2个参数，元组中是父类的名字，不是字符串。
- 添加的属性是类属性，不是实例属性。

**3、添加静态方法和类方法**

	Animal = type('Animal', (), {'name': 'daocoder'})
	animal = Animal()
	print(animal.name)
	
	
	def talk(obj, age):
	    print('my name is %s and %s years old' % (obj.name, age))
	
	
	@staticmethod
	def eat(food):
	    print('i can eat %s' % food)
	
	
	@classmethod
	def sleep(self, dt):
	    print('%s can sleep %s hours' % (self.name, dt))
	
	
	Dog = type('Dog', (Animal,), {'name': 'huang', 'talk': talk, 'eat': eat, 'sleep': sleep})
	dog = Dog()
	# dog.name = 'da huang'
	dog.talk(10)
	dog.eat('meat')
	dog.sleep(8)

结果：

	daocoder
	my name is huang and 10 years old
	i can eat meat
	huang can sleep 8 hours

# 5、什么是元类

**元类就是用来创建类（对象）的，可以理解为元类就是创建类的类。**

	MyClass = type('MetaClass', (), {})
	# class MyClass(object):
	#     pass
	
	
	MyObject = MyClass()
	
	print(MyClass)
	print(MyObject)

结果：

	<class '__main__.MetaClass'>
	<__main__.MetaClass object at 0x00000000023E9D30>

上面利用type创建了一个MyClass类（对象），然后基于它实例化一个对象MyObject。注释的基本形式结果一致。

这里实际上type函数就是一个元类。**type就是在python解释器用来创建所有类的元类。**我们可以这么理解，类比str是创建字符串对象的类（对象），int是创建整数对象的类（对象），那么type就是创建对象的类（对象）。**python中，所有的东西都是对象，包括整数、字符串、函数及类。它们全是对象，且从一个类中创建而来，这个类就是type。**

	print(type(1))
	print(type('1'))
	print(type(True))
	
	print(type(int.__class__))
	print(type(str.__class__))
	print(type(bool.__class__))
	print(type(object.__class__))

	print(type(int.__class__.__class__))
	print(type(str.__class__.__class__))
	print(type(bool.__class__.__class__))
	print(type(object.__class__.__class__))

结果：

	<class 'int'>
	<class 'str'>
	<class 'bool'>

	<class 'type'>
	<class 'type'>
	<class 'type'>
	<class 'type'>

	<class 'type'>
	<class 'type'>
	<class 'type'>
	<class 'type'>

**从上面可以看出元类就是创建类这种对象的东西，type是python内建的元类，那么我们当然可以创建自己的元类啊。**

# 6、__metaclass__属性

我们可以定义一个类的时候为其添加一个__metaclass__属性。

	class Bar(type):
	    pass
	
	
	class Foo(object, metaclass=Bar):
	    # __metaclass__ = Bar # python2的写法
	    pass

当我们运行这段代码时，python进行了如下操作：

1、Foo中有__metaclass__的属性么？如有，py将通过__metaclass__创建一个名字为Foo的类（对象）

2、如果没有找到__metaclass__，它会继续在其继承的父类中去寻找__metaclass__属性，并尝试和之前相同的操作。

3、如果python在父类中都找不到__metaclass__，python会在模块层次去寻找__metaclass__，并尝试做和前面一样的操作。

4、如果还是找不到__metaclass，那么python将会用内置的type去创建这个对象。

**那么问题就显而易见了，__metaclass__指什么，答案就是可以创建一个类的东西。创建一个类需要type或继承自type的子类（对象）。**

# 7、自定义元类

**元类的主要目的就是为了创建类的时候能够自动的改变类。**

举一个帮助理解的例子：你决定在你的模块里所有的类的属性都应该是大写形式。有一些办法可以办法，其中一种就是在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们需要做的就是在元类中把所有索性全部改为大写就可以了。

值得一提的是，__metaclass__实际上可以被任意调用，它并不需要一个正式的类，所以下面先以一个函数来开始。

	def upper_attr(class_name, parent_class, attr):
	    new_attr = {}
	    print(class_name)
	    print(parent_class)
	    print(attr)
	    for name, value in attr.items():
	        if not name.startswith('__'):
	            new_attr[name.upper()] = value
	    return type(class_name, parent_class, new_attr)
	
	
	class Bar(object):
	    pass
	
	
	class MyClass(object):
	    pass
	
	
	class Foo(MyClass, Bar, metaclass=upper_attr):
	    # __metaclass__ = Bar
	    test = 'test'
	
	
	foo = Foo()
	print(foo)
	print(hasattr(foo, 'test'))
	print(hasattr(foo, 'TEST'))

结果：

	Foo
	(<class '__main__.MyClass'>, <class '__main__.Bar'>)
	{'__module__': '__main__', '__qualname__': 'Foo', 'test': 'test'}
	<__main__.Foo object at 0x0000000002BA4748>
	False
	True

如上面代码，class_name是当前类名，parent_class为要继承的父类，attr为字典形式所有的类属性。

下面再考虑用一个真正的class作为元类。

	class Bar(object):
	    pass
	
	
	class MyMetaClass(type):
	    def __new__(cls, class_name, class_parents, class_attr):
	        print(cls)
	        new_attr = {}
	        for name, value in class_attr.items():
	            if not name.startswith('__'):
	                new_attr[name.upper()] = value
		        # return type(class_name, class_parents, new_attr)
		        return type.__new__(cls, class_name, class_parents, new_attr)
	
	
	class Foo(Bar, metaclass=MyMetaClass):
	    # __metaclass__ = Bar
	    test = 'test'
	
	
	foo = Foo()
	print(foo)
	print(hasattr(foo, 'test'))
	print(hasattr(foo, 'TEST'))

从上面的代码可以理解，**元类的作用基本就是拦截类的创建，然后修改这个待创建的类，最后返回修改后的类。**


下一篇会理解`__new__`、`__init__`、`__call__`等魔术方法。

最后为什么要使用元类，用python界的领袖Tim Peters的话来说：元类是深度的魔法，99%的人应该不为此操心什么。**如果你想搞清楚是否需要用到元类，那么就不需要用到它。那些实际用到元类的人很清楚他们需要做什么，而且根本不需要去解释为什么要用元类。**

# 8、利用元类实现ORM

## 8.1 ORM是什么

ORM（object relational mapping）对象关系印射，是py后端框架django的核心思想。

通俗点理解就是通过创建一个实例对象，用创建它的类当作表名，用创建它的类属性作为表的字段，当对这个实例对象进行操作时，能够生成对应的sql语句。

下面一个简单的demo：

	class User(object):
	    uid = ('uid', "int unsigned")
	    name = ('username', "varchar(30)")
	    email = ('email', "varchar(30)")
	    password = ('password', "varchar(30)")
	
	
	u = User(uid=12345, name='Michael', email='test@orm.org', password='my-pwd')
	u.save()
	# 对应如下sql语句
	# insert into User (username, email, password, uid) values ('Michael', 'test@orm.org', 'my-pwd', 12345)

将实现的效果如上，即**ORM的作用就是：让开发者操作数据库的时候，能够像操作对象时通过其属性赋值等操作一样简单。**

## 8.2 通过元类实现ORM中的insert功能

编写底层模块的第一步就是先把调用接口写出来，比如想写一个ORM框架，想定义一个User类来操作相应的数据库表user，需要开发者写的代码类似这个样子：

	class User(Model):
	    id = IntegerField('id')
	    name = StringField('name')
	    age = IntegerField('age')
	    address = StringField('address')
	
	
	# 创建一个user实例
	user = User(id=1, name='daocoder', age=27, address='anhui')
	# 保存到数据库中
	user.save()

其中父类Model和属性类型IntegerField和StringField都是由ORM框架提供，剩下的方法由metaclass完成，即创建Model的元类。

下面就按照上面的思路来实现这个简单的ORM框架。

**1、首先定义Field类，它负责定义数据表中字段名和字段类型长度等。**

	class Field(object):
	    def __init__(self, name, column_type):
	        self.name = name
	        self.column_type = column_type
	
	    def __str__(self):
	        return '<%s:%s>' % (self.__class__.__name__, self.name)

**2、在Field的基础上再定义各种数据类型，StringField和IntegerField等。**

	class IntegerField(Field):
	    def __init__(self, name, column_type='int(11)'):
	        super(IntegerField, self).__init__(name, column_type)
	
	
	class StringField(Field):
	    def __init__(self, name, column_type='varchar(100)'):
	        super(StringField, self).__init__(name, column_type)

**3、下面开始定义基类Model模型。**

	class Model(dict, metaclass=ModelMetaClass):
	
	    def __init__(self, **kwargs):
	        super(Model, self).__init__(**kwargs)
	
	    def __getattr__(self, key):
	        try:
	            return str(self[key])
	        except KeyError:
	            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
	
	    def __setattr__(self, key, value):
	        self[key] = str(value)
	
	    def save(self):
	        fields = []
	        args = []
	        for k, v in self.__mappings__.items():
	            print(k, v, v.name, v.column_type)
	            fields.append(v.name)
	            args.append(getattr(self, k))
	        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args))
	        print('SQL: %s' % sql)
	        print('ARGS: %s' % str(args))

**4、编写元类ModelMetaclass**

	class ModelMetaClass(type):
	    def __new__(cls, class_name, class_parents, class_attr):
	        if class_name == 'Model':
	            return type.__new__(cls, class_name, class_parents, class_attr)
	        print('found model %s' % class_name)
	        mappings = {}
	        for name, value in class_attr.items():
	            if isinstance(value, Field):
	                mappings[name] = value
	        for k in mappings.keys():
	            class_attr.pop(k)
	        class_attr['__mappings__'] = mappings
	        class_attr['__table__'] = class_name.lower()
	        return type.__new__(cls, class_name, class_parents, class_attr)

全部代码：

	class Field(object):
	    def __init__(self, name, column_type):
	        self.name = name
	        self.column_type = column_type
	
	    def __str__(self):
	        return '<%s:%s>' % (self.__class__.__name__, self.name)
	
	
	class IntegerField(Field):
	    def __init__(self, name, column_type='int(11)'):
	        super(IntegerField, self).__init__(name, column_type)
	
	
	class StringField(Field):
	    def __init__(self, name, column_type='varchar(100)'):
	        super(StringField, self).__init__(name, column_type)
	
	
	class ModelMetaClass(type):
	    def __new__(cls, class_name, class_parents, class_attr):
	        if class_name == 'Model':
	            return type.__new__(cls, class_name, class_parents, class_attr)
	        print('found model %s' % class_name)
	        mappings = {}
	        for name, value in class_attr.items():
	            if isinstance(value, Field):
	                mappings[name] = value
	        for k in mappings.keys():
	            class_attr.pop(k)
	        class_attr['__mappings__'] = mappings
	        class_attr['__table__'] = class_name.lower()
	        return type.__new__(cls, class_name, class_parents, class_attr)
	
	
	class Model(dict, metaclass=ModelMetaClass):
	
	    def __init__(self, **kwargs):
	        super(Model, self).__init__(**kwargs)
	
	    def __getattr__(self, key):
	        try:
	            return str(self[key])
	        except KeyError:
	            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
	
	    def __setattr__(self, key, value):
	        self[key] = str(value)
	
	    def save(self):
	        fields = []
	        args = []
	        for k, v in self.__mappings__.items():
	            print(k, v, v.name, v.column_type)
	            fields.append(v.name)
	            args.append(getattr(self, k))
	        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args))
	        print('SQL: %s' % sql)
	        print('ARGS: %s' % str(args))
	
	
	class User(Model):
	    id = IntegerField('id')
	    name = StringField('name')
	    age = IntegerField('age')
	    address = StringField('address')
	
	
	user = User(id='1', name='daocoder', age=27, address='anhui')
	user.save()

跑起来：

	found model User
	id <IntegerField:id> id int(11)
	name <StringField:name> name varchar(100)
	age <IntegerField:age> age int(11)
	address <StringField:address> address varchar(100)
	SQL: insert into user (id,name,age,address) values (1,daocoder,27,anhui)
	ARGS: ['1', 'daocoder', '27', 'anhui']

解释一番：

User类定义继承自父类Model，且有4个属性，4个属性分别继承自IntegerField和StringField，这两个继承自Field，这个不谈。聚焦Model。

1、实例化User时，去找父类Model，发现父类拥有metaclass属性值为ModelMetaClass，即它是由一个自定义的元类来创建的类，向上寻找ModelMetaClass，这个类是继承自type。需要先创建它的实例对象。调用其静态方法__new__，这里面4个参数(cls, class_name, class_parents, class_attr)，分别为ModelMetaClass的类对象、Model类名、父类(dict, )元组、自身内置属性。类名为Model时，直接创建`type.__new__(cls, class_name, class_parents, class_attr)`并返回。再调用Model类的__init__方法，调用了父类dict的__init__的方法。父类Model作为类对象创建完成。

2、开始User类对象的创建，Model已有，然后开始创建User，还是向上找到了ModelMetaClass，这时的4个参数分别是(cls, class_name, class_parents, class_attr)，分别为ModelMetaClass的类对象、User类名、父类(Model, )元组、自身内置属性包含id，name，age，address等。然后判断类名不是Model，继续向下，将User属性遍历，其实例自Field的属性封装为User类对象的__mappings__属性，类名User为User类对象的__table__属性。

3、调用实例对象user.save方法，没啥可说的了，调用类对象获取其属性的内置方法。

# 9、致谢

[python 简易ORM](https://blog.csdn.net/yang5102/article/details/52485977)

某平台内部培训资料。









