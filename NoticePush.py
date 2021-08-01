import requests
import json
import GlobalVariable
import markdown

# Server酱推送
def server_push(text, desp):
    if not GlobalVariable.SERVERPUSHKEY:
        print("Server酱推送的SERVERPUSHKEY未设置!!")
        return
    server_push_url = "https://sc.ftqq.com/" + GlobalVariable.SERVERPUSHKEY + ".send"
    str = GlobalVariable.SERVERPUSHKEY[0:3]
    if "SCT" == str:
        server_push_url = "https://sctapi.ftqq.com/" + GlobalVariable.SERVERPUSHKEY + ".send"
    params = {
        "text": text,
        "desp": desp
    }
    res = requests.post(url=server_push_url, data=params)
    if res.status_code == 200:
        print("Server酱推送成功!")
    else:
        print("Server酱推送失败!")

# pushplus推送
def push_plus(title, content):
    if not GlobalVariable.PUSHPLUS:
        print("pushplus推送的PUSHPLUS未设置!!")
        return
    push_plus_url = "http://www.pushplus.plus/send"
    params = {
        "token": GlobalVariable.PUSHPLUS,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    res = requests.post(url=push_plus_url, params=params)
    if res.status_code == 200:
        print("pushplus推送成功!")
    else:
        print("pushplus推送失败!")

# Bark推送
def bark(title, content):
    if not GlobalVariable.BARK:
        print("bark服务的bark_token未设置!!")
        return
    res = requests.get(
        f"""https://api.day.app/{GlobalVariable.BARK}/{title}/{content}""")
    if res.status_code == 200:
        print("bark推送成功!")
    else:
        print("bark推送失败!")

# tg推送
def telegram_bot(title, content):
    if not GlobalVariable.TG_BOT_TOKEN or not GlobalVariable.TG_USER_ID:
        print("Telegram推送的TG_BOT_TOKEN或者TG_USER_ID未设置!!")
        return
    send_data = {"chat_id": GlobalVariable.TG_USER_ID, "text": title + '\n\n' + content, "disable_web_page_preview": "true"}
    res = requests.post(
        url='https://api.telegram.org/bot%s/sendMessage' % (GlobalVariable.TG_BOT_TOKEN), data=send_data)
    if res.status_code == 200:
        print("telegram推送成功!")
    else:
        print("telegram推送失败!")

# 企业微信推送
def enterprise_wechat(title, content):
    html = markdown.markdown(content)
    access_token = ""
    if not GlobalVariable.ACCESSTOKEN:
        if not GlobalVariable.CORPID or not GlobalVariable.CORPSECRET or not GlobalVariable.TOUSER or not GlobalVariable.AGENTID:
            print("企业微信应用消息推送的变量未设置或未设置完全!!")
            return
        res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={GlobalVariable.CORPID}&corpsecret={GlobalVariable.CORPSECRET}")
        access_token = res.json().get("access_token", False)
    else:
        if not GlobalVariable.TOUSER or not GlobalVariable.AGENTID:
            print("企业微信应用消息推送的变量未设置或未设置完全!!")
            return
        access_token = GlobalVariable.ACCESSTOKEN
    if not GlobalVariable.THUMB_MEDIA_ID:
        data = {
            "touser": GlobalVariable.TOUSER,
            "agentid": GlobalVariable.AGENTID,
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        res = requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}",
                            data=json.dumps(data)).json()
        errmsg = res["errmsg"]
        if errmsg == "ok":
            print("企业微信应用消息推送成功!")
        else:
            print("企业微信应用消息失败!错误信息:"  + errmsg)
    else:
        data = {
            "touser": GlobalVariable.TOUSER,
            "agentid": GlobalVariable.AGENTID,
            "msgtype": "mpnews",
            "mpnews": {
                    "articles" : [
                    {
                    "title" : title,
                    "thumb_media_id" : GlobalVariable.THUMB_MEDIA_ID ,
                    "author" : GlobalVariable.AUTHOR ,
                    "content_source_url": "",
                    "content" : html,
                    "digest": content
                    }
                    ]
            }
        }
        res = requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}",
                            data=json.dumps(data)).json()
        errmsg = res["errmsg"]
        if errmsg == "ok":
            print("企业微信应用消息推送成功!")
        else:
            print("企业微信应用消息失败!错误信息:"  + errmsg)
