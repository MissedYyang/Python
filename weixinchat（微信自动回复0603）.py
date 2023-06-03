'''
微信自动回复测试
'''
import re
import requests
import uiautomation 
from uiautomation import WindowControl, MenuControl

#利用chatapi,回复消息
#01获取key
def get_pubkey():
    url='https://api.aigcfun.com/fc/key'
    headers={"Content-Type":"application/json",
                    "Referer":"https://aigcfun.com/"}
    
    res=requests.get(url=url,headers=headers)
    #print(res.text)
    key=re.findall('"data":"(.*?)"',res.text)[0]
    
    #print(key)
    return  key
    
#调用接口回答问题
def get_answer(key,question):
    url="https://api.aigcfun.com/api/v1/text?key="+key
    headers={"Content-Type": "application/json",
    "Referer": "https://aigcfun.com/"}
    
    data={"messages":[{"role": "system","content":"请以txt的形式返回答案"},{"role": "user","content":question}],
    "tokensLength":20,
    "model":"gpt-3.5-turbo"
    }
    res=requests.post(url=url,headers=headers,json=data)
    #print(res.text)
    asw_txt=re.findall('"text":"(.*?)"',res.text)[-1]
    #content=re.findall('"content":"(.*?)"',res.text)
    #print(asw_txt)
    return asw_txt

if __name__ == '__main__':
    #打开微信窗口
    wx = WindowControl(Name="微信")
    #进入窗口
    wx.SwitchToThisWindow()
    #进入会话窗口
    hw = wx.ListControl(Name="会话")
    #print(hw)
    while True:
        #查找未读消息，查找范围为前4个会话窗口
        we=hw.TextControl(searchDepth=4)
        #存在消息
        if we.Name:
            #点击进入未读消息（默认第一个会话）
            we.Click(simulateMove=False)
            #读取消息msg=wx.ListControl(Name='消息').GetChildren()
            #读取最后一条消息
            msg=wx.ListControl(Name='消息').GetChildren()[-1].Name
            print('最后一条消息是：',msg)

            #回复消息：
            question=msg
            key=get_pubkey()
            asw_txt=get_answer(key,question)
            #print(type(asw_txt))
            wx.SendKeys(asw_txt,waitTime=0)

            wx.SendKeys('{Enter}',waitTime=0)
        else:
            #print('没有新消息。。。')
            pass



 
