<h3><a href="http://hamilton.duapp.com/">http://hamilton.duapp.com/的源码</a></h3>

基于Python的Flask框架开发，使用SQLAlchemy作为ORM。前端基于Bootstrap开发，其中发布博客页面使用的是UEditor富文本编辑器
<h4>文件说明</h4>
<h4>app.conf</h4>
BAE的相关配置，主要设置静态文件的访问方法
<h4>index.py</h4>
程序的入口，初始化数据库连接，设置WSGIApplication等
<h4>intro.py</h4>
首页，标签页，关于页等页面的Python代码
<h4>admin目录</h4>
管理员登录，发布博客，编辑博客等页面的Python代码
<h4>dao目录</h4>
数据库访问接口
<h4>database目录</h4>
数据库连接的相关设置，比如连接池的时间等
<h4>model目录</h4>
基本对象，有一些映射到了数据库的关系表
<h4>static目录</h4>
静态文件目录，比如一些js，css文件
<h4>templates目录</h4>
Jinja2模板文件
<h4>utils目录</h4>
一些工具类，比如提取HTML文本，取出HTML背景颜色等



