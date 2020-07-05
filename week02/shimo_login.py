import requests

# 请求头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56',
    'Referer': 'https://shimo.im/login',
    
    # 防止csrf检测
    'x-requested-with': 'XmlHttpRequest'
}

# 开启session浏览
s = requests.session()

# 登录信息
data = {
    'mobile': '+8613022892840',
    'password': '123456'
}

# 登录api地址
login_url = 'https://shimo.im/lizard-api/auth/password/login'

# 登录结果
response = s.post(login_url, data=data, headers=headers)
print('Status Code: %s' % response.status_code)

# 登录之后访问某个页面，验证登录是否成功
response = s.get('https://shimo.im/dashboard', headers=headers)
print('Status Code: %s' % response.status_code)
print('Body: %s' % response.text)