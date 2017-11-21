
# python模块（包）之urllib

[urllib：官方文档是最好的模块表达说明。](https://docs.python.org/3.6/library/urllib.html)

urllib is a package that collects several modules for working with URLs:

- urllib.request for opening and reading URLs
- urllib.error containing the exceptions raised by urllib.request
- urllib.parse for parsing URLs
- urllib.robotparser for parsing robots.txt files

大体来说就是urllib是一个包含request、error、parse、robotparser四个模块，关乎网络资源请求的包。request模块用来发起网络资源请求；error模块用来在request网络资源过程中搜集异常报错；parse模块用来对url地址进行处理；robotparser模块用来解析robots.txt文件（未知）。

# 1、request

The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP) in a complex world — basic and digest authentication, redirections, cookies and more.

## 1.1 方法

**urllib.request.urlopen(url, data=None, [timeout, ], cafile=None, capath=None, cadefault=False, context=None)**：

- url，可以是url地址字符串，或者是Request对象（下面会提到）。
- data，指定发送到服务器的数据对象。
- cafile、capath，发起HTTPS请求时指定一组可信的CA证书。cafile应指向包含一系列CA证书的单个文件，而capath应指向散列证书文件的目录。
- context，该参数若被指定，必须是`ssl.SSLContext`对象。
- timeout，请求超时时间。

这里一般url、data、timeout三个参数还比较常用。

该函数返回一个上下文管理对象，包含一下几种方法获取返回结果的相关信息：

- geturl()：返回检索的资源的URL，通常用于确定是否遵循重定向。
- info()：以`email.message_from_string()`实例的形式返回页面的元信息，如头信息。
- getcode()：返回http响应的状态码。

对于http和https，除上述的几个函数获取信息外，该函数返回也是对`http.client.HTTPResponse`稍加修改的对象，其详细说明见下方官档。

[HTTPResponse Objects 官档](https://docs.python.org/3.6/library/http.client.html#httpresponse-objects)

`HTTPResponse Objects`这个对象常用方法有：

- read()：读取响应主体，数据格式为bytes类型，需要decode()解码，要按编码转换成str类型。
- msg：http.client.HTTPMessage包含响应标头实例。
- status：服务器的状态码。
- reason：服务器返回的原因短语。
- closed：数据流被关闭时为True。

在查看urllib的源码`request.py`找到类`OpenerDirector`，其下面方法`open`可以找到下面几行代码：

	if isinstance(fullurl, str):
	    req = Request(fullurl, data)
	else:
	    req = fullurl
	    if data is not None:
	        req.data = data

**urllib.request.urlopen()** 方面介绍里面提到：请求资源可以是url地址字符串，或者是Request对象。再看上面一段代码**isinstance(fullurl, str)**传递的fullurl是str的实例对象，就将fullurl等转化为Request的实例对象。

所以请求资源是url地址字符串或是Request对象都殊途同归，最终会转为Request的实例对象进行资源请求。下面的子类会对Request对象进行详细介绍。

附加这个方法对应的去注释源码。

	def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
	            *, cafile=None, capath=None, cadefault=False, context=None):
	    global _opener
	    if cafile or capath or cadefault:
	        import warnings
	        warnings.warn("cafile, cpath and cadefault are deprecated, use a "
	                      "custom context instead.", DeprecationWarning, 2)
	        if context is not None:
	            raise ValueError(
	                "You can't pass both context and any of cafile, capath, and "
	                "cadefault"
	            )
	        if not _have_ssl:
	            raise ValueError('SSL support not available')
	        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,
	                                             cafile=cafile,
	                                             capath=capath)
	        https_handler = HTTPSHandler(context=context)
	        opener = build_opener(https_handler)
	    elif context:
	        https_handler = HTTPSHandler(context=context)
	        opener = build_opener(https_handler)
	    elif _opener is None:
	        _opener = opener = build_opener()
	    else:
	        opener = _opener

这里面注意几个变量。

a、**https_handler**：姑且称为**资源构造器**，它相当于处理不同网络资源的句柄对象，如HTTPHandler、HTTPSHandler、FileHandler、FTPHandler、UnknownHandler等类的实例对象。

b、**opener = build_opener(https_handler)**：姑且称为**资源钥匙**，它是一个` OpenerDirector`类的实例对象，其参数是上面说的资源构造器，用这把钥匙可以打开网络的任意资源。

下面继续`request`模块的方法介绍。

**urllib.request.build_opener([handler, ...])**：构造**资源钥匙**，它是一个` OpenerDirector`类的实例对象，其参数是上面说的资源构造器。

- handler，HTTPHandler、HTTPSHandler、FileHandler、FTPHandler、UnknownHandler等类的实例对象。

**urllib.request.install_opener(opener)**：插入**资源钥匙**，载入` OpenerDirector`子类的实例对象，用来请求网络资源。

- opener，常为build_opener([handler, ...])方法得到的` OpenerDirector`类的实例对象。


## 1.2 request常用子类

**urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)**：网络资源请求的抽象。

- url，网络资源地址字符串。
- data， 请求携带数据，常为post表单数据。
- headers，携带请求头，一些http常用请求头信息。
- method，指明请求方法，GET、POST、PUT之类。

**urllib.request.HTTPCookieProcessor(cookiejar=None)**：处理http cookie。

- cookiejar，一般为`cookielib.CookieJar()`方法保存的cookie文件。

**urllib.request.ProxyHandler(proxies=None)**：代理请求。

- proxies，字典形式。如`{'sock5': 'localhost:1080'}`、`{'https': '192.168.8.8:2365'}`。

**urllib.request.FileHandler()**：一个文件对象。（不知是否可以作为上传文件使用。）

这些子类又有一些自己的方法，大多暂且不介绍，附`Request`类的方法官档链接。

[Request类的方法官档](https://docs.python.org/3.6/library/urllib.request.html#request-objects)

# 2、error

处理由request请求产生的错误。

**urllib.error.URLError**：地址错误，有属性如下：

- reason，可能是错误字符串或其它的错误实例。

**urllib.error.HTTPError**：网络请求错误，有属性如下：

- code，http状态码。
- reason，错误原因。
- headers，响应头。

# 3、parse

The urllib.parse module defines functions that fall into two broad categories: URL parsing and URL quoting. These are covered in detail in the following sections.

这个模块提供处理url的标准接口，两种：解析处理和引用处理。

## 3.1 URL Parsing

The URL parsing functions focus on splitting a URL string into its components, or on combining URL components into a URL string.

**urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)**：url地址解析。

url地址通常标准格式如下：`scheme://netloc/path;parameters?query#fragment`详细说明介绍可见`http.md`的介绍。返回是6个元素组成的元组。

- urlstring，urlstring地址字符串。
- scheme，指定默认协议。
- allow_fragments，False时将不进行fragment解析，直接将其视作path、query或parameters的一部分。

**urllib.parse.parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')**：解析url参数字符串。

- qs，查询子串。
- keep_blank_values，百分比编码查询的空白值是否应视为空白字符串。
- strict_parsing，如果解析错误，false为默认忽略，否则错误引发ValueError异常。
- encoding，errors。可选的编码和错误参数指定如何将百分比编码的序列解码为Unicode字符。

## 3.2 URL Quoting

**urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)**：多参数元组拼接为百分比编码后的字符串。

# 4、写在后面

概念比较空洞，实践出真知。简单内容可以参见`threading_douban.py`。
































