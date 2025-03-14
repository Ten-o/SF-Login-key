import asyncio
import json
import onnxruntime as ort
import random
import string
import time
from curl_cffi.requests import AsyncSession, exceptions
from curl_cffi import requests
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

appkey = ''

class Phone_SMS:
    def __init__(self):
        self.id = None
        self.operator = None
        self.api_url = 'http://api.sqhyw.net:90'
        self.username = ''
        self.password = ''
        self.mobile = ''
        self.token = ''

    async def api(self, opt):
        if not opt.get('method'):
            opt['method'] = 'get'
        # print(json.dumps(opt, indent=4, ensure_ascii=False))
        async with AsyncSession() as session:
            response = await session.request(opt['method'], **opt['kwargs'])
            status = response.status_code
            resp = response.text

        try:
            resp = json.loads(resp)
        except json.JSONDecodeError:
            pass
        return resp

    async def login(self):
        opt = {
            'kwargs': {
                'url': self.api_url + '/api/logins',
                'params':{
                    'username': self.username,
                     'password': self.password
                }
            }
        }
        resp = await self.api(opt)
        if not resp: return False
        self.token = resp['token']
        data = resp['data'][-1]
        self.id = data['id']
        print(f'登录成功: {self.id}, 剩余: {data["money"]}元')

    async def get_mobile(self):
        if not self.token:
            await self.login()
        opt = {
            'kwargs': {
                'url': self.api_url + '/api/get_mobile',
                'params':{
                    'token': self.token,
                    'project_id': '825829',
                    'operator': 0
                }
            }
        }
        resp = await self.api(opt)
        if not resp: return False
        self.mobile = resp['mobile']
        self.operator = resp['operator']
        print(f'获取到手机号: {self.mobile}, 归属地: {self.operator}')
        return self.mobile

    async def get_message(self):
        if not self.token:
            await self.login()
        opt = {
            'kwargs': {
                'url': self.api_url + '/api/get_message',
                'params':{
                    'token': self.token,
                    'project_id': '825829',
                    'phone_num': self.mobile,
                }
            }
        }
        resp = await self.api(opt)
        if not resp: return False
        code = resp.get('code')
        if code:
            print('获取到验证码:', code)
            return code
        return False


# if __name__ == '__main__':
    # asyncio.run(Phone_SMS().task())

class siliconflow:
    def __init__(self):
        self.sms = Phone_SMS()
        self.shareCode = "HHZPVn92"
        self.default_timeout = 10
        self.support_captcha = [
            'nine'
        ]

        self.cookies = {
            "captcha_v4_user": self.random_sting(32)
        }
        self.result = {}
        self.success = {}
        self.count = 0
        self.herders = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            # "Referer": "https://account.siliconflow.cn/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "referer": f"https://account.siliconflow.cn/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn&invitation={self.shareCode}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }


    async def api(self, opt, t=0):
        # opt['kwargs'].update({'proxy': 'http://' + self.proxy if 'http://' not in self.proxy else self.proxy})
        opt['kwargs']['timeout'] = self.default_timeout
        if opt.get('headers'):
            opt['kwargs']['headers'] = self.herders
        if opt.get('cookies'):
            opt['kwargs']['cookies'] = self.cookies
        if not opt.get('method'):
            opt['method'] = 'post'
        while t < 3:
            try:
                async with AsyncSession() as session:
                    response = await session.request(opt['method'], **opt['kwargs'])
                    status = response.status_code
                    resp = response.text.replace('(', '').replace(')', '')

                try:
                    resp = json.loads(resp)
                except json.JSONDecodeError:
                    pass
                return resp
            except exceptions.Timeout:
                t += 1
            except asyncio.TimeoutError:
                t += 1

            except Exception as e:
                t += 1
        else:
            print(f'请求失败，大于3次，跳过该请求 ')
            return False

    def printf(self, msg, func: str, code: int | str = 200):
        print(f'[{func}]请求出错[{code}]：{msg}')

    def random_sting(self, length: int):
        charset = string.digits + string.ascii_lowercase
        rstr = ''
        for i in range(length):
            rstr += charset[int(random.random() * len(charset))]
        return rstr




    async def user_login(self, phone, sms_code):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "text/plain;charset=UTF-8",
            "origin": "https://account.siliconflow.cn",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": f"https://account.siliconflow.cn/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn&invitation={self.shareCode}",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        url = "https://account.siliconflow.cn/api/account/user"
        data = {
            "phone": phone,
            "code": sms_code,
            "shareCode": self.shareCode,
            "area": "+86"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, data=data)

        print(f'登录结果：{response.text}')
        print(response.headers)
        target_cookie = response.cookies.get("__SF_auth.session-token")
        print(target_cookie)

        headers = {
            'origin': 'https://cloud.siliconflow.cn',
            'referer': 'https://cloud.siliconflow.cn/account/ak',
            'cookie': '__SF_auth.session-token=' + target_cookie
        }
        print(headers)
        params = {
            'action': 'create',
        }

        data = '{"description":"test"}'

        responseq = requests.post(
            'https://cloud.siliconflow.cn/api/redirect/apikey',
            params=params,
            headers=headers,
            data=data,
        )

        resp = responseq.json()
        if resp.get('code') == 20000:
            data = resp.get('data')
            userId = data.get('userId')
            secretKey = data.get('secretKey')
            new_line = f"{userId}:{secretKey}\n"
            try:
                with open('secret.key', 'r+') as f:
                    lines = f.readlines()
                    found = False
                    # 遍历每行查找 userId
                    for i, line in enumerate(lines):
                        if line.startswith(f"{userId}:"):
                            lines[i] = new_line  # 替换整行内容
                            found = True
                            break
                    if not found:
                        lines.append(new_line)
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()  # 清除旧内容残留
            except FileNotFoundError:
                with open('secret.key', 'w') as f:
                    f.write(new_line)
            print(userId, secretKey)


    async def sms_send(self, phone, lot_number, pass_token, gen_time, captcha_output):
        opt = {
            'headers': True,
            'kwargs': {
                'url': "https://account.siliconflow.cn/api/open/sms",
                'json': {
                    "phone": phone,
                    "area": "+86",
                    "device": "5eacfb2dae714e22da7eca2ea61d3b45",
                    "captcha_id": "592ad182314270f0c1442d9aa82d3ac2",
                    "lot_number": lot_number,
                    "pass_token": pass_token,
                    "gen_time": gen_time,
                    "captcha_output": captcha_output
                },
            }
        }
        resp = await self.api(opt)
        status = resp.get('status')
        if status:
            print('短信下发成功 开始获取短信中........')
            while True:
                sms_code = await self.sms.get_message()
                if sms_code: break
            await self.user_login(phone, sms_code)
        else:
            self.printf(resp['message'], 'sms_send')


    async def main(self):
        req = requests.post('http://api.ttocr.com/api/recognize', data={
            'appkey': appkey,
            'gt': '592ad182314270f0c1442d9aa82d3ac2',
            'host': 'gcaptcha4.geetest.com',
            'referer': 'https://account.siliconflow.cn/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn%2F%3F',
            'itemid': 48
        })
        if req.status_code == 200:
            resultid = req.json()['resultid']
            print('等待打码平台返回结果.....')
            while True:
                resp = requests.post('http://api.ttocr.com/api/results', data={
                    'appkey': appkey,
                    'resultid': resultid
                })
                resp = resp.json()

                if resp.get('status') == 1:
                    break
                if resp.get('status') not in [1, 2]:
                    print(resp)
                    return False
                time.sleep(1)
        data = resp.get('data')
        self.result['lot_number'] = data.get('lotNumber')
        self.result['pass_token'] = data.get('passToken')
        self.result['gen_time'] = data.get('genTime')
        self.result['captcha_output'] = data.get('captchaOutput')
        phone = await self.sms.get_mobile()
        await self.sms_send(phone, self.result['lot_number'], self.result['pass_token'], self.result['gen_time'],
                            self.result['captcha_output'])

async def run_tasks():
    tasks = [siliconflow().main() for _ in range(1)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run_tasks())
