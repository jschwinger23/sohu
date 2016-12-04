###Sohu
采用Actor模式来进行多线程爬虫，分为CrawlingActor和ParsingActor两个模式，维护了两个线程安全队列进行线程间通信。

#### 依赖
数据抓取依赖requests模块，数据清洗依赖lxml模块。
可使用以下命令进行安装：

	sudo pip install -r requirements.txt



#### 配置
可以在```sohu/conf/config.py```中配置两个Actor的线程数，默认抓取线程为10，解析线程为1.
#### 运行
通过运行sohu/bin/start.sh就可以启动进程

	sh start.sh
	
将会在终端打印出当前运行的队列中的任务数量（大概值，计数时没有加线程锁）。

若不希望输出信息到终端，可以使用后台运行：

	nohup sh start.sh &> /dev/null &
	
#### 输出
输出的日志将在```sohu/log```中出现，包括了不可达链接的url、时间、错误状态。

#### 优化
在ParsingActor内部维护了一个集合，记录已经访问过的url，防止同一url被多次访问。

所有的url都被切掉了查询部分和标签部分，也就是说以?与#字符之前的url路径进行处理和判断。