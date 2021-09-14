import datetime
import time
import json
import pytz
import requests
import urllib3
import NoticePush
import GlobalVariable

urllib3.disable_warnings()

web_url = "https://oapi.dingtalk.com/robot/send?access_token=******************************(token)"

MESSAGE = ""
TITLE = ""
UPDATE_INFO = ""
FAILURES_Count = 0

# 登录
def login():
    global MESSAGE,FAILURES_Count
    if INFORMATION.get("phone") is None or INFORMATION.get("phone").strip() == '':
        MESSAGE += "\n手机号为空"
        return

    if INFORMATION.get("password") is None or INFORMATION.get("password").strip() == '':
        MESSAGE += "\n密码为空"
        return

    requestsBody = {
        "phone": INFORMATION["phone"],
        "password": INFORMATION["password"],
        "loginType": INFORMATION.get("device","android"),
        "uuid": ""
    }

    url = GlobalVariable.BASE_URL + "session/user/v1/login"

    response = requests.post(url=url, headers=GlobalVariable.headers, data=json.dumps(requestsBody), verify=False)
    responseJson = response.json()
    if responseJson["code"] != 200:
        msg = responseJson["msg"]
        FAILURES_Count+=1
        print(msg)
        return

    data = responseJson["data"]
    #print(data)
    nikeName = data["nikeName"]
    userId = data["userId"]
    token = data["token"]
    userType = data["userType"]
    moguNo = data["moguNo"]

    newData = {
        "nikeName": nikeName,
        "userId": userId,
        "token": token,
        "userType": userType,
        "moguNo": moguNo
    }

    INFORMATION.update(newData)

    # 登录后显示的信息
#     print(nikeName)
#     print(userId)
#     print(token)
#     print(userType)


# 获取基本信息
def getUserInfo():
    global MESSAGE
    GlobalVariable.headers.update(
        {"authorization": INFORMATION.get("token"), "rolekey": "student"}
    )

    requestsBody = {}
    url = GlobalVariable.BASE_URL + "usercenter/user/v1/info"

    response = requests.post(url=url, headers=GlobalVariable.headers, data=json.dumps(requestsBody), verify=False)
    responseJson = response.json()
    if responseJson["code"] != 200:
        MESSAGE = responseJson["msg"]
        print(responseJson["msg"])
        if "token" in MESSAGE or "失效" in MESSAGE:
            if FAILURES_Count >= 3:
                print("账号或密码错误...")
                return
            # token失效尝试重新登录
            print("token失效尝试重新登录...")
            login()
            getPlanByStu()
    else:
        data = responseJson["data"]
        nikeName = data["nikeName"]
        userId = data["userId"]
        userType = data["userType"]
        moguNo = data["moguNo"]

        newData = {
            "nikeName": nikeName,
            "userId": userId,
            "userType": userType,
            "moguNo": moguNo
        }
        INFORMATION.update(newData)


# 获取计划
def getPlanByStu():
    global TITLE, MESSAGE
    # 没有token则重新登录
    if INFORMATION.get("token") is None or INFORMATION.get("token").strip() == '':
        login()

    if INFORMATION.get("userId") is None or INFORMATION.get("userId").strip() == '':
        # 获取基本信息
        getUserInfo()

    # 获取sign
    paramString = ""
    parameterSign = {
        "userId": INFORMATION["userId"],
        "paramString": paramString,
        "moguNo": INFORMATION["moguNo"],
        "userType": INFORMATION["userType"],
    }

    sign = getSign("getPlanByStuSign",parameterSign)

    GlobalVariable.headers.update(
        {"authorization": INFORMATION.get("token"), "rolekey": "student", "sign": sign}
    )

    requestsBody = {
        "state": paramString
    }

    url = GlobalVariable.BASE_URL + "practice/plan/v3/getPlanByStu"

    response = requests.post(url=url, headers=GlobalVariable.headers, data=json.dumps(requestsBody), verify=False)
    responseJson = response.json()
    if responseJson["code"] != 200:
        MESSAGE = responseJson["msg"]
        print(responseJson["msg"])
        if "token" in MESSAGE or "失效" in MESSAGE:
            if FAILURES_Count >= 3:
                print("账号或密码错误...")
                return
            # token失效尝试重新登录
            print("token失效尝试重新登录...")
            login()
            getPlanByStu()
    else:
        dataList = responseJson["data"]
        data = dataList[len(dataList) - 1]
        planName = data["planName"]
        planId = data["planId"]

        dataNew = {
            "planName": planName,
            "planId": planId,
        }

        INFORMATION.update(dataNew)

        # 显示学校名称和id
        # print(planName)
        # print(planId)

# 获取sign
def getSign(url,parameter):
    global MESSAGE
    try:
        response = requests.post(url=GlobalVariable.SIGN_URL + url,headers=GlobalVariable.headers, data=json.dumps(parameter))
        responseJson = response.json()
        if responseJson["code"] == 200 :
            return responseJson["sign"]
        else:
            MESSAGE += "\n%s" % responseJson["msg"]
            print(responseJson["msg"])
            return None
    except Exception as e:
        MESSAGE += "\nAPI访问出错！"


def ding_push_message(phone,titles,messages):
    #iphon = 19943466021
    ding_data = {}
    ding_data['msgtype'] = 'markdown'

    markdown = {}
    markdown['title'] = "蘑菇钉提醒"
    markdown[
        'text'] = "#### 签到提醒:@{0} \n {1} \n  \n {2} ".format(phone,TITLE,MESSAGE)

    ding_data['markdown'] = markdown
    ding_data['at'] = {"atMobiles": [phone], "isAtAll": False}

    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    # 构建请求数据
    """
    message = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": False
        }
    }"""
    # 对请求的数据进行json封装
    #message_json = json.dumps(message)
    # 发送请求
    #info = requests.post(url=web_url, data=message_json, headers=header)
    info = requests.post(url=web_url, data=json.dumps(ding_data), headers=header)
    # 打印返回的结果
    print(info.text)

# 上下班打卡签到
def signIn(type):
    global TITLE, MESSAGE

    if INFORMATION.get("token") is None or INFORMATION.get("token").strip() == '':
        print("没有获取到token，请检查是否正确登录！")
        return

    if INFORMATION.get("planId") is None or INFORMATION.get("planId").strip() == '':
        print("没有获取到planId，请检查是否正确指定签到对象！")
        MESSAGE = "没有获取到planId，请检查是否正确指定签到对象！"
        return

    typeStr = "START" if type == 1 else "END"

    parameterSign = {
        "userId": INFORMATION["userId"],
        "moguNo": INFORMATION["moguNo"],
        "address": INFORMATION["address"],
        "device": INFORMATION.get("device","Android"),
        "planId": INFORMATION["planId"],
        "type": typeStr,
        "latitude": INFORMATION["latitude"],
        "longitude": INFORMATION["longitude"]
    }

    sign = getSign("getClockInSign",parameterSign)
    GlobalVariable.headers.update({"authorization": INFORMATION.get("token"), "rolekey": "student", "sign": sign})

    requestsBody = {
        "country": INFORMATION["country"],
        "address": INFORMATION["address"],
        "province": INFORMATION["province"],
        "city": INFORMATION["city"],
        "latitude": INFORMATION["latitude"],
        "description": "",
        "planId": INFORMATION["planId"],
        "type": typeStr,
        "device": INFORMATION.get("device","Android"),
        "longitude": INFORMATION["longitude"]
    }

    url = GlobalVariable.BASE_URL + "attendence/clock/v2/save"

    response = requests.post(url=url, headers=GlobalVariable.headers, data=json.dumps(requestsBody), verify=False)
    responseJson = response.json()

    if responseJson["code"] != 200:
        msg = responseJson["msg"]
        MESSAGE = msg
        print(msg)
    else:
        createTime = responseJson["data"]["createTime"]
        TITLE = "%s，%s打卡成功!" % (INFORMATION["nikeName"], "上班" if typeStr == "START" else "下班")
        MESSAGE = "  目标:%s\n\n  打卡时间:%s \n\n  打卡地点:%s" % (INFORMATION["planName"], createTime, INFORMATION['address'])


# 检测更新
def checkForUpdates():
    global UPDATE_INFO
    #remote_address = "https://raw.githubusercontent.com/leifengwl/MoGuDing-Auto/main/config.ini"
    remote_address = "https://endpoint.fastgit.org/https://github.com/leifengwl/MoGuDing-Auto/blob/main/config.ini"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    res = requests.get(url=remote_address, headers=headers,verify=False)
    if res.status_code == 200:
        res_json = res.json()
        if res_json["version"] != GlobalVariable.version:
            UPDATE_INFO = "**MoGuDing-Auto更新提醒:**" \
                          + "\n最新版：" + res_json["version"] \
                          + "  当前版本：" + GlobalVariable.version \
                          + "\n " + res_json["updateLog"] + "\n"
        else:
            print("欢迎使用MoGuDing-Auto!")

        UPDATE_INFO += "> " + res_json["announcement"] + " \n\n"
    else:
        print("checkForUpdate failed!")


# 主程序
def main():
    global INFORMATION, TITLE, MESSAGE
#    pw = open('MoGuDing.json','r',encoding='utf8')
#    personal_information  = pw
#    pw.close
#    print(personal_information)
#    if GlobalVariable.PERSONAL_INFORMATION is None or GlobalVariable.PERSONAL_INFORMATION.strip() == '':
#    print("未获取到环境变量'PERSONAL_INFORMATION'，执行中止")
      #  return

#    personal_information = GlobalVariable.PERSONAL_INFORMATION
    # 检查更新
    checkForUpdates()
#    informations = json.loads(personal_information)
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

    for information in informations:
        INFORMATION = information

        # 开始签到
        # login()
        getPlanByStu()

        hourNow = datetime.datetime.now(pytz.timezone('PRC')).hour
        #9点前为上班打卡   1为上班   0为下班
        if hourNow <= 9:
            signIn(1)
            print(TITLE+"\n"+MESSAGE+"\n"+"=====================")
        # 17点后为下班打卡
        elif hourNow >= 17:
            signIn(0)
            print(TITLE+"\n"+MESSAGE+"\n"+"=====================")

        MESSAGE = UPDATE_INFO + MESSAGE

        # 开始推送
        if TITLE == "":
            TITLE = "%s,打卡失败!" % (INFORMATION["nikeName"])
        #NoticePush.server_push(TITLE, MESSAGE)
        #NoticePush.push_plus(TITLE, MESSAGE)
        #NoticePush.telegram_bot(TITLE, MESSAGE)
        #NoticePush.bark(TITLE, MESSAGE)
        #NoticePush.enterprise_wechat(TITLE, MESSAGE)
        #msg = 
        ding_push_message(INFORMATION["phone"],TITLE,MESSAGE)
        # 清空变量
        INFORMATION = {}
        MESSAGE = ""
        TITLE = ""
        time.sleep(5)
    print("=================================")

if __name__ == '__main__':
    main()
