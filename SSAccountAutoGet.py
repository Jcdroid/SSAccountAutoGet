# -*- coding: utf-8 -*-
__author__ = 'caojing'

import urllib2
import requests
import hashlib
import json
import time
import threading
import codecs
from bs4 import BeautifulSoup
import sys

# 解决编码问题
reload(sys)
sys.setdefaultencoding("utf-8")

# 默认设置
# header = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"
# header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36' }
header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36' }
url_login = 'https://www.ss-link.com/login'
url_free = 'https://www.ss-link.com/my/free'
# file_path = './xxx/Shadowsocks/gui-config-test.json'
file_path = './xxx/Shadowsocks/gui-config.json'
loop_wait_time = 55 * 60 # 服务器默认为一小时，我这里默认设置循环等待时间必须小于一小时，所以设置为55分钟

def autoModifyPW(password_net):

    print '---------------------------------------------------\n'
    # print '网络密码 = {0}'.format(password_net)
    # 解决window cmd中文乱码
    print '网络密码 = {0}'.format(password_net).decode('utf-8').encode('cp936')

    path = unicode(file_path, 'utf-8')

    # 读取数据
    with open(path, 'r+') as f:
        data = json.load(f)

        password_old = data['configs'][0]['password']
        remarks = data['configs'][0]['remarks']
        # print '当前账户 = {0}, 旧密码 = {1}'.format(remarks, password_old)
        print '当前账户 = {0}, 旧密码 = {1}'.format(remarks, password_old).decode('utf-8').encode('cp936')

        data['configs'][0]['password'] = password_net

        password_new = data['configs'][0]['password']
        # print '当前账户 = {0}, 新密码 = {1}'.format(remarks, password_new).format(remarks, password_new)
        print '当前账户 = {0}, 新密码 = {1}'.format(remarks, password_new).format(remarks, password_new).decode('utf-8').encode('cp936')

        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print '最后更新时间：{0}'.format(current_time)
        print '最后更新时间：{0}'.format(current_time).decode('utf-8').encode('cp936')

        print '---------------------------------------------------\n\n'

        # data['id'] = 134 # <--- add `id` value.
        # f.seek(0)        # <--- should reset file position to the beginning.
        # json.dump(data, f, indent=4)

    # filer = open(path, 'r')
    # jsonStr = ''
    # for line in filer:
    #     jsonStr += line
    # filer.close()
    # print '旧gui-config = {0}'.format(jsonStr)

def extractHtml(html):
    soup = BeautifulSoup(html)
    tbody = soup.tbody

    list = []
    for tr in tbody.children:
        if not tr == '\n':
            for td in tr.children:
                if not td == '\n':
                    # if cmp(td.string, u'美国拉斯维加斯VW线路'):
                    # print td.string
                    list.append(td.string)

    return list[3]


def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def login(form_data):
    s = requests.session()
    response = s.post(url_login, data = form_data, headers = header)
    # print response.content
    return response.content

def get_last_pw():
    form_data = {
        'email':'123456@qq.com',
        'redirect':'/my/free',
        'password':'123456'
    }
    # print 'no encryption : '+form_data['password']
    form_data['password'] = md5(form_data['password'])
    # print 'encryption : '+form_data['password']
    autoModifyPW(extractHtml(login(form_data)))

    global timer
    timer = threading.Timer(loop_wait_time, get_last_pw)
    timer.start()

if __name__ == '__main__':
    # print '^_^ 欢迎使用SS账号自动获取器，祝生活愉快！ ^_^'.decode('utf-8').encode('cp936') # cmd model
    print '^_^ 欢迎使用SS账号自动获取器，祝生活愉快！ ^_^'.decode('utf-8')
    timer = threading.Timer(0, get_last_pw)
    timer.start()