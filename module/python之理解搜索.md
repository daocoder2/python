<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之理解搜索

# 1、顺序查找

## 1.1 顺序查找

当数据项存储在诸如列表的集合中，我们说它们有线性和顺序关系。每个数据项都存储在相对其它数据项的位置。python列表中，这些相对位置是单个项的索引值。这些索引值是有序的，我们可以按照顺序来访问它们。即顺序查找。

从列表的第一个项开始，我们按照基本的顺序排序，简单地从一个项移动到另一个项，直到找到我们正在寻找的项或遍历完整个列表找不到要寻找的项。

代码如下：

	def senquential_search(search):
	    origin_list = [1, 2, 4, 5, 6]
	    list_length = len(origin_list)
	    i = 0
	    found = False
	    while i < list_length and not found:
	        if origin_list[i] == search:
	            found = True
	        else:
	            i = i+1
	    if found:
	        print('found the search data %d and its index is %d' % (search, i))
	    else:
	        print('the search data %d not found' % search)

结果：

	found the search data 4 and its index is 2
	the search data 7 not found

## 1.2 顺序查找分析

首先，项在列表任何位置的概率都是一样的。然后查找某一项是否存在的唯一方法就是将其与每个项进行比较。能找到的话，三种情况：最好开头找到、其次中间找到、最差末尾找到。

平均下来计算的话，我们会在列表的中间找到该项，即我们将循环`n/2`次，当n无限大时，那么顺序查找的复杂度（大O符号）就是`O(n)`。

## 1.3 有序查找的引子

上面的假设是列表中的项是随机的，没有大小相对顺序的，试想下如果列表中的项以某种顺序排序。当带搜索项大于一定值，就停止搜索。顺序查找会取得一些好的效率么。

	def senquential_search(search):
	    origin_list = [0, 1, 2, 8, 13, 17, 19, 32, 42]
	    list_length = len(origin_list)
	    i = 0
	    found = stop = False
	    while i < list_length and not found and not stop:
	        if origin_list[i] == search:
	            found = True
	        else:
	            if origin_list[i] > search:
	                stop = True
	            else:
	                i = i + 1
	
	    if found:
	        print('found the search data %d and its index is %d' % (search, i))
	    else:
	        print('the search data %d not found' % search)

结果如下：

	senquential_search(16)
	senquential_search(7)

不过分析起来结果如上节，没啥改善。不过还是为下节做准备，就是**有序列表以特定的方式去查找能否会取得更高的效率**。

# 2、二分查找

## 2.1 二分查找

有序列表对于我们的比较是很有用的。在顺序查找中，当我们与第一个项进行比较时，如果不是我们需要的，则最多还有n-1项去查找。

二分查找建立在一个有序列表上，如列表从小到大排序。然后它查找时从中间开始查找，如果该项是我们的搜索项，即完成了查找；如果不是，我们可以利用列表的有序性消除剩余项一半的元素。如果我们的搜索项大于中间项，就可以消除中间项及比中间项小的一半元素。即如果搜索项在列表中，它肯定在中中间项大的那一半元素中。最后不断改变首尾元素的起始位置（改变中间项），找到搜索项。

	def binary_search(search):
	    origin_list = [0, 1, 2, 8, 13, 17, 19, 32, 42]
	    list_length = len(origin_list)
	    firstpos = 0
	    lastpos = list_length - 1
	    found = False
	    while firstpos <= lastpos and not found:
	        middlepos = (firstpos + lastpos) // 2
	        if origin_list[middlepos] == search:
	            found = True
	        else:
	            if origin_list[middlepos] > search:
	                lastpos = middlepos-1
	            else:
	                firstpos = middlepos + 1
	
	    if found:
	        print('found the search data %d and its index is %d' % (search, middlepos))
	    else:
	        print('the search data %d not found' % search)
	
	
	binary_search(17)
	binary_search(7)

结果：

	found the search data 17 and its index is 5
	the search data 7 not found

## 2.2 二分查找中的递归思想

下面继续分析之前，可以发现这个算法是分而治之的很好的例子。分和治意味着我们可以将问题分为更小的部分，以某种方式解决这个小部分，最后再重新组合整个问题以获得结果。

当我们执行列表的二分查找时，我们首先检索中间项。如果我们正在搜索的项小于中间项，我们可以简单地对原始列表的左半部分进行二分查找。同样，项大，即右半部分二分查找。不过那种方式，都是递归调用二分查找函数。

	def binary_search(search_list, search):
	    if len(search_list) == 0:
	        print('the search data %d not found' % search)
	    else:
	        middlepos = len(search_list) // 2
	        if search_list[middlepos] == search:
	            print('found the search data %d and its index is %d' % (search, middlepos))
	        else:
	            if search_list[middlepos] > search:
	                binary_search(search_list[:middlepos-1], search)
	            else:
	                binary_search(search_list[middlepos+1:], search)
	
结果：
	
	binary_search([0, 1, 2, 8, 13, 17, 19, 32, 42], 17)
	binary_search([0, 1, 2, 8, 13, 17, 19, 32, 42], 7)

## 2.3 二分查找分析

为了分析二分查找算法，我们需要先知道每个计较大约消除了一半的元素，该算法检查整个列表的最大比较次数是多少？假如从n项开始，大约n/2项将在第一次比较后留下，然后第二次余下n/4，继而n/8、n/16……。

当我们拆分足够多次后，我们最终会得到只有一个项的列表。这个要么是我们寻找的项，要么不是。达到这一点的比较次数是i，那么`n/2^i=1`时，求解出i=log^n。最大比较次数相对于列表中的项是对象的。因此二分查找是O（log^n）。

另一个分析的问题是在上面的递归求解的例子中：

	binary_search(alist[:midpoint],item)

使用切片运算创建列表的左半部分，然后传递到下一个调用（同样对右半部分）。我们上面做的分析假设切片操作符是恒定时间的。然而，我们知道python中的slice运算符实际上是O（k）。这意味着使用slice的二分查找将不会在严格的对数时间执行。幸运的是，这可以通过传递列表联通开始和结束的索引来纠正，如不利用递归实现的二分查找。

即使二分查找通常比顺序查找更好，但更重要的需要注意，对于小的n的值，排序的额外成本可能不值得。实际中，我们应该经常考虑采取额外的分类工作是否可以是搜索获得好处。我们可以排序一次，然后进行很多次查找，那么排序的成本就可以忽略。然后对大型的列表，排序一次的代价可能是昂贵的，从一开始就执行顺序查找可能是最好的选择。

# 3、hash查找

## 3.1 hash查找

在之前的部分，我们已经知道利用项在集合中相对彼此的位置来改进我们的搜索算法。如一个列表是有序的，我们可以使用二分法查找在对数时间中查找。下面将继续进一步建立一个可以在O（1）时间内搜索的数据结构。这个概念被称为hash查找。

为了做到这一点，当我们在集合中查找项时，我们需要更多的去了解项可能在哪里。如果每个项都在该在的地方，那么搜索可以使用单个比较就能发现项的存在。然后，通常实际情况并不是这样。

`哈希表`是以一种容易找到它们方式存储项的集合。哈希表的每个位置，通常称为一个槽，可以容纳一个项，并且从0开始的整数值命名。最初哈希表不包含项，因此每个槽都为空。python中可以利用列表来实现一个哈希表，每个元素初始化为None。

![列表模拟hash](https://i.imgur.com/BguJwbt.png)

**项和该项在散列表中所属的槽之间的印射被称为hash函数。**hash函数将接收集合中的任何项，并在槽名范围内（0和m-1）返回一个整数。假设我们有54,26,93,17,77和31的集合。我们的第一个hash函数称为余数法，只需要一个项除以其表大小，返回剩余部分作为其散列值（h(item)=item%11)。**这种余数方法（模运算）通常以某种形式存在所有散列函数中，因此结果必须在槽名的范围之内。**

![hash查找-hash函数-余数法.png](https://i.imgur.com/15vTs6W.png)

一旦计算了哈希值，我们可以将每个项插入到指定位置的哈希表中，如下所示。注意，**11个插槽的6个已经被占用，这被称为负载因子，通常表示为`λ=项数/表大小`。**这个例子中，λ=6/11。

![hash查找-余数法-hash列表](https://i.imgur.com/OUMA7FK.png)

**现在当我们要所有一个项时，我们只需要使用哈希函数来计算项的槽名称，然后检索哈希表以查看它是否存在。**该搜索操作是O（1），因为需要恒定的时间量来计算**散列值**，然后在该位置索引散列列表。如果正确的话，我们将找到这个项。

然后基于以上，我们能注意到只有每个项印射到哈希表中的唯一位置，这种技术才会起作用。例如44和77的散列值都是0。**根据散列函数，一个或更多的项要在同一槽中，这种现象被称为碰撞（它也可以被称为冲突）。**显然，冲突是散列技术产生了问题。

## 3.2 hash函数

**给定项的集合，将每个项印射到唯一槽的散列函数被称为完美散列函数**。如果我们知道项和集合永远不会改变，那么可以构造一个完美的散列函数。**不幸的是，实际中给定任意项的集合，没有系统的方法来构建完美的散列函数，幸运的是，我们不需要散列函数是完美的，仍旧可以提高性能。**

总是有具有完美散列函数的一种方式是增加散列表的大小，是的可以容纳项范围中的每个可能值。这保证每个项将具有唯一的槽。虽然这个对于小项目是实用的，但是当项的数目尽可能大的时候是不可行的。例如项是九个数字的社保号码，那么这个方法将需要大约10亿个槽，如果只是存储几个学生的数据，那么将浪费大量的内存。

**我们的目标是构建一个散列函数，最大限度地减少冲突数，易于计算，并均匀分布在哈希表中的项。**有很多方法扩展**简单余数法**，下面将介绍几个。

### 3.2.1 分组求和法

将项分为相等大小的块，最后一块可能不是相等大小。然后将这些块加在一起求出散列值。如我们的项是电话号码 `436-555-4601`，我们将取出数字，并将他们分为两位数（43,65,55,46,01）,`43 + 65 + 55 + 46 + 01=210`，相加为210.我们假设哈希表一共11个槽，这种情况下，`210%11=1`，因此电话号码的`436-555-4601`散列到槽1。一些分组求和法会在求和之前每隔一个反转，即（43,56,55,64,01），` 43+56+55+64+01=219`，散列值为`219%11=10`。

### 3.2.2 平方取中法

先对该项平方，然后提取一部分数字结果。例如项是44，我们将计算`44^2=1936`，通过提取中间两个数字得到`93`，我们得到`93%11=5`。

### 3.2.3 基于字符的项

基于字符的项去创建散列函数同样可以。`cat`可以看作是ascii值的序列。

	>>> ord('c')
	99
	>>> ord('a')
	97
	>>> ord('t')
	116

然后我们可以获取这三个ascii值，将它们相加，并使用余数方法获取散列值。

	def hash(astring, tablesize):
	    sum = 0
	    for pos in range(len(astring)):
	        sum = sum + ord(astring[pos])
	
	    return sum%tablesize

有趣的是，当使用次散列函数时，不同顺序的字符换总会返回相同的散列值。那么我们就将字符的位置作为权重重新计算。

![hash查找-字符hash函数加权重](https://i.imgur.com/haBxJmd.png)

同样的我们可以自己实现一些方法来计算集合中项的散列值。但是万变不离其宗的是：哈希函数必须是搞笑的，以便它不会成为存储和搜索过程中的主要部分。否则本末倒置了。

## 3.3 解决冲突

现在再回到碰撞的问题，**当两个项散列值在同一槽时，我们必须有一个系统的方法将第二个项放在散列表中，这个过程称之为冲突解决。**如前所述，如果散列函数是完美的，冲突将永远不会发生，然而实际中，冲突解决称为解决散列非常重要的一部分。

**解决冲突的办法一种叫做查找散列表，尝试查找到另一个空槽以保存导致冲突的项。一个简单的办法就是从原始的哈希位置开始，然后以顺序方式移动槽，知道遇到第一个空槽。注意，我们也可能需要回到第一个槽（循环）以查找整个散列表。这种冲突解决过程被称为开放寻址，因为它试图在散列表中找到下一个空槽或地址。通过系统地一次访问每个槽，我们执行称为线性探测的开放寻址计数。**

下面展示了在简单余数法散列函数`（54,26,93,17,77,31,44,55,20）`下整数项的扩展集合。当我们尝试将44放入槽0时，发生冲突，先线性探测下，我们卓哥顺序观察，知道找到位置。这时我们找到槽1。再次，55应该在槽0中，但是必须放在槽2中，因为它是下一个开放位置，值20散列到槽9。由于槽9已满，进行线性探测，我们访问槽10,0,1和2，最后在位置3找到一个空槽。**这里依次移位寻找空槽的位置，这里很明显看出会影响之后的项的插入。**

![冲突解决-线性探测的开放寻址技术](https://i.imgur.com/zpsTpm4.png)

一旦我们使用线性探测和开放寻址建立了哈希表，我们就必须使用相同的方法来搜索项。假设我们相差找93，当我们计算哈希值时，我们得到5，查看槽5得到93，返回True。如果我们查找20，这时哈希值是9，而槽9的当前项是31，我们不能简单的返回False，因为我们知道可能存在冲突。**我们被迫做一个顺序搜索，从位置10开始寻找，知道我们找到项20或我们找到一个空槽。**

**线性探测的缺点是聚集的趋势**：项在表中聚集，意味着如果在相同的散列值处发生很多冲突，则将线性探测来填充多个周边槽。这将影响正在插入的其他项，假如我嫩尝试添加上面的项20时看到的，必须跳过一组值为0的值，最终找到开放位置。

处理聚集的一种方式是扩展线性探测技术，使得不是顺序地查找下一个开放槽，而是跳过槽，从而更均匀地分布引起冲突的项。这将潜在地减少发生的聚集 。如下图所示`加3`探头进行碰撞识别时的项，意味着一旦发生碰撞，我们将查看之后的第三个槽，直到找到一个槽为空。

![hash查找-加3线性探测解决冲突](https://i.imgur.com/IZWVeAf.png)

在冲突后寻找另一个槽的过程叫做`重新散列`。使得简单的线性探测，`rehash`函数是`newhashvalue=rehash(oldhashvalue)`，其中`rehash(pos)=(pos+1)%sizeoftbale`。`加3`可以定义为`rehash(pos)=(pos+3)$sizeoftable`。一般来说为`rehash(pos)=(pos + skip)％sizeoftable`。**重要的是，“跳过”的大小必须使得表中的所有槽最终都被访问。否则，表的一部分将不会被使用。为了确保这一点，通常建议表的大小是素数。**

线性探测思想的另一个变种称为二次探测。代替使用常量“跳过”值，使用rehash函数，将散列值递增1，3，5，7，9依此类推，这意味着如果第一哈希值是h，则连续值是h+1，h+4，h+9，h+16等，换句话说，二次探测使用由连续完全正方形组成的跳跃。下图示例：

![hash查找-变种线性探测-依次递增解决冲突](https://i.imgur.com/OIzffCw.png)

用于冲突解决的提到方式允许每个槽保持对项的集合（或链）的引用。连接允许许多项存在哈希表中相同的位置。当发生冲突时，项仍旧放在散列表的正确槽中。随着越来越多的项放在哈希到相同的位置，搜索集合中的项的难度增加。如下使用链解决冲突。

![hash查找-集合或链解决冲突](https://i.imgur.com/jUGib65.png)

当我们要搜索一个项时，我们使用散列函数来生成它应该在的槽，由于每个槽都有一个集合，我们使用一种搜索计数来查找该项是否存在。优点在于平均来说，每个可能有更少的项，搜索可能有效。

## 3.4 实现map抽象数据类型

最有用的python集合之一是字典。字典是一种关联数据类型，你可以在其中存储键值对，该键用于查找关联的值，我们经常称之为`map`。

map的抽象数据类型定义如下。该结构是键值之间的管理的无序集合。map中的键都是唯一的，因此键值之间存在一对一的关系。操作如下：

- Map()：创建一个新的map。它返回一个空的map集合。
- put(key, value)：向map中添加一个新的键值对。如果键已经在map中，那么新值替换旧值。
- get(key)：根据指定的键返回存储的值、
- del(map[key])：删除指定的键值对。
- len()：返回集合键值对数量。
- in ：key in map类似语句，找到返回True，否则返回False。

字典的一个很大的好处就是给定一个键，我们可以快速根据这个键去查找相关的值。为了加速这种查找能力，我们需要支持一个高效的搜索的实现。我们可以使用具有顺序或二分查找的列表，但是如果使用上面的哈希表将更好，因为查找哈希表的项可以接近O(1)的性能。

我们使用两个列表来创建一个实现Map抽象数据类型的HashTable类。一个名为`slots`的列表将保存键项，一个名为`data`的并行列表将保存数据值。当我们查找一个键时，`data`列表中相应位置将保存相关的数据值。我们将使用前面提出的想法将键列表视为哈希表。这里注意哈希表的初始已被选择为11，尽管这是任意的，但重要的是，大小是质数，使得冲突解决的算法可以尽可能的提高。

	class HachTable(object):
	    def __init__(self):
	        self.size = 11
	        self.slots = [None] * self.size
	        self.data = [None] * self.size

hash函数实现简单的余数方法。冲突解决是`加1`函数的线性探测。put函数将定最终将有一个空槽，除非key已经存在于`self.slots`，它计算原始哈希值，如果该槽部位空，则迭代rehash函数，直到出现空槽。如果非空槽已经包含key，则旧数据替换为新数据。

    def put(self, key, value):
        hashvalue = self.hash_function(key)
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = value
        else:
            if self.slots[hashvalue] == key:
                self.slots[hashvalue] = value
            else:
                nextslot = self.rehash(hashvalue)
                while self.slots[nextslot] !=None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot)
                if self.slots[nextslot] == None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = value
                else:
                    self.data[nextslot] = value

    def hash_function(self, value):
        return value % self.size

    def rehash(self, oldhash):
        return (oldhash + self.hop) % self.size

同样get函数从计算初始哈希值开始，如果值不在槽中，那么rehash定位下一个可能的位置。搜索将通过检索以确保我们没有返回到初始槽来终止。如果发生这种情况，我们已用尽所有的槽，并且项不存在。

HashTable类提供了附加的字典功能。我们重载`__getitem__`和`__setitem__`方法以允许使用[]访问。这意味着一旦创建了HashTable。索引操作符将可用。

    def get(self, key):
        startslot = self.hash_function(key)
        data_value = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and not stop and not found:
            if self.slots[position] == key:
                found = True
                data_value = self.data[position]
            else:
                position = self.rehash(position)
                if position == startslot:
                    stop = True
        return data_value

    def hash_function(self, value):
        return value % self.size

    def rehash(self, oldhash):
        return (oldhash + self.hop) % self.size

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)

完整数据：

	class HachTable(object):
	    def __init__(self):
	        self.size = 11
	        self.hop = 1
	        self.slots = [None] * self.size
	        self.data = [None] * self.size
	
	    def put(self, key, value):
	        hashvalue = self.hash_function(key)
	        if self.slots[hashvalue] == None:
	            self.slots[hashvalue] = key
	            self.data[hashvalue] = value
	        else:
	            if self.slots[hashvalue] == key:
	                self.slots[hashvalue] = value
	            else:
	                nextslot = self.rehash(hashvalue)
	                while self.slots[nextslot] !=None and self.slots[nextslot] != key:
	                    nextslot = self.rehash(nextslot)
	                if self.slots[nextslot] == None:
	                    self.slots[nextslot] = key
	                    self.data[nextslot] = value
	                else:
	                    self.data[nextslot] = value
	
	    def get(self, key):
	        startslot = self.hash_function(key)
	        data_value = None
	        stop = False
	        found = False
	        position = startslot
	        while self.slots[position] != None and not stop and not found:
	            if self.slots[position] == key:
	                found = True
	                data_value = self.data[position]
	            else:
	                position = self.rehash(position)
	                if position == startslot:
	                    stop = True
	        return data_value
	
	    def __getitem__(self, key):
	        return self.get(key)
	
	    def __setitem__(self, key, data):
	        self.put(key, data)
	
	    def hash_function(self, value):
	        return value % self.size
	
	    def rehash(self, oldhash):
	        return (oldhash + self.hop) % self.size
	
	
	H = HachTable()
	H[54] = "cat"
	H[26] = "dog"
	H[93] = "lion"
	H[17] = "tiger"
	H[77] = "bird"
	H[31] = "cow"
	H[44] = "goat"
	H[55] = "pig"
	H[20] = "chicken"
	print(H.slots)
	print(H.data)
	H.put(20, 'monkey')
	print(H.data)
	print(H[20])

结果为：

	[77, 44, 55, 20, 26, 93, 17, None, None, 31, 54]
	['bird', 'goat', 'pig', 'chicken', 'dog', 'lion', 'tiger', None, None, 'cow', 'cat']
	['bird', 'goat', 'pig', 'monkey', 'dog', 'lion', 'tiger', None, None, 'cow', 'cat']
	monkey

## 3.5 hash法分析

在最好的情况下，散列将提供O(1)，恒定时间搜索。然而，由于冲突，比较的数量通常不是那么简单。

我们需要**分析散列表的使用最重要的信息是负载因子λ（λ=项数/表大小）**。如果λ小，则碰撞的机会较低，这意味着更可能在它们所属的槽中。如果λ大，意味着表正在填满，则存在越来越多的冲突，这意味着解决冲突更加困难，需要更多的比较去找到一个空槽。使用链接，增加的碰撞意味着每个链上的项数量增加。

# 4、感谢

这系列将是学习交流、非原创。

[排序和搜索](https://facert.gitbooks.io/python-data-structure-cn/5.%E6%8E%92%E5%BA%8F%E5%92%8C%E6%90%9C%E7%B4%A2/5.1.%E7%9B%AE%E6%A0%87/)



