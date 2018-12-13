
# chooseCourseHelper
选课助手，获取开课列表及志愿填报信息，通过简单的数据库操作即可进行选课系统没有的高级筛选功能。也可以设计算法自动帮你安排课程。

# 食用方法
下载本项目
```shell
$ git clone git@github.com:jcq15/chooseCourseHelper.git
```
然后在目录下新建一个文件`mytoken.py`，内容如下：
```text
username = 'jcq15'
pswd = r'12345678'
```
其中`'jcq15'`改为你的用户名，`'12345678'`改为密码，然后执行
```shell
$ python getHtml.py
$ python toxls.py
```
文件`./output/courses.csv`为所有课程列表

# 开发过程记录
选课系统的筛选功能有限，选课时如果有更多高级功能会更方便。例如过滤掉已经被占用的时间，或者根据填报志愿情况计算当前选中的概率。类似的需求还有很多。既然选课系统没有实现，只有自己把数据搞下来。

基本思路很简单，使用爬虫获取课程列表界面的源码，然后分析文本提取出信息写入文件。

## 获取页面源码
### selenium库
学校的选课系统是在后台采用js获取数据，用传统的爬虫有些麻烦。于是我把目光转向了selenium库。利用selenium库可以方便地在python中使用代码控制Chrome、Firefox等浏览器进行操作。更加感人的是Firefox有一个Headless模式，没有图形界面只有后台程序，两者配合简直就是为爬虫而生的。需要安装一下相应的webdriver，详见https://github.com/SeleniumHQ/selenium

这里使用Firefox的headless模式操作

```python
from selenium import webdriver
import mytoken as token

# headless mode
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
```
这就配置成功了，然后启动
```python
browser = webdriver.Firefox(options = options)
```
### 进行浏览器操作
#### 登录
我们要操纵浏览器登录，首先要定位到用户名和密码的输入框。这里有一个很强大的功能`find_element_by`，可以通过元素的id，name等信息进行定位。

打开登录页面 academic.tsinghua.edu.cn，在用户名处右键-审查元素可以看到
```html
<input class="nrb left yahei" type="text" placeholder="用户名" name="userName">
```
它的`name`为`'username'`，于是可以这样定位元素

```python
browser.find_element_by_name('userName')
```
使用`send_keys()`方法向输入框输入内容，`click()`方法点击按钮。登录部分的代码如下：
```python
# login
browser.get(r'http://academic.tsinghua.edu.cn/')
browser.find_element_by_name('userName').send_keys(token.username)
browser.find_element_by_name('password').send_keys(token.pswd)
browser.find_element_by_id('logining').click()
```
#### 浏览开课目录
现在只要遍历开课目录的每一页，把html文件保存下来就可以了，这部分和上面类似，直接放代码
```python
# enter choose lesson page
browser.get(r'http://zhjw.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do?m=kkxxSearch&p_xnxq=2018-2019-2')
with open('pages/page1.html', 'w') as f:
    f.write(browser.page_source)

# all pages
pages = 2
total_pages = 226
for i in range(2,total_pages+1):
    browser.find_element_by_id('nextpage').click()
    with open('pages/page%s.html'%pages, 'w') as f:
        f.write(browser.page_source)
    print('%ssucceed!'%pages)
    pages = pages + 1
```
这样所有开课信息就被保存在`pages`文件夹下的226个`.html`文件中了。

## 提取信息


