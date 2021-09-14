<div align="center">
<h1 align="center">
MoGuDing-Auto
</h1>
</div>


## 项目简介

请不要使用本开源程序在服务器上(包括GitHub的Actions)跑！！！

请不要使用本开源程序在服务器上跑(包括GitHub的Actions)！！！

请不要使用本开源程序在服务器上跑(包括GitHub的Actions)！！！


WEB版本：[点击进入](http://www.mgdauto.ml/) 

蘑菇丁每日上下班打卡，支持多账户，指定地区，后续将添加日报周报等功能


## 项目功能
***当前版本:  20210914***  

1. 修改为可本地执行脚本  

***当前版本:  20210826***  

1. 定时上下班自动打卡
2. 支持指定地区
3. 支持多用户
4. 支持多种推送方式
5. 支持自定义设备


## 更新日志
### 2021-08-26:

1. 自定义设备
2. 修复死循环

### 2021-08-01:

1. 定时上下班自动打卡
2. 支持指定地区
3. 支持多用户


微信交流群:

<img src="https://img14.360buyimg.com/ddimg/jfs/t1/201870/16/5638/173507/6138b1a1E39d27fb4/449af85e750378ce.jpg" style="zoom:33%;" />


## 使用说明

### 系统级别计划任务方式

1. **GIT Clone 本项目**

2. ** 修改MoGuDing.py中`informations `内容**

   ```python
       informations = [
       {
           "phone":"手机号",
           "password":"密码",
           "token":"",
           "country":"中国",
           "province":"北京",
           "city":"丰台区",
           "address":"具体地址",
           "latitude":"39.939043",
           "longitude":"116.333059"
       }
       ]
   ```

- 例子（使用时请删除注释！！！）

  -  一个账户：

    ```json
    [
      {
        "phone": "你的手机号", # 账号
        "password": "你的密码", # 密码
        "device": "Android", # 设备  Android或者iOS
        "token": "123", #抓包获取token，在请求头中为 authorization
        "country": "中国", # 国家
        "province": "江西省", # 省份
        "city": "萍乡市", # 城市  
        "address": "中国江西省萍乡市芦溪县东南边境", # 详细地址
        "latitude": "27.467943", # 纬度
        "longitude": "114.17542" # 经度
      }

    ]
    ```

  -  多个账户：

    ```json
    [
      {
        "phone": "你的手机号", # 账号
        "password": "你的密码", # 密码
        "device": "Android", # 设备  Android或者iOS
        "token": "", #抓包获取token，在请求头中为 authorization，不会抓包请留空，不要删除
        "country": "中国", # 国家
        "province": "江西省", # 省份
        "city": "萍乡市", # 城市  
        "address": "中国江西省萍乡市芦溪县东南边境", # 详细地址
        "latitude": "27.467943", # 纬度
        "longitude": "114.17542" # 经度
      },
      {
        "phone": "你的手机号", # 账号
        "password": "你的密码", # 密码
        "device": "Android", # 设备  Android或者iOS
        "token": "123", #抓包获取token，在请求头中为 authorization
        "country": "中国", # 国家
        "province": "江西省", # 省份
        "city": "萍乡市", # 城市  
        "address": "中国江西省萍乡市芦溪县东南边境", # 详细地址
        "latitude": "27.467943", # 纬度
        "longitude": "114.17542" # 经度
      }
    
    ]
    ```

经纬度查询推荐使用高德：https://lbs.amap.com/tools/picker

4. 修改为本地可执行版本 可在有Python3的环境中运行，添加自动任务即可

```bash
10 6,18 * * * 0-7    python3 绝对路径/MoGuDing.py >> /opt/mogu/pu.log # Linux 计划任务 
```





## 为什么需要token？

### 区别：

无token：每次都是重新登录，会导致app上的账户被挤下线

有token：每次使用token登录，不影响app的账户在线状态

### 订阅执行结果

1. 修改钉钉机器人webhook即可

   ```python
   web_url = "https://oapi.dingtalk.com/robot/send?access_token=******************************(token)"
   ```

2. 若不需要通知功能需要注释此行

   ```python
   ding_push_message(INFORMATION["phone"],TITLE,MESSAGE)
   ```


<img src="docs/IMG/ysxg1.jpg" style="zoom:33%;" />
