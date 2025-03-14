import asyncio
import base64
import hashlib
import io
import json
import onnxruntime as ort
import random
import string
import subprocess
import time
import uuid
import numpy as np
from curl_cffi.requests import AsyncSession, exceptions
from curl_cffi import requests
import torch
from PIL import Image
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

pic_point_map = {
    1: [
        (0, 0),
        (100, 87)
    ],
    2: [
        (100, 0),
        (200, 87)

    ],
    3: [
        (200, 0),
        (300, 87)
    ],
    4: [
        (0, 87),
        (100, 174)
    ],
    5: [
        (100, 87),
        (200, 174)

    ],
    6: [
        (200, 87),
        (300, 174)

    ],
    7: [
        (0, 174),
        (100, 274)
    ],
    8: [
        (100, 174),
        (200, 274)

    ],
    9: [
        (200, 174),
        (300, 274)

    ],
}
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
                    'operator': 2,
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
        print(resp)
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
        self.ort_session = ort.InferenceSession('./model.onnx')
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
        self.proxy = 'http://ten:ten-996633@61.177.202.42:40002'


    async def api(self, opt, t=0):

        opt['kwargs'].update({'proxy': 'http://' + self.proxy if 'http://' not in self.proxy else self.proxy})
        opt['kwargs']['timeout'] = self.default_timeout
        if opt.get('headers'):
            opt['kwargs']['headers'] = self.herders
        if opt.get('cookies'):
            opt['kwargs']['cookies'] = self.cookies
        if not opt.get('method'):
            opt['method'] = 'post'
        while t < 3:
            try:
        # print(json.dumps(opt, indent=4, ensure_ascii=False))
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
                # self.log.debug(f'请求失败，第{t}次重试，状态: 请求超时，接口: {param["fn"]}')
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

    def get_values(self, keys: list):
        args = []
        for key in keys:
            args.append(self.result.get(key, ''))
        if len(args) == 1:
            return args[0]
        return args

    def get_pic(self, url: str) -> bytes:
        return requests.get(url, timeout=self.default_timeout).content

    def cut_image(self, img, top_left, bottom_right, size):
        width, height = img.size
        x1, y1 = top_left
        x2, y2 = bottom_right
        x1 = max(0, min(x1, width))  # x1 最小为 0，最大为 width（不超过图像宽度）
        y1 = max(0, min(y1, height))  # y1 最小为 0，最大为 height
        x2 = max(0, min(x2, width))  # x2 最小为 0，最大为 width
        y2 = max(0, min(y2, height))  # y2 最小为 0，最大为 height

        if not (0 <= x1 < width and 0 <= y1 < height and 0 < x2 <= width and 0 < y2 <= height and x1 < x2 and y1 < y2):
            return None

        # 裁剪图像
        cropped_img = img.crop((x1, y1, x2, y2))

        # 计算中心点
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # 计算正方形的边界
        half_size = size // 2
        square_x1 = max(0, center_x - half_size)
        square_y1 = max(0, center_y - half_size)
        square_x2 = min(width, center_x + half_size)
        square_y2 = min(height, center_y + half_size)

        # 裁剪出以中心点为中心的正方形区域
        square_cropped_img = img.crop((square_x1, square_y1, square_x2, square_y2))

        return square_cropped_img

    def resize_with_padding(self, image):
        # 转换图像为Numpy数组
        new_image_array = np.array(image)
        new_image_array = np.transpose(new_image_array, (2, 0, 1))
        new_image_array = np.expand_dims(new_image_array, axis=0)
        new_image_array = (new_image_array.astype(np.float32) / 255)

        return new_image_array

    def get_top_three_matches(self, scores):
        positions = []
        for i in range(3):
            for j in range(3):
                position = (i + 1, j + 1)
                score = scores[i * 3 + j]
                positions.append((round(score, 2), position))
        positions.sort(key=lambda x: x[0], reverse=True)

        top_three = positions[:3]
        return [[pos[1][0], pos[1][1]] for pos in top_three]

    def get_match_string_bool(self, str1):
        return str1.startswith('000')

    async def task(self):
        imgs, ques = self.get_values(['imgs', 'ques'])
        # print(f'https://static.geetest.com/{imgs}')
        # print(f'https://static.geetest.com/{ques[0]}')
        bg = self.get_pic(f'https://static.geetest.com/{imgs}')
        tip = self.get_pic(f'https://static.geetest.com/{ques[0]}')

        b64decode_bg = base64.b64decode(base64.b64encode(bg))
        b64decode_tip = base64.b64decode(base64.b64encode(tip))
        bg_image = Image.open(io.BytesIO(b64decode_bg))
        tip_image = Image.open(io.BytesIO(b64decode_tip))

        score = []
        for point_setting in pic_point_map:
            points = pic_point_map[point_setting]
            point1, point2 = points[0], points[1]
            adjust_image: Image = self.cut_image(bg_image, point1, point2, 80)
            if tip_image.mode in ('RGBA', 'LA', 'P', 'L', 'RGB'):
                tip_image_rgba = tip_image.convert('RGBA')
                white_background = Image.new('RGBA', tip_image.size,
                                             (255, 255, 255, 255))
                image_rgb = Image.alpha_composite(white_background, tip_image_rgba).convert(
                    'RGB')
            else:
                image_rgb = tip_image.convert('RGB')  #

            resized_image = adjust_image.resize((50, 50))
            tip_image = image_rgb.resize((50, 50))
            png_image = np.array(tip_image)
            tile_image = np.array(resized_image)
            input_data = {'image_1': self.resize_with_padding(png_image), 'image_2': self.resize_with_padding(tile_image)}
            output = self.ort_session.run(None, input_data)[0]
            calculate_value = torch.nn.Sigmoid()(torch.from_numpy(output)).item()
            print(f'模型：相似度 -> {output}')

            score.append(calculate_value)
        userresponse = self.get_top_three_matches(score)
        print(f'输出 -> {userresponse}')

        pow_detail = self.result['pow_detail']

        while True:
            pow_msg = f"{pow_detail['version']}|{pow_detail['bits']}|{pow_detail['hashfunc']}|{pow_detail['datetime']}|592ad182314270f0c1442d9aa82d3ac2|{self.result['lot_number']}||{self.random_sting(16)}"
            pow_sign = hashlib.md5(pow_msg.encode()).hexdigest()
            if self.get_match_string_bool(pow_sign): break

        base_data = {
            "passtime": random.randint(1000, 2000),
            "userresponse": userresponse,
            "device_id": "",
            "lot_number": self.result['lot_number'],
            "pow_msg": pow_msg,
            "pow_sign": pow_sign,
            "geetest": "captcha",
            "lang": "zh",
            "ep": "123",
            "biht": "1426265548",
            "gee_guard": {
                "roe": {
                    "aup": "3",
                    "sep": "3",
                    "egp": "3",
                    "auh": "3",
                    "rew": "3",
                    "snh": "3",
                    "res": "3",
                    "cdc": "3"
                }
            },
            "xUGO": "3ILF",
            "em": {
                "ph": 0,
                "cp": 0,
                "ek": "11",
                "wd": 1,
                "nt": 0,
                "si": 0,
                "sc": 0
            }
        }

        code = subprocess.Popen(['node', './test.js', str(json.dumps(base_data, separators=(",", ":"))), ],
                                stdout=subprocess.PIPE).stdout.read().strip().decode()
        params = {
            "captcha_id": "592ad182314270f0c1442d9aa82d3ac2",
            "client_type": "web",
            "lot_number": self.result['lot_number'],
            "risk_type": "nine",
            "payload": self.result['payload'],
            "process_token": self.result['process_token'],
            "payload_protocol": self.result['payload_protocol'],
            "pt": "1",
            "w": code
        }
        return await self.verify(params)
    async def refresh_image(self, lot_number, payload, process_token):
        params = {
            "captcha_id": "592ad182314270f0c1442d9aa82d3ac2",
            "challenge": str(uuid.uuid4()),
            "client_type": "web",
            "risk_type": "nine",
            "lang": "zho",
            'lot_number': lot_number,
            'pt': '1',
            'payload': payload,
            'process_token': process_token,
            'payload_protocol': '1',
        }
        opt = {
            'method': 'get',
            'headers': True,
            'cookies': True,
            'kwargs': {
                'url': "https://gcaptcha4.geetest.com/load",
                'params': params,
            }
        }
        resp = await self.api(opt)
        if not resp: return
        status = resp.get('status')
        ret = False
        if status == 'success':
            data = resp['data']
            captcha_type = data['captcha_type']
            if captcha_type in self.support_captcha:
                ret = data
            else:
                self.printf('验证方式不支持', 'get_load')
        else:
            self.printf('异常', 'get_load')
        return ret


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
        set_cookie_headers = response.headers.get('set-cookie')
        print(set_cookie_headers)
        headers = {
            'origin': 'https://cloud.siliconflow.cn',
            'referer': 'https://cloud.siliconflow.cn/account/ak',
            'cookie': set_cookie_headers
        }
        params = {
            'action': 'create',
        }
        data = '{"description":"test"}'

        response = requests.post(
            'https://cloud.siliconflow.cn/api/redirect/apikey',
            params=params,
            headers=headers,
            data=data,
        )
        resp = response.json()
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
            while True:
                sms_code = await self.sms.get_message()
                if sms_code: break
            await self.user_login(phone, sms_code)
        else:
            self.printf(resp['message'], 'sms_send')



    async def verify(self, params):

        opt = {
            'method': 'get',
            'headers': True,
            'cookies': True,
            'kwargs': {
                'url': "https://gcaptcha4.geetest.com/verify",
                'params': params,
            }
        }
        resp = await self.api(opt)
        if not resp: return
        status = resp.get('status')
        ret = False
        if status == 'success':
            data = resp['data']
            result = data['result']
            print(f'验证结果：{result}')
            if result == 'success':
                ret = True
                seccode = data['seccode']
                phone = await self.sms.get_mobile()
                await self.sms_send(phone, seccode['lot_number'], seccode['pass_token'], seccode['gen_time'],
                         seccode['captcha_output'])

        else:
            self.printf('异常', 'verify')
        return ret

    async def get_load(self):
        opt = {
            'method': 'get',
            'headers': True,
            'cookies': True,
            'kwargs': {
                'url': "https://gcaptcha4.geetest.com/load",
                'params':{
                    "captcha_id": "592ad182314270f0c1442d9aa82d3ac2",
                    "challenge": str(uuid.uuid4()),
                    "client_type": "web",
                    "risk_type": "nine",
                    "lang": "zh-cn"
                },
            }
        }
        resp = await self.api(opt)
        if not resp: return
        status = resp.get('status')
        ret = False
        if status == 'success':
            data = resp['data']
            captcha_type = data['captcha_type']
            if captcha_type in self.support_captcha:
                ret = data
            else:
                self.printf('验证方式不支持', 'get_load')
        else:
            self.printf('异常', 'get_load')
        return ret

    async def main(self):

        while not self.result:
            self.result = await self.get_load()
            time.sleep(random.uniform(0.3, 1))
        while not self.success:
            if await self.task(): break
            self.count += 1
            print(f'刷新验证码第[{self.count}]次')
            self.result = await self.refresh_image(self.result['lot_number'], self.result['payload'], self.result['process_token'])

async def run_tasks():
    tasks = [siliconflow().main() for _ in range(1)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run_tasks())
