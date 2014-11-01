chronicle
=========

历史事件浏览，数据来自维基百科。使用了TimelineJS控件和Python。

可以访问我预先部署的
http://1.chronicletimeline.sinaapp.com/

安装和启动
Windows
  安装Python，在这里https://www.python.org/downloads/windows/下载安装。
  解压缩dist.zip到指定目录，例如：chronicle。
  打开命令窗口，进入chronicle目录，输入 python -m SimpleHTTPServer 8899 回车。
  打开浏览器，在地址栏中输入：http://localhost:8899  回车。


想自己生成缓存
  下载code/http.py,code/cache.py
  按照cache.py中的说明运行即可。
  注意：维基百科的网站可能做了控制，一次不可能下载完成，多试几次就好。


Have fun!

