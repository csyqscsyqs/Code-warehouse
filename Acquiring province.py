import os
import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# 获取IP地址
def get_ip_address():
    try:
        r = requests.get('http://ip.42.pl/raw')
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

# 获取IP地址所在省份
def get_province_by_ip(ip):
    try:
        url = 'http://ip-api.com/json/{}?lang=zh-CN'.format(ip)
        r = requests.get(url)
        if r.status_code == 200:
            data = json.loads(r.text)
            if data['status'] == 'success':
                return data['regionName']
    except:
        pass
    return None

# 将信息写入日志文件
def write_to_log_file(log_file_path, message):
    with open(log_file_path, 'a') as f:
        f.write(message + '\n')

# 获取用户的 QQ 账号
def get_user_qq():
    # 这里假设获取到了用户的 QQ 账号，这里用 123456 代替
    return '123456'

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 处理用户提交的表单
@app.route('/submit', methods=['POST'])
def submit():
    if request.form.get('yes'):
        ip = get_ip_address()
        if ip is not None:
            province = get_province_by_ip(ip)
            qq = get_user_qq()
            if province is not None:
                message = 'IP 地址：{}，省份：{}，QQ 账号：{}'.format(ip, province, qq)
            else:
                message = '无法获取位置信息，IP 地址：{}，QQ 账号：{}'.format(ip, qq)
        else:
            message = '无法获取 IP 地址，QQ 账号：{}'.format(qq)

        log_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', '输出日志.txt')
        write_to_log_file(log_file_path, message)
        return render_template('success.html')
    else:
        return render_template('failure.html')

if __name__ == '__main__':
    app.run()
