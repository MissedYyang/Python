
# 百度贴吧图片下载器
# 新手，代码------见笑了
import re
import os
import requests

from gooey import Gooey, GooeyParser


def get_href(keys):
	"""爬取每个版块的链接"""
    url = 'https://tieba.baidu.com/f?kw={}#'.format(keys)
    heders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    result = requests.get(url).text
    # print(result.text)
    href_all = re.findall('href="/p/(.*?)" title', result)
    return href_all


def get_imgurl(href):
	"""爬取每个版块里的图片链接"""
    url = 'https://tieba.baidu.com/p/{}'.format(href)
    heders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    result = requests.get(url).text
    # print(result)
    url_all = re.findall('<img class="BDE_Image" src="(.*?)" size', result)
    # print(url)
    return url_all


def dowm_img(keys, path):
	"""尝试下载图片，并保存在本地"""
    path = path + '/' + keys
    # 判断文件存在与否
    if not os.path.exists(path):
    	# 不存在创建
        os.makedirs(path)
    # 使用该文件
    os.chdir(path)

    href_all = get_href(keys)
    for h in href_all:
        url_all = get_imgurl(h)
        for u in url_all:
            heders = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
            result = requests.get(u).content
            file = u.split('/')[-1]
            f = open(file, 'wb')
            f.write(result)
            f.close()


@Gooey(encode="utf-8", program_name='@Yyang', language='chinese')
def main():
	"""gui"""
    parse = GooeyParser(description='百度贴吧照片下载器')
    parse.add_argument('keys', metavar='贴吧名称', widget='TextField')
    parse.add_argument('path', metavar='保存位置', widget='DirChooser')
    args = parse.parse_args()
    dowm_img(args.keys, args.path)



if __name__ == '__main__':
	main()

