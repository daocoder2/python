
# python模块（包）之网络请求（爬虫）相关包介绍

网络请求最复杂莫过于爬虫，不同的业务场景应用的工具不尽相同，下面简明介绍一些基础的库（模块），然后其中一些会在模块章节中有单独的使用介绍。

[更全的python爬虫工具列表](http://python.jobbole.com/82633/)

## 1、HTTP

[http官方文档](https://docs.python.org/3.6/library/http.html)

http is a package that collects several modules for working with the HyperText Transfer Protocol:

- http.client is a low-level HTTP protocol client; for high-level URL opening use urllib.request.
- http.server contains basic HTTP server classes based on socketserver.
- http.cookies has utilities for implementing state management with cookies.
- http.cookiejar provides persistence of cookies.

http is also a module that defines a number of HTTP status codes and associated messages through the http.HTTPStatus enum.

大体来说就是http是一个包含client、server、cookies、cookiejar四个模块，且http本身也是关乎一些请求响应的状态码和相关信息的模块。client是一个低级的http客户端，更高级的去使用urllib.request；server有http服务器相关的基本功能；cookie用来管理请求或响应的cookie；cookiejar用来保存cookie文件。

最后总结：该库一般不直接使用，比较底层。

## 2、urllib

[urllib官方文档](https://docs.python.org/3.6/library/urllib.html)

urllib is a package that collects several modules for working with URLs:

- urllib.request for opening and reading URLs
- urllib.error containing the exceptions raised by urllib.request
- urllib.parse for parsing URLs
- urllib.robotparser for parsing robots.txt files

大体来说就是urllib是一个包含request、error、parse、robotparser四个模块，关乎网络资源请求的包。request模块用来发起网络资源请求；error模块用来在request网络资源过程中搜集异常报错；parse模块用来对url地址进行处理；robotparser模块用来解析robots.txt文件（未知）。

最后总结：该库作为python的内置标准库，满足一些通用的网络请求。

## 3、requests

[requests官方文档](http://docs.python-requests.org/en/latest/index.html)

requests基于urllib3，“Requests is an elegant and simple HTTP library for Python, built for human beings.”，号称为专门为人类设计的HTTP库。

最后总结：该库属于第三方扩展库，使用起来优雅简单大方。

## 4、lxml

[lxml官方文档](http://lxml.de/index.html)

lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.

其主要作用在xpath语法之上，这里要求使用者了解基本的html及xml等结构化语言的文档结构，然后利用xpath语法进行操作文档节点。

xpath是一门在xml文档中查找信息的语言。xpath可用来在xml文档中对元素和属性进行遍历。

[w3c关于xpath的基础教程](http://www.w3school.com.cn/xpath/index.asp)

最后总结：简单测试使用，有正则我不用它。

## 5、Beautiful Soup

[BeautifulSoup官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)

用python编写出来的包，速度较正则慢，胜在通俗易懂。

最后总结：简单测试使用，有正则我不用它。


















