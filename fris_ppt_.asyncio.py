# 尝试下载第一ppt网站里的班会ppt
# 目标网站：https://www.1ppt.com/kejian/banhui/banhui_3.html
# 目标内容：班会ppt
# 2021-12-25
#报错，但好像不影响使用，初学者，不知道为毛


import re
from fake_useragent import UserAgent
import asyncio
import aiohttp


async def down_file(url):
    headers = {'user-agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers)as response:
            result = await response.read()
            file_name = url.split('/')[-1]
            f = open(file_name, 'wb')
            f.write(result)
            f.close()


async def get_donwurl(url, target):
    headers = {'user-agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers)as response:
            result = await response.text()
            # print(result)
            all_result = re.findall(target, result)
            # print(all_result)
            tasks = []
            for r in all_result:
                url = r
                task = asyncio.create_task(down_file(url))
                tasks.append(task)
            await asyncio.wait(tasks)


async def get_response(url, target):
    headers = {'user-agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers)as response:
            result = await response.text()
            # print(result)
            all_result = re.findall(target, result)
            print(all_result)
            tasks = []
            for r in all_result:
                url = 'https://www.1ppt.com/plus/download.php?open=0&aid={}&cid=17'.format(
                    r)
                target = '<li class="c1"><a href="(.*?)" target="_blank">'
                task = asyncio.create_task(get_donwurl(url, target))
                tasks.append(task)
            await asyncio.wait(tasks)


if __name__ == '__main__':
    for i in range(1, 4):
        target = '<a href="/kejian/(.*?).html"'
        url = 'https://www.1ppt.com/kejian/banhui/banhui_{}.html'.format(i)
        asyncio.run(get_response(url, target))
