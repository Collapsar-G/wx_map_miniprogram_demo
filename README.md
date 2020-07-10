# wx_map_miniprogram_demo
## 1. 开发环境

#### 1.1. 开发工具：

* 微信开发者工具；
* pycharm；

* * *

#### 1.2. 前端+后端框架：

* 前端： html + css + javascript + bootstrap；
* 后端： pyrhon + flask；
* 地图API： 高德API；

## 2. 微信小程序前端开发

#### 2.1. 功能需求和设计

##### 多用户

**功能说明：**
* 实现不同用户的区分，方便用户查看自己的记录信息；

**功能实现：**
* 用户在首次使用此小程序时，小程序会先获取用户的openid，并在数据库中查询此openid，若未查询到则将openid放入数据库中，若查询到则返回已经添加，将openid作为用户的唯一识别码。

#####  标记当前用户位置

**功能说明：**
* 用户在当前位置可以记录该位置，方便之后再次查看；

**功能实现：**
* 调用高德API获得用户标记时的位置信息，然后调用接口进行上传；

##### 路线规划

**功能说明：**
* 用户在选定起始点和目的地之后给出导航信息；

**功能实现：**
* 通过获取设置的出发地和目的地的位置信息，调用高德API返回路径规划信息，同时将出发地和目的地的信息通过调用接口上传到数据库，方便之后查询；

#####  历史路线规划查询

**功能说明：**
* 用户可以查看自己之前从某地到某地的路线规划；

**功能实现：**
* 从后台返回历史路线规划的记录，点击任意一条历史后会从后台返回所查看路径的信息，后调用高德API将其再次显示；

##### 查看附近热点

**功能说明：**
* 可以搜索查看想去的位置及周边建筑物的位置

**功能实现：**
* 调用高德API；

##### 查看当前天气

**功能实现：**
* 调用高德API；

* * *

#### 2.2. 页面设计
采用UI：colorui、weiui

##### 起始页
* **demo：**


![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/Image1.png)


* **代码：**“/pages/firstPage/“

##### 位置标记页

* **demo：**

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618113216.png)

* **代码：**“/pages/testPage/”

##### 路线规划
* **demo：**

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618113447.png)

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618113521.png)

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618113606.png)

* **代码：**
* “/pages/firstOfNavigation”；
* “/pages/endOfNavigation”；
* “/pages/navigation_car”；

##### 历史路线规划查询

* **demo：**

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618114153.png)

* **代码：** "/pages/myTrackPage/“


##### 附近热点页面

* **demo：**
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/Image.png)


* **代码：**“/pages/poi”


##### 天气页面




* **demo：**

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/Image3.png)



* **代码：**“/pages/weather”


* * *


## 3. 管理网站前端开发

#### 3.1. 功能需求与设计

##### 功能需求
* 管理员登录、注册；
* 位置管理；
* 路径规划记录管理；
* 管理员管理；
* 微信用户管理；

##### 页面设计
**UI：**BootStrap

* 登录页面：
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618120137.png)
* 注册页面：
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618120319.png)

* 首页：
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618120501.png)

* 位置记录页面：

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618120536.png)

* 轨迹管理页面：

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618120846.png)


* 用户管理页面：
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618121121.png)
* 管理员管理页面：

![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618121152.png)

* * *

## 4. 数据库设计
**环境：** mysql + navicat;

**结构：**![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618123756.png)

* * *

## 5. 后端开发
**后端采用 python + Flask 框架开发**
* 结构如下：
![](https://cdn.jsdelivr.net/gh/yexihe-jpg/image/img/20200618121523.png)

* 项目结构说明：
    
    1.   static: 存放css样式、js文件、图片等文件；
    2.   templates: 存放html文件；
    3.   venv: pythonk虚拟环境；
    4.   app.py: 与数据库链接、接口和Flask开发；
    5.   config.py: 数据库配置；
    6.   decorators.py: 对页面login函数封装，实现未登录跳转；


**具体代码详情见附件**

## 6 附件
[源码下载地址（非移动用户）](http://cloud.xiheye.club/map.zip)
[百度网盘下载地址（提取码：gla8） ](https://pan.baidu.com/s/1K5ik11JzOPubN1_9tU2DIw)
[博客地址](
https://xiheye.club/2020/06/18/wx-map/)
[Flask+BootStrap开发](
https://xiheye.club/2020/04/27/flask-use/)