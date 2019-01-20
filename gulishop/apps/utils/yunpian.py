import requests, json


class YunPian(object):
    def __init__(self, api_key):
        self.url = 'https://sms.yunpian.com/v2/sms/single_send.json'
        self.api_key = api_key

    def send_code(self, mobile, code):
        data = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': f'【刘渊先生】您的验证码是{code}。如非本人操作，请忽略本短信'
        }
        response = requests.post(url=self.url, data=data).text
        response = json.loads(response)
        return response


