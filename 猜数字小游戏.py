"""
#猜数字小游戏
#上厕所的灵感，无聊制作
"""


print("===========================Yyang Game===============================")
print("========================欢迎进入猜数字游戏==========================")
import random                                    #引入随机数组模块
a=random.randint(1,10)                           #生成随机1--10之间的int类型数字
times=0
while True:                                      #死循环
    
    num=input("数字输入，并按回车键确定：")  #用户输入提示
    

    
    while not num.isdigit():
        num=input("请输入一个整数")
    if int(num)==a:                                   #if判断用户输入
        print("好厉害，猜中了！！！")
        break
    elif int(num)!=a:
        #print("很遗憾，猜错了！！！")
        times+=1
            
        if times<=3:
            if int(num)>=a:
                    print("大了，大了！！！")
            else:
                    print("小了，小了！！！")
        else:
            print("机会被用完了哦哦，再见")
            break

    #print("请输入数字啊，。。。。。。。。。。")
