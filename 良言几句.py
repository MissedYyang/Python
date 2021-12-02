# -*- coding: utf-8 -*-
# 微信QQ自动发送每日添狗句子---
# 加入自动打开微信聊天窗口
# 自动打开qq窗口失败---原因是qq可以多开

#
from time import sleep  # 时间模块
from re import findall  #
from requests import get
from os import walk
from os import system
from os.path import join

from pywinauto.keyboard import send_keys  # 键盘操作
from pywinauto.mouse import click  # 鼠标操作
from gooey import Gooey, GooeyParser


def get_path(app):
    # QQ.exe
    # WeChat.exe
    disk = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'Z:']
    find = False
    while not find:
        for d in disk:
            for roots, files, names in walk(d):
                for n in names:
                    if app == n:
                        file_path = join(roots, n)
                        print(n, file_path)
                        find = True
                        break
    system(file_path)


def get_text(model):
    """
    # 用来爬取网上的每日一添日记
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    if model == '舔狗日记':
         # 舔狗日记
        url = 'https://fabiaoqing.com/jichou/randomrj.html'
        text1 = get(url=url, headers=headers).text.encode(
            'ascii').decode('unicode_escape').split('"')[-2]
    else:
        if model == '彩虹屁':
                # 彩虹屁生成器
            url = 'https://chp.shadiao.app/api.php'
        elif model == '骂人宝典':
                    # 骂人宝典
            url = 'https://zuanbot.com/api.php?level=min&lang=zh_cn'
        elif model == '毒鸡汤文':
            # 毒鸡汤文案生成器
            url = 'https://du.shadiao.app/api.php'
        else:
            # 朋友圈文案生成器
            url = 'https://pyq.shadiao.app/api.php'
        text1 = get(url=url, headers=headers).text
    return text1


def messages_02(name, num, app, model):
    # 微信安装的位置
    get_path(app)
    # 按下查找快捷键
    send_keys('^f')
    sleep(1)
    send_keys(name)
    # 按下回车键
    sleep(1)
    send_keys('{ENTER}')
    # 一直发送
    i = 0
    while i < num:
        result = get_text(model)
        # 输入
        send_keys(result)
        send_keys('{ENTER}')
        i = i + 1


@Gooey(encode="utf-8", program_name='@Yyang', language='chinese')
def main02():
    parse = GooeyParser(description='每日一添')
    parse.add_argument('name', metavar='聊天对象:', widget='TextField')
    parse.add_argument('num', metavar='发送信息数量:', widget='TextField')
    parse.add_argument('app', metavar='选择聊天软件',
                       widget='Dropdown', choices={'微信': 1, 'QQ(有bug)': 2})
    parse.add_argument('model', metavar='选择聊天模式',
                       widget='Dropdown', choices={'舔狗日记': 1, '彩虹屁': 2, '骂人宝典': 3, '毒鸡汤文': 4, '朋友圈文案': 5})
    args = parse.parse_args()
    # 处理下用户输入
    num = int(args.num)
    # print(args.app)
    if args.app == '微信':
        app = 'WeChat.exe'
    else:
        app = 'QQ.exe'
    messages_02(args.name, num, app, args.model)


if __name__ == '__main__':
    main02()
