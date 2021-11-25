#!/usr/bin/env python3
"""
 -*- coding: utf-8 -*-
 @Author：   Yyang
 @Datetime： 2021/11/21 12:07 
 @Ide：      PyCharm
 @Purpose:   #尝试自动完成普法网答题
 @Url:       #https://static.qspfw.moe.gov.cn/user/#/user/login
 @Ps:        #代码加入了等待时间，可自行修改
"""
from time import sleep
import re

import ddddocr
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By

#账号密码获取--未完成
def get_user():
    """用来批量获取用户名账号密码"""
    #文件名--模板，记得修改赋值
    file_name='useridandpassword.xls'
    #读取文件
    result=pandas.read_excel(file_name)
    #遍历文件，获取需要的信息
    for i in result.itertuples():
        #打印测试
        #print(i.Index, i.账号, i.姓名, i.密码)
        user_id=i.账号
        user_name =i.姓名
        password=i.密码
        #暂时想到  #2021.11.25  19:56
        #1.获取一个账号，就运行一个登陆-爬取题库-答题-再进行下一轮
        #2.把全部账号放进一个列表里，在一个个循环
        #不知道怎么更好的处理，登入账号后，答题完，在进入下一个账号的答题





def get_code():
    """获取验证码"""
    img = open('code.png', 'rb').read()
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(img)
    return code


def log_in(driver):
    """登录"""
    g = ['账号', '姓名', '密码']#记得修改为自己的账号密码
    user_id = g[0]  # 账号
    user_name =g[1]  # 姓名
    password = g[2]  # 密码
    url = 'https://static.qspfw.moe.gov.cn/user/#/user/login'
    # 打开网址
    driver.get(url)
    sleep(1)
    # 输入账号,姓名。密码
    driver.find_element(By.ID, 'formLogin_loginInfo').send_keys(user_id)
    driver.find_element(By.ID, 'formLogin_userName').send_keys(user_name)
    driver.find_element(By.ID, 'formLogin_password').send_keys(password)
    # 验证码链接
    src = driver.find_element(By.XPATH, '//img[@title="换一张"]')
    src.screenshot('code.png')
    # 获取验证码------输入验证码=
    code = get_code()
    driver.find_element(By.ID, 'formLogin_captcha').send_keys(code)
    # 点击登录
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(1)
    # 判断是否登录成功----好像不怎么ok,但是可以用
    driver.refresh()
    driver.switch_to.window(driver.window_handles[-1])
    button = driver.find_elements(By.XPATH, '//button[@type="submit"]')
    print(len(button))
    if len(button) != 0:
        log_in(driver)
    else:
        print('登录成功')


def get_result(driver):
    """得到正确答案"""
    file = 'answer_all.txt'
    f = open(file, 'a')
    # 点击去学习
    driver.find_element(
        By.XPATH, '//button[@class="ant-btn ant-btn-link"]').click()
    driver.switch_to.window(driver.window_handles[-1])
    #获取当前页练习的数量
    practice = driver.find_elements(By.XPATH, '//div[@onclick="toPractice(this)"]')
    driver.find_elements(By.XPATH, '//div[@ock="toPractice(this)"]')#
    for j in range(len(practice)):
        # 遍历练习
        driver.find_elements(By.XPATH, '//div[@onclick="toPractice(this)"]')[j].click()
        # 获取答案
        driver.switch_to.window(driver.window_handles[-1])
        # 获取定位元素的文本----题目数量
        number = driver.find_element(By.XPATH, '//span[@id = "totalTopic"]').text
        #print( number)
        for i in range(int(number)):
            #获取问题----题目
            question=driver.find_element(By.ID,'exam_question').text
            # 随便选一个答案-----选第一个A
            driver.find_elements(
                By.XPATH, '//div[@onclick="checkAnswer(this)"]')[0].click()
            # 获取所有的答案选项
            driver.switch_to.window(driver.window_handles[-1])
            checkAnswer = driver.find_elements(
                By.XPATH, '//div[@onclick="checkAnswer(this)"]')
            for c in checkAnswer:
                # 判断答案选项的class属性，是否为正确答案
                if c.get_attribute('class') == 'item success' or c.get_attribute('class') == 'item  success':
                    # 是正确答案执行
                    #print(c.get_attribute('class'), c.get_attribute('data-check'))
                    #获取答案内容
                    xpath='//div[@data-check="'+c.get_attribute("data-check")+'"]/span[@class="content"]'
                    #print(xpath)
                    #print(driver.find_element(By.XPATH,xpath).text)
                    answer_txt=driver.find_element(By.XPATH, xpath).text
                    f.write('&\n'+question+'&'+c.get_attribute('data-check')+'&'+answer_txt+'&\n')
                else:
                    pass
            # 点击下一题------------------根据文本定位元素
            if i != int(number) - 1:
                #点击下一页
                driver.find_element(By.XPATH, '//*[text()="下一题"]').click()
            else:
                pass
        #new*2 返回--学习页面
        driver.back()
        driver.switch_to.window(driver.window_handles[-1])
    f.write('@---------------Next_Class---------------@&\n')
    f.close()
    print('-----ok  ok  ok -----')
    get_result_in=True #用来判断是都否进入了次函数
    return get_result_in


def do_answer(driver,get_result_in):
    """尝试自动答题
        在题库中查找题目，选出答案选项
        有Bug：就是当它答案选项顺序打乱了，就gg了
        本来计划是查找题目，再根据答案的文本信息，来点击的---时间赶不及就写了do_answer02
    """
    f=open('answer_all.txt','r').read().replace('（正确答案）','').replace('\n','')
    #print(f)
    answer_list=re.split('&',f)
    print(answer_list)
    if not get_result_in:
        #如果没有进入get_result函数执行
        #点击去学习
        driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-link"]').click()
        driver.switch_to.window(driver.window_handles[-1])
    else:
        pass
    #点击--综合评价
    driver.find_element(By.ID,'toEvaluation').click()
    #点击--开始答题
    driver.find_element(By.XPATH,'//span[text()="开始答题"]').click()

    #获取当前题目数量---10题，先写死
    for i in range(10):
        sleep(3)
        # 获取当前题目
        question = driver.find_element(By.ID, 'exam_question').text
        #print(question)
        if question in answer_list:
            #如果题目在题目里面,获取问题的索引位置
            question_index=answer_list.index(question)
            #此题目对应的答案，就是下一个
            answer_index=question_index+1
            #获取此题答案
            answer=answer_list[answer_index]
            print(str(i)+answer)
            if answer=='A':
                answer_xpath = '//span[@class="prev" and text()="A"]'
            elif answer=='B':
                answer_xpath = '//span[@class="prev" and text()="B"]'
            elif answer=='C':
                answer_xpath = '//span[@class="prev" and text()="C"]'
            else:
                answer_xpath = '//span[@class="prev" and text()="D"]'
            #点击答案
            driver.find_element(By.XPATH,answer_xpath).click()
            #点击下一题
            if i!=9:
                driver.find_element(By.XPATH,'//*[text()="下一题"]').click()
                driver.switch_to.window(driver.window_handles[-1])
            else:
                pass
        else:
            #题目不存在题库中，则执行获取答案
            print('题目不存在！')
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            get_result_in=get_result(driver)
            #获取完答案后在执行，自动答题
            do_answer(driver,get_result_in)

    #点击提交按钮
    driver.find_element(By.ID,"submit").click()
    sleep(0.5)
    # 处理弹窗---点击确定
    driver.switch_to.alert.accept()
    #退出
    driver.quit()


def do_answer02(driver,get_result_in):
    """尝试自动答题
        在题库中查找答案内容，直接点击选出答案
        ----------测试时是ok的----------
        有Bug：就是当它一个答案对应的题目多个时顺，就gg了
        自我感觉比上一个稳妥---而且简单好理解
    """
    f=open('answer_all.txt','r').read().replace('（正确答案）','').replace(' ','')
    #print(f)
    answer_list=re.split('&',f)
    print(answer_list)
    if not get_result_in:
        #如果没有进入get_result函数执行
        #点击去学习
        driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-link"]').click()
        driver.switch_to.window(driver.window_handles[-1])
    else:
        pass
    #点击--综合评价
    driver.find_element(By.ID,'toEvaluation').click()
    #点击--开始答题
    driver.find_element(By.XPATH,'//span[text()="开始答题"]').click()
    #获取当前题目数量---10题，先写死
    for i in range(10):
        sleep(3)#停顿一下，免得被封
        #获取当前题目的答案选项(4个)
        questions=driver.find_elements(By.XPATH,'//span[@class="content"]')
        for q in questions:
            #遍历题目答案文本
            print(q.text)
            if q.text in answer_list:
                #判断---在题库里。点击
                print('Yes')
                q.click()
            else:
                # 不存在题库中，则pass
                print('No')
                pass

        # 点击下一题
        if i!= 9:
            driver.find_element(By.XPATH, '//*[text()="下一题"]').click()
            driver.switch_to.window(driver.window_handles[-1])
        else:
            pass

    # 点击提交按钮
    driver.find_element(By.ID, "submit").click()
    sleep(0.5)
    #处理弹窗---点击确定
    driver.switch_to.alert.accept()
    #答题完，退出
    driver.quit()


def main():
    """代码主逻辑"""
    # 浏览器配置对象
    options = webdriver.ChromeOptions()
    # 以开发者模式启动浏览器
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 屏蔽以开发者运行提示框
    # options.add_experimental_option('useAutomationExtension', False)
    # 屏蔽保存密码提示框
    prefs = {'credentials_enable_service': False,
             'profile.password_manager_enabled': False}
    options.add_experimental_option('prefs', prefs)
    # 隐藏的webrtc IP检测
    preferences = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    # 关闭webrtc 避免找到真实IP地址
    options.add_experimental_option("prefs", preferences)
    # chrome 88 或更高版本的反爬虫特征处理
    options.add_argument('--disable-blink-features=AutomationControlled')
    # 浏览器对象
    driver = webdriver.Chrome(options=options)
    # 读取脚本 自行下载 stealth.min.js 到相同路径文件夹里
    with open('stealth.min.js', mode='r', encoding='utf-8') as f:
        string = f.read()
    # 移除 selenium 中的爬虫特征
    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument', {'source': string})
    # 隐士等待时间
    driver.implicitly_wait(10)
    # 最大化窗口
    driver.maximize_window()
    # 删除cookies
    driver.delete_all_cookies()
    '''#获取答案代码区域----begin
    # 点击学习----https://static.qspfw.moe.gov.cn/xf2021/learn_practice_list.html
    driver.find_element(
        By.XPATH, '//button[@class="ant-btn ant-btn-link"]').click()
    # 点击学习----第一课
    #driver.find_elements(By.XPATH, '[onclick="toLearning(this)"]')[0].click()
    # 练习
    driver.switch_to.window(driver.window_handles[-1])
    practice=driver.find_elements(By.XPATH, '//div[@onclick="toPractice(this)"]')
    for j in range(len(practice)):
        #遍历练习
        driver.find_elements(By.XPATH, '//div[@onclick="toPractice(this)"]')[j].click()
        # 获取答案
        get_result(driver)
        # 返回--学习页面
        driver.back()
        driver.switch_to.window(driver.window_handles[-1])
    '''##获取答案代码区域-----ending
    return driver


if __name__ == '__main__':
    """运行起点"""
    #判断是否进入了get_result函数
    get_result_in=False
    driver=main()
    #读取文件

    # 登录
    log_in(driver)
    # 获取答案----同一年级获取一次就可以，测试账号为三年级
    #get_result_in=get_result(driver)
    #答题----若没有对应的题库，也会自动爬取，可-无须修改代码
    do_answer(driver,get_result_in)#旧方法------
    #do_answer02(driver,get_result_in)#新方法----- 测试ok
    sleep(15)
    driver.quit()
