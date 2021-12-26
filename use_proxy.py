# 代理使用
# 需配合proxy_ip.py爬取代理模块使用
# proxy_ip.py     ues_proxy.py需要在同一目录路径下。


def get_proxy():
    '''
    获取代理ip列表、返回代理ip列表
    '''
    f = open('proxies2_ip.txt', 'r', encoding='utf-8').read()
    all_proxy = re.findall('@(.*?)@', f)
    proxies_list = []
    for a in all_proxy:
        # print(a)
        # print(eval(a))
        proxies_list.append(eval(a))
    return proxies_list


if __name__ == '__main__':
    get_proxy()
    # print(a)
