#!/usr/bin/env python3
"""
 -*- coding: utf-8 -*-
 @Author：   Yyang
 @Datetime： 2021/11/9 18:58
 @Ide：      PyCharm
 @Purpose:   #爬取小说，保存至本地，xx.txt
 #新人小白一枚，代码不知道怎么精简,打包后发现不支持中文，百度翻译为英语，打包好依旧不行，不知道为毛
"""
# 模块引入
import re  # 正则表达式
from string import punctuation

import requests  # 爬虫
from fake_useragent import UserAgent  # 伪装浏览头模块
from gooey import Gooey, GooeyParser  #


def get_id(key):
    # 网站搜索小说请求网址
    url = 'https://www.txt909.com/search/'
    # 请求信息
    headers0 = {'authority': 'www.txt909.com', 'method': 'POST', 'path': '/search/', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'max-age=0', 'content-length': '56', 'content-type': 'application/x-www-form-urlencoded', 'cookie': 'articlevisited=1', 'origin': 'https://www.txt909.com',
                'referer': 'https://www.txt909.com/search/', 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': ' ?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': ' navigate', 'sec-fetch-site': ' same-origin', 'sec-fetch-user': ' ?1', 'upgrade-insecure-requests': ' 1', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    headers = {'user-agent': UserAgent().random}
    # 请求数据
    data = {'show': 'title,writer', 'searchkey': key, 'Submit': ' '}
    # 发送请求
    # result = requests.post(url=url, headers=headers, data=data)
    result = requests.post(url=url, headers=headers,
                           data=data).text  # 小白一枚，不知道为毛加上headers0(来自浏览器--复制)报错了。
    # print(result)  # 打印测试
    # 利用正则表达式提取，小说链接，小说名字
    id_all = re.findall(
        '"title"><a href="/txt/(.*?).html" title=".*?" target="_blank">', result)
    title_all = re.findall(
        '"title"><a href=".*?" title="(.*?)" target="_blank">', result)
    #print((' 搜索结果为： {} ，一共有{}本小说：\n').format(title_all,len(id_all)))
    print((' A total of {} novels：\n').format(len(id_all)))
    return id_all, title_all


def get_text(key, path):
    id_all, title_all = get_id(key)
    # 判断小说的id是否为空
    if len(id_all) != 0:
        # 不为空执行
        for i in range(len(id_all)):
            #print(('正在下载第 {0} 本小说，名字为：.\n').format(i + 1,title_all[i]))
            #print(('Is downloading {0} ,name:{}.\n').format(i + 1, title_all[i]))
            print(('Is downloading {0} .\n').format(i + 1))
            url = 'http://down.xsbooktxt.cc/modules/article/txtarticle.php?id={}'.format(
                id_all[i])
            headers = {'user-agent': UserAgent().random}
            result = requests.get(url=url, headers=headers).content
            # 去除名字中有特殊符号
            title = re.sub(r'[%s]+' % punctuation, '', title_all[i])

            file_name = path + '\\' + title + '.txt'
            # 保存小说文本
            f = open(file_name, 'wb')
            f.write(result)
            f.close()
            #print((' {}，下载完成。。。。。。。').format(title_all[i]))
            #print(('Name: {}，The download is complete。。。。。。。').format(title_all[i]))
            print(('{}，The download is complete。。。。。。。').format(i + 1))
        # 全部下载完，提示
        print('ok，ok,ok!!!\n')
    else:
        # 小说ID为0 ，搜索为空时提示
        # print('错误：小说名字有误.\n')
        print('Error: The wrong name for the novel.\n')

# 装饰器，用来转换成gui


@ Gooey(encoding='utf-8', program_name='小说下载器 ', language='chinese')
def main():
    parser = GooeyParser(description=' Novel_Download')
    parser.add_argument('key', metavar='小说名字', widget='TextField')
    parser.add_argument('path', metavar='保存位置', widget='DirChooser')
    args = parser.parse_args()
    print('Search in progress, please wait patiently。。。。。。')
    get_text(args.key, args.path)


if __name__ == '__main__':
    main()
    # print(UserAgent().random)
