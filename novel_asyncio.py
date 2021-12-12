# 尝试使用异步爬取小说
# 第二次使用

# 模块引入
import re
from string import punctuation
import asyncio

import aiohttp
from fake_useragent import UserAgent  # 伪装浏览头模块


async def get_text(id, title):
    # 去除名字中有特殊符号
    title = re.sub(r'[%s]+' % punctuation, '', title)
    print(('正在下载小说：{0}  ,id={1}.\n').format(title, id))
    file_name = "C:\\Users\\Administrator\\Desktop\\新建文件夹\\" + title + '.txt'
    url = 'http://down.xsbooktxt.cc/modules/article/txtarticle.php?id={}'.format(
        id)
    headers = {'user-agent': UserAgent().random}

    # 下面没执行就结束任务了-----手动加入io阻塞，延长了get_id执行时间
    #原来60行少了await hhhhhhhh
    async with aiohttp.ClientSession() as session1:
        async with await session1.get(url=url, headers=headers) as response0:
            response1 = await response0.read()
            # 保存小说文本
            f = open(file_name, 'wb')
            f.write(response1)
            f.close()
            print('{} is ok!!'.format(title))


async def get_id(key):
    tasks = []
    # 网站搜索小说请求网址
    url = 'https://www.txt909.com/search/'
    # 请求信息
    headers0 = {'authority': 'www.txt909.com', 'method': 'POST', 'path': '/search/', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'max-age=0', 'content-length': '56', 'content-type': 'application/x-www-form-urlencoded', 'cookie': 'articlevisited=1', 'origin': 'https://www.txt909.com',
                'referer': 'https://www.txt909.com/search/', 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': ' ?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': ' navigate', 'sec-fetch-site': ' same-origin', 'sec-fetch-user': ' ?1', 'upgrade-insecure-requests': ' 1', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    headers = {'user-agent': UserAgent().random}
    # 请求数据
    data = {'show': 'title,writer', 'searchkey': key, 'Submit': ' '}
    # 发送请求
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            response = await response.text()
            id_all = re.findall(
                '"title"><a href="/txt/(.*?).html" title=".*?" target="_blank">', response)
            title_all = re.findall(
                '"title"><a href=".*?" title="(.*?)" target="_blank">', response)
            print((' 搜索结果为： {} ，一共有{}本小说：\n').format(title_all, len(id_all)))
            for i in range(len(id_all)):
                n = {'小说名': title_all[i], 'id': id_all[i]}
                # all_novel.append(n)
                print(n)
                task = asyncio.create_task(get_text(id_all[i], title_all[i]))
                tasks.append(task)
                #await asyncio.sleep(2)  # 加入这句话就可以，但是时间也变长了
            await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(get_id('妹妹'))
