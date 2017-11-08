
# python模块之os、sys

# 1、os

os模块是与操作系统交互的一个接口。没啥可说的，需要用直接查找使用就好，权限相关参考linux的文件属性。

	os.access(path, mode)           	# 检验权限模式   
	os.chdir(path)                  	# 改变当前工作目录
	os.chflags(path, flags)         	# 设置路径的标记为数字标记。
	os.chmod(path, mode)            	# 更改权限
	os.chown(path, uid, gid)        	# 更改文件所有者
	os.chroot(path)                 	# 改变当前进程的根目录
	os.close(fd)                    	# 关闭文件描述符 fd
	os.closerange(fd_low, fd_high)  	# 关闭所有文件描述符，从 fd_low (包含) 到 fd_high (不包含), 错误会忽略
	os.curdir                       	# 返回当前目录：（'.'）
	os.dup(fd)                      	# 复制文件描述符 fd
	os.dup2(fd, fd2)                	# 将一个文件描述符 fd 复制到另一个 fd2
	os.environ                      	# 获取系统环境变量
	os.fchdir(fd)                   	# 通过文件描述符改变当前工作目录
	os.fchmod(fd, mode)             	# 改变一个文件的访问权限，该文件由参数fd指定，参数mode是Unix下的文件访问权限。
	os.fchown(fd, uid, gid)         	# 修改一个文件的所有权，这个函数修改一个文件的用户ID和用户组ID，该文件由文件描述符fd指定。
	os.fdatasync(fd)                	# 强制将文件写入磁盘，该文件由文件描述符fd指定，但是不强制更新文件的状态信息。
	os.fdopen(fd[, mode[, bufsize]])  	# 通过文件描述符 fd 创建一个文件对象，并返回这个文件对象
	os.fpathconf(fd, name)          	# 返回一个打开的文件的系统配置信息。name为检索的系统配置的值，它也许是一个定义系统值的字符串，这些名字在很多标准中指定（POSIX.1, Unix 95, Unix 98, 和其它）。
	os.fstat(fd)                    	# 返回文件描述符fd的状态，像stat()。
	os.fstatvfs(fd)                 	# 返回包含文件描述符fd的文件的文件系统的信息，像 statvfs()
	os.fsync(fd)                    	# 强制将文件描述符为fd的文件写入硬盘。
	os.ftruncate(fd, length)        	# 裁剪文件描述符fd对应的文件, 所以它最大不能超过文件大小。
	os.getcwd()                     	# 返回当前工作目录
	os.getcwdu()                    	# 返回一个当前工作目录的Unicode对象
	os.isatty(fd)                   	# 如果文件描述符fd是打开的，同时与tty(-like)设备相连，则返回true, 否则False。
	os.lchflags(path, flags)        	# 设置路径的标记为数字标记，类似 chflags()，但是没有软链接
	os.lchmod(path, mode)           	# 修改连接文件权限
	os.lchown(path, uid, gid)       	# 更改文件所有者，类似 chown，但是不追踪链接。
	os.link(src, dst)               	# 创建硬链接，名为参数 dst，指向参数 src
	os.listdir(path)                	# 返回path指定的文件夹包含的文件或文件夹的名字的列表。
	os.lseek(fd, pos, how)          	# 设置文件描述符 fd当前位置为pos, how方式修改: SEEK_SET 或者 0 设置从文件开始的计算的pos; SEEK_CUR或者 1 则从当前位置计算; os.SEEK_END或者2则从文件尾部开始. 在unix，Windows中有效
	os.lstat(path)                  	# 像stat(),但是没有软链接
	os.linesep                      	# 当前平台使用的行终止符，win下为"\t\n",Linux下为"\n"
	os.major(device)                	# 从原始的设备号中提取设备major号码 (使用stat中的st_dev或者st_rdev field)。
	os.makedev(major, minor)        	# 以major和minor设备号组成一个原始设备号
	os.makedirs(path[, mode])       	# 递归文件夹创建函数。像mkdir(), 但创建的所有intermediate-level文件夹需要包含子文件夹。
	os.minor(device)                	# 从原始的设备号中提取设备minor号码 (使用stat中的st_dev或者st_rdev field )。
	os.mkdir(path[, mode])          	# 以数字mode的mode创建一个名为path的文件夹.默认的 mode 是 0777 (八进制)。
	os.mkfifo(path[, mode])         	# 创建命名管道，mode 为数字，默认为 0666 (八进制)
	os.mknod(filename[, mode=0600, device])  # 创建一个名为filename文件系统节点（文件，设备特别文件或者命名pipe）。
	os.open(file, flags[, mode])    	# 打开一个文件，并且设置需要的打开选项，mode参数是可选的
	os.openpty()                    	# 打开一个新的伪终端对。返回 pty 和 tty的文件描述符。
	os.pathconf(path, name)         	# 返回相关文件的系统配置信息。
	os.pathsep                      	# 用于分割文件路径的字符串
	os.pardir                       	# 获取当前目录的父目录字符串名：('..')
	os.pipe()                       	# 创建一个管道. 返回一对文件描述符(r, w) 分别为读和写
	os.popen(command[, mode[, bufsize]])  # 从一个 command 打开一个管道
	os.path.abspath(path)           	# 返回path规范化的绝对路径
	os.path.split(path)             	# 将path分割成目录和文件名二元组返回
	os.path.dirname(path)           	# 返回path的目录。其实就是os.path.split(path)的第一个元素
	os.path.basename(path)          	# 返回path最后的文件名。如何path以／或\结尾，那么就会返回空值。即os.path.split(path)的第二个元素
	os.path.exists(path)            	# 如果path存在，返回True；如果path不存在，返回False
	os.path.isabs(path)             	# 如果path是绝对路径，返回True
	os.path.isfile(path)            	# 如果path是一个存在的文件，返回True。否则返回False
	os.path.isdir(path)             	# 如果path是一个存在的目录，则返回True。否则返回False
	os.path.join(path1[, path2[, ...]]) # 将多个路径组合后返回，第一个绝对路径之前的参数将被忽略
	os.path.getatime(path)          	# 返回path所指向的文件或者目录的最后存取时间
	os.path.getmtime(path)          	# 返回path所指向的文件或者目录的最后修改时间
	os.name                         	# 字符串指示当前使用平台。win->'nt'; Linux->'posix'
	os.read(fd, n)                  	# 从文件描述符 fd 中读取最多 n 个字节，返回包含读取字节的字符串，文件描述符 fd对应文件已达到结尾, 返回一个空字符串。
	os.readlink(path)               	# 返回软链接所指向的文件
	os.remove(path)                 	# 删除路径为path的文件。如果path 是一个文件夹，将抛出OSError; 查看下面的rmdir()删除一个 directory。
	os.removedirs(path)             	# 递归删除目录。若目录为空，则删除，并递归到上一级目录，如若也为空，则删除，依此类推
	os.rename(src, dst)             	# 重命名文件或目录，从 src 到 dst
	os.renames(old, new)            	# 递归地对目录进行更名，也可以对文件进行更名。
	os.rmdir(path)                  	# 删除path指定的空目录，如果目录非空，则抛出一个OSError异常。
	os.sep                          	# 操作系统特定的路径分隔符，win下为"\\",Linux下为"/"
	os.stat(path)                   	# 获取path指定的路径的信息，功能等同于C API中的stat()系统调用。
	os.stat_float_times([newvalue]) 	# 决定stat_result是否以float对象显示时间戳
	os.statvfs(path)                	# 获取指定路径的文件系统统计信息
	os.symlink(src, dst)            	# 创建一个软链接
	os.system("bash command")       	# 运行shell命令，直接显示
	os.tcgetpgrp(fd)                	# 返回与终端fd（一个由os.open()返回的打开的文件描述符）关联的进程组
	os.tcsetpgrp(fd, pg)            	# 设置与终端fd（一个由os.open()返回的打开的文件描述符）关联的进程组为pg。
	os.tempnam([dir[, prefix]])     	# 返回唯一的路径名用于创建临时文件。
	os.tmpfile()                    	# 返回一个打开的模式为(w+b)的文件对象 .这文件对象没有文件夹入口，没有文件描述符，将会自动删除。
	os.tmpnam()                     	# 为创建一个临时文件返回一个唯一的路径
	os.ttyname(fd)                  	# 返回一个字符串，它表示与文件描述符fd 关联的终端设备。如果fd 没有与终端设备关联，则引发一个异常。
	os.unlink(path)                 	# 删除文件路径
	os.utime(path, times)           	# 返回指定的path文件的访问和修改的时间。
	os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])  # 输出在文件夹中的文件名通过在树中游走，向上或者向下。
	os.write(fd, str)               	# 写入字符串到文件描述符 fd中. 返回实际写入的字符串长度

# 2、sys

	sys.argv   						# 命令行参数List，第一个元素是程序本身路径 script.py arg1 arg2 arg3 
	sys.modules 					# 返回系统导入的模块字段，key是模块名，value是模块
	sys.exit(n)        				# 退出程序，正常退出时exit(0)
	sys.modules.keys() 				# 返回所有已经导入的模块名
	sys.modules.values() 			# 返回所有已经导入的模块
	sys.exc_info()     				# 获取当前正在处理的异常类,exc_type、exc_value、exc_traceback		# 当前处理的异常详细信息
	sys.hexversion     				# 获取Python解释程序的版本值，16进制格式如：0x020403F0
	sys.version        				# 获取Python解释程序
	sys.api_version    				# 解释器的C的API版本
	sys.version_info				# (major=3, minor=6, micro=2, releaselevel='final', serial=0)
	‘final’表示最终,也有’candidate’表示候选，serial表示版本级别，是否有后继的发行
	sys.displayhook(value)      	# 如果value非空，这个函数会把他输出到sys.stdout，并且将他保存进__builtin__._.指在python的交互式解释器里，’_’ 代表上次你输入得到的结果，hook是钩子的意思，将上次的结果钩过来
	sys.getdefaultencoding()    	# 返回当前你所用的默认的字符编码格式
	sys.getfilesystemencoding() 	# 返回将Unicode文件名转换成系统文件名的编码的名字
	sys.setdefaultencoding(name)	# 用来设置当前默认的字符编码，如果name和任何一个可用的编码都不匹配，抛出 LookupError，这个函数只会被site模块的sitecustomize使用，一旦别site模块使用了，他会从sys模块移除
	sys.builtin_module_names    	# Python解释器导入的模块列表
	sys.executable              	# Python解释程序路径
	sys.getwindowsversion()     	# 获取Windows的版本
	sys.copyright      				# 记录python版权相关的东西
	sys.byteorder      				# 本地字节规则的指示器，big-endian平台的值是’big’,little-endian平台的值是’little’
	sys.exc_clear()    				# 用来清除当前线程所出现的当前的或最近的错误信息
	sys.exec_prefix    				# 返回平台独立的python文件安装的位置
	sys.stderr         				# 错误输出
	sys.stdin          				# 标准输入
	sys.stdout         				# 标准输出
	sys.platform       				# 返回操作系统平台名称
	sys.path           				# 返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值
	sys.maxunicode     				# 最大的Unicode值
	sys.maxint         				# 最大的Int值
	sys.version        				# 获取Python解释程序的版本信息

exit is a helper for the interactive shell - sys.exit is intended for use in programs.



