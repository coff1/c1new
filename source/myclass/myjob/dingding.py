import time
import hmac
import hashlib
import base64
import urllib.parse
from ..myrequests import myrequests
from source.config import config
from source.myclass.mylog import mylog



def send_message_to_dingding(message):
    # 没配置会引起异常而跳过
    try:
        timestamp = str(round(time.time() * 1000))
        secret = config.secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        webhook = config.webhook
        url=webhook+'&timestamp={}&sign={}'.format(timestamp,sign)
        headers = {
            'Content-Type': 'application/json',
        }

        content = {
            "msgtype": "text",
            "text": {
                "content":message
                }
        }
        myrequests(url,headers = headers,json = content ,method = 'post')
    except:
        message = "dingding message send fail ,please check your config"
        mylog().error(message)
        pass
