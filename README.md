# README

#### 配置环境：

```py
pip install requests,bs4,fake_useragent,queue
```

#### 代理ip爬取的使用方法：

```py
# 在文件的目录打开命令窗口 参数t是设置线程的数量
python ip_proxy -t 10
```

爬取的结果

![image-20221031191428297](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031191428297.png)

![image-20221031191440808](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031191440808.png)

默认爬取的网址是https://www.89ip.cn/ ，如需爬取其他网站的代理ip只需修改

![image-20221031190342671](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031190342671.png)

![image-20221031190416909](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031190416909.png)

改为对应想要爬取的数据



#### 子域名收集的使用方法：

```py
# -d 要收集的域名 -t 线程的数量
# 默认爬取的网址是https://crt.sh
python sub_domain.py -d wuyecao.net -t 10
```

运行结果：

![image-20221031191711680](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031191711680.png)

![image-20221031191724395](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031191724395.png)

生成的文件都在当前各自的当前目录下

子域名收集还可以根据自己的需求添加相应的模块

![image-20221031191944340](C:\Users\15501\AppData\Roaming\Typora\typora-user-images\image-20221031191944340.png)

后续会持续优化！！！