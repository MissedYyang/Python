
#爬取代理ip---------------- OK
#测试代理ip的可用性--------- OK
# 觉得有点浪费,不如直接测试在写入文件


import re
from fake_useragent import UserAgent
from requests import get


class MyProjectProxyIp02():
    '''
    在01的基础上，尝试优化
    '''

    def __init__(self, url):
        '''
        '''
        self.headers = {'uesr-agent': UserAgent().random}  # 随机生成请求头
        self.url = url  # 网址
        self.all_proxies = []  # 存放代理IP信息
        self.f = open('proxies2_ip.txt', 'a+', encoding='utf-8')
        self.test_url = 'http://httpbin.org/ip'
        self.count = 0

    def get_proxise(self):
        '''
        爬取网页上的代理IP信息
        '''
        # 获取网页响应
        response = get(url=self.url, headers=self.headers)
        # 转还响应的编码
        result = response.content.decode('utf-8')
        # print(result)#打印测试
        # 正则表达式查找符合目标的所有，pythonista无法用lxml.etree
        all = re.findall('<td>(.*?)</td>', result)
        # print(all,len(all))#打印测试

        # 遍历得到的结果
        for i in range(int((len(all)) / 7)):
            i = i * 7
            '''print('IP地址:',all[i])
			print('端口号:',all[i+1])
			print('匿名等级:',all[i+2])
			print('代理类型:',all[i+3])
			print('响应时间:',all[i+4])
			print('地理位置:',all[i+5])
			print('验证时间:',all[i+6])
			print('\n')'''
            # ip代理信息
            proxy = {'代理类型': all[i + 3], 'IP地址': all[i], '端口号': all[i + 1],
                     '匿名等级': all[i + 2], '响应时间': all[i + 4], '地理位置': all[i + 5], '验证时间': all[i + 6]}

            # print(proxy)
            # 加入列表中
            self.all_proxies.append(proxy)

        return self.all_proxies

    def test_ip(self):
        '''
        测试代理ip的可用性
        '''
        # 遍历
        for p in self.all_proxies:
            # print(p)#打印测试
            #print(p['代理类型'])#
            #print(p['IP地址'])#
            #print(p['端口号'])#
            # 判断
            if ',' in p['代理类型']:
                a = p['代理类型'].split(',')
                proxies = {a[0].lower(): (a[0].lower() + '://' + p['IP地址'] + ':' + p['端口号']),
                           a[1].lower(): (a[1].lower() + '://' + p['IP地址'] + ':' + p['端口号'])}
            else:
                proxies = {p['代理类型'].lower(): (
                    p['代理类型'].lower() + '://' + p['IP地址'] + ':' + p['端口号'])}
            # print(proxies)

            try:
                # 使用代理IP，超时为8秒
                response = get(url=self.test_url,
                               headers=self.headers, proxies=proxies, timeout=8)

                print(response)  # 打印响应代码测试
                print(response.content.decode('utf-8'))

                print('代理IP:', proxies, ',OK')  # 打印测试
                # 写入文件
                self.f.write(str(p))
                self.f.write('\n@')
                self.f.write(str(proxies))
                self.f.write('@\n\n')
                self.count = self.count + 1
                print(self.count)
                # 关闭文件
                self.f.close()
            except:
                # 失败提示
                print('代理IP:', proxies, ',失败')


class MyProjectProxyIp01():
    '''
    获取代理IP、并测试其可用性
    '''

    def __init__(self, url):
        '''

        '''
        self.headers = headers = {'uesr-agent': UserAgent().random}
        self.url = url

    def get_text(self):
        """
        获取网页响应，获取代理地址
        """
        # 获取网页响应
        response = get(url=self.url, headers=self.headers)
        # 转还响应的编码
        result = response.content.decode('utf-8')
        # print(result)#打印测试
        # 正则表达式查找符合目标的所有，pythonista无法用lxml.etree
        all = re.findall('<td>(.*?)</td>', result)
        # print(all,len(all))#打印测试
        # 遍历得到的结果
        for i in range(int((len(all)) / 7)):
            i = i * 7
            '''print('IP地址:',all[i])
			print('端口号:',all[i+1])
			print('匿名等级:',all[i+2])
			print('代理类型:',all[i+3])
			print('响应时间:',all[i+4])
			print('地理位置:',all[i+5])
			print('验证时间:',all[i+6])
			print('\n')'''
            # 以追加的形式打开文件
            f = open('proxies_ip.txt', 'a+', encoding='utf-8')
            # 构造写入文件的文字内容
            text = ('代理类型:' + all[i + 3]) + ('\nIP地址:' + all[i]) + ('端口号:' + all[i + 1]) + ('\n匿名等级:' + all[i + 2]) + (
                '\n响应时间:' + all[i + 4]) + ('\n地理位置:' + all[i + 5]) + ('\n验证时间:' + all[i + 6] + '\n\n@')
            # 写入文件,关闭文件
            f.write(text)
            f.close()

    def test_ip(self):
        """
        测试ip的可用性，保留or删除
        """
        # 测试网址
        test_url0 = 'https://whatismyipaddress.com/'
        test_url1 = 'https://www.whatismyip.com.tw/'
        test_url2 = 'https://icanhazip.com/'
        test_url = 'http://httpbin.org/ip'

        # 以只读的方式读取文件
        proxies_text = open('proxies_ip.txt', 'r', encoding='utf-8').read()
        # 去掉换行符，并以@分隔文本内容
        proxy_text = proxies_text.split('@')
        # print(proxy_text)#打印测试

        # 遍历以@分隔文本得到的字符串
        for p in proxy_text:
            p1 = p.replace('\n', '')
            print(p1)
            # 查找文件里的代理ip及端口号
            proxy_ip = re.findall('代理类型:(.*?)匿名等级', p1)
            # print(proxy_ip)#打印测试
            # 替换内容
            proxy_ip = str(*proxy_ip).replace('端口号', '')  # 不知道为啥，用列表index取值报错
            # print(proxy_ip)#打印测试
            # 判断代理IP的内容
            if ',' in proxy_ip:
                # HTTP,HTTPSIP地址:120.78.164.79:59394
                # print(proxy_ip)
                proxies = {(proxy_ip.split(',')[0]).lower(): (proxy_ip.split(',')[0]).lower() + '://' + (proxy_ip.split('IP地址:')[-1]), (proxy_ip.split(
                    'IP地址:')[0].split(',')[-1]).lower(): (proxy_ip.split('IP地址:')[0].split(',')[-1]).lower() + '://' + (proxy_ip.split('IP地址:')[-1])}
            else:
                proxies = {(proxy_ip.split('IP地址:')[0]).lower(): (proxy_ip.split(
                    'IP地址:')[0]).lower() + '://' + (proxy_ip.split('IP地址:')[-1])}

            # print(proxies)#打印测试
            #{'HTTP': '115.29.170.58:8118'}
            #
            try:

                response = get(url=test_url, headers=self.headers,
                               proxies=proxies, timeout=8)

                print(response)  # 打印响应代码测试
                print(response.content.decode('utf-8'))

            except:
                # proxies_text=open('proxies_ip.txt','r',encoding='utf-8').read()
                proxies_text = proxies_text.replace('@' + p, '')
                # print(proxies_text)
                print('代理IP:', proxies, ',已移除')
                # print(proxies_text)
        # 把测试通过的代理ip写入文件,关闭文件
        f = open('proxies_ip.txt', 'w', encoding='utf-8')
        f.write(proxies_text)
        f.close()


def mian():
    '''#one
    for i in range(1,2):
            url='http://www.kxdaili.com/dailiip/1/{}.html'.format(i)
            #
            myproject=MyProjectProxyIp01(url)
            #爬取代理ip
            myproject.get_text()
            #测试代理ip
            #myproject.test_ip()
            print(' OKOKOK')

    #'''

    #'''#two
    for i in range(1, 10):
        url = 'http://www.kxdaili.com/dailiip/1/{}.html'.format(i)
        #
        myproject = MyProjectProxyIp02(url)
        # 爬取代理ip
        all_proxy = myproject.get_proxise()
        # 测试代理ip
        # myproject.test_ip()
        print(' OKOKOK')
        myproject.test_ip()
        # print(all_proxy)

    #'''


mian()
