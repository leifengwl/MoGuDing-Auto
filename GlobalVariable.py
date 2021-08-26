import os

# 全局参数
# API
BASE_URL = "https://api.moguding.net:9000/"
SIGN_URL = "http://mgd.lftools.ltd:2658/api/"

headers = {
        "Host": "api.moguding.net:9000",
        "accept-language": "zh-CN,zh;q=0.8",
        "user-agent": "Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI 6 Build/PKQ1.190118.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
        "sign": "",
        "authorization": "",
        "rolekey": "",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "cache-control": "no-cache"
}

# 当前版本
version = "20210826"

# 环境变量
PERSONAL_INFORMATION = os.environ.get("PERSONAL_INFORMATION",'')

SERVERPUSHKEY = os.environ.get("SERVERPUSHKEY", "")  # Server酱推送
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")  # Telegram推送服务Token
TG_USER_ID = os.environ.get("TG_USER_ID", "")  # Telegram推送服务UserId
BARK = os.environ.get("BARK", "")  # bark消息推送服务,自行搜索; secrets可填;形如jfjqxDx3xxxxxxxxSaK的字符串
PUSHPLUS = os.environ.get("PUSHPLUS", "")  # PUSHPLUS消息推送Token
ACCESSTOKEN = os.environ.get("ACCESSTOKEN", "")  # 企业微信access_token     获取地址:https://work.weixin.qq.com/api/doc/90000/90135/91039
CORPID = os.environ.get("CORPID", "")  # 企业ID  （如果已经填写ACCESSTOKEN  则无需填写这个）
CORPSECRET = os.environ.get("CORPSECRET", "")  # 应用的凭证密钥  （如果已经填写ACCESSTOKEN  则无需填写这个）
TOUSER = os.environ.get("TOUSER", "")  # touser指定接收消息的成员  默认为全部
AGENTID = os.environ.get("AGENTID", "")  # agentid企业应用的id
THUMB_MEDIA_ID = os.environ.get("THUMB_MEDIA_ID", "") #企业微信素材库图片id
AUTHOR = os.environ.get("AUTHOR", "") #企业微信文章作者


