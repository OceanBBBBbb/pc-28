# pc-28
luyck-28

在pc28摸爬滚打了很长时间了。每天领救济连续一个多月后，终于进入到了爆发阶段。最后最高时期达到了累积赢取100亿金蛋。但是在连续三天兑换手机电脑后，就怎么买怎么输，怎么输怎么买，越买越不信邪最后一天输掉50多亿。


作为一个程序员，特别是做过一段时间量化交易程序的，这种事情自然要想用程序来做，于是自己用Python写了一个下注的程序，结果还没运行多久，账户就被冻结了，当然，这个策略是没问题的，被冻结的时候，是运行了3天了，账上已有1300万了。实现这个不会很困难，我是在Windows系统上跑的，使用webdriver就可以了，后期我再用程序试验策略的时候，还会同时跑一个反检测程序，但是也不敢再长期运行了。这个程序我慢慢准备整理后进行开源，但是使用的时候必须要知道，这个是会被检测封号的。GitHub地址：

https://github.com/OceanBBBBbb/pc-28
​
github.com
自打从“牛人”跌下来后，我也不断反思自己，有点感觉到那天是被安排了，做人不能太高调，不然搞的就是你。在之后坚持了几天好的，上了一次亿后，就又凉凉了，一直后来不止盈，多次晚上技术前一会儿把自己玩死。结果是玩棋牌充了n个首冲，依旧没起来。现在的感触就是，生活要往好的方面想，赌博这种东西，不要去惹，除非你是心态特好的人，能很有效的控制自己的情绪，欲望。

为什么这么说？

后来我才发现，pc28已经不使用第三方数据，而是系统随机数了，这样的话，平台可以做手脚的地方就太大了，甚至他可以通过一套算法，做一些勾当。既然是自动生成，那自己也能弄个玩了。下面这套代码就是一个模拟玩这个游戏的，可以修改main方法中的下注数nums，自己输入每期的投注数投注额都是可以的，自己根据注释改一改可以玩很久。代码就是很粗糙的demo：
```
'''
模拟游戏
'''
import random
import time


def get_trade_vol(num):
    return {
        0: 1,
        1: 3,
        2: 6,
        3: 10,
        4: 15,
        5: 21,
        6: 29,
        7: 36,
        8: 45,
        9: 55,
        10: 63,
        11: 69,
        12: 73,
        13: 75,
        14: 75,
        15: 73,
        16: 69,
        17: 63,
        18: 55,
        19: 45,
        20: 36,
        21: 29,
        22: 21,
        23: 15,
        24: 10,
        25: 6,
        26: 3,
        27: 1,
    }.get(num, 1)


def get_peilv(num):
    return {
        0: 1000,
        1: 333.3,
        2: 166.7,
        3: 100,
        4: 66.66,
        5: 47.61,
        6: 35.71,
        7: 27.77,
        8: 22.22,
        9: 18.18,
        10: 15.87,
        11: 14.49,
        12: 13.69,
        13: 13.33,
        14: 13.33,
        15: 13.69,
        16: 14.49,
        17: 15.87,
        18: 18.18,
        19: 22.22,
        20: 27.27,
        21: 35.71,
        22: 47.61,
        23: 66.66,
        24: 100,
        25: 166.7,
        26: 333.3,
        27: 1000,
    }.get(num, 1)


def produceThreeNum():
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    num3 = random.randint(0, 9)
    sum = num1 + num2 + num3
    print(str(num1) + "+" + str(num2) + "+" + str(num3) + "=" + str(sum))
    return sum


local_cash = 1000000
init_case = 1000000
i = 0


def game_begin(num, beilv):
    global i
    global init_case
    # while 1:
    i += 1
    if (num == ''):
        num = input("期数：" + str(i) + ",输入一组数，用,号隔开：")
    # print("你输入的是：" + num)
    if ('' == num):
        return
    nums = num.split(',')
    jichue = 0
    for buy in nums:
        jichue = jichue + get_trade_vol(int(buy))
    if (beilv == ''):
        beilv = input("基础额是:" + str(jichue) + "，当前资产为：" + str(init_case) + ",输入投入倍率：")
    zonge = 0
    for buy in nums:
        zonge = zonge + get_trade_vol(int(buy)) * float(beilv)
    if (zonge > init_case):
        print("余额不足")
        return
    print("投入总额将会是：" + str(zonge))  #
    this_time_num = str(produceThreeNum())  # 获取一个随机数
    if (this_time_num in nums):
        print(this_time_num + "在你的结果中，goal")
        # 根据赔率计算所得
        win = get_peilv(int(this_time_num)) * float(get_trade_vol(int(this_time_num))) * float(beilv)
        win = win - zonge
        init_case = init_case + win
        print('win:+' + str(win) + ",当前总额：" + str(init_case))
        return -1
    else:
        print(this_time_num + "不在结果中")
        init_case = init_case - zonge
        if (init_case < 5000):
            print("凉凉，再见")
            return
        print('lose:-' + str(zonge) + ",当前总额：" + str(init_case))
        return 1


if __name__ == '__main__':
    while 1:
        try:
            local_cash = 1000000
            init_case = 1000000
            is_lose = 0
            is_win = 0
            jichubeilv = 100
            yinzi = 1
            nums = '0,1,2,3,4,5,6,7,8,9,10,11,12,13'
            i = 0
            zhiying = 0
            yinglv = 1.3
            while 1:
                i = i + 1
                if (init_case > 10000000):
                    yinglv = 1.2
                if (init_case > 30000000):
                    yinglv = 1.15
                if (init_case > 60000000):
                    yinglv = 1.1
                print("init_case=" + str(init_case) + ",local_cash=" + str(local_cash))
                if (float(init_case) > float(yinglv * local_cash)):
                    yinzi = yinzi * 1.33
                    local_cash = init_case
                    print(str(i) + "止盈了")
                    zhiying = 22
                if (zhiying > 0):
                    jichubeilv = 10
                    zhiying = zhiying - 1
                result = game_begin(nums, jichubeilv * yinzi)
                # time.sleep(0.1)
                if (result > 0):  # lose
                    is_win = 0
                    is_lose = is_lose + result
                    # nums = '0,1,2,3,4,5,6,7,20,21,22,23,24,25,26,27'
                    if (is_lose > 5):
                        jichubeilv = 50
                        # nums='0,1,2,3,4,5,6,7,8,9,18,19,20,21,22,23,24,25,26,27'
                    else:
                        jichubeilv = jichubeilv * 1.2
                else:
                    # nums = '10,11,12,13,14,15,16,17'
                    is_win = is_win + result
                    is_lose = 0
                    if (is_win < -4):
                        jichubeilv = 50
                    else:
                        jichubeilv = 100
        except:
            time.sleep(5)
            pass

    # while 1:
    #     produceThreeNum()
    #     time.sleep(2)
```
在这之前，我还创建了一个100万期的随机数数据集，通过数据分析，试图计算出各个数之间的关系，甚至还用到马尔科夫、熵等等，而结论就是，重要的不是你买哪些数，而是你的资产管理！

说通白一些，你不管什么时候入场，前面的数理论上和你要买的数是没有任何练习的，这时候不管你是买大还是小，单还是双，都会有一个偏移（熵原理）导致你盈利或是亏损，只要你在盈利的时候（也是是你运气好的时候），做到止盈退出，那你就是赚的；当你运气不好，就只能等待或者赌一把大的，赌到了，扭亏为盈，可以退出了，而没堵到，可能就凉凉了。如果你足够理智，或者有足够的时间，就不必去赌，而是继续平着，直到亏损中和过来，且盈利了一些，这时候退出，也是盈利的。说起来似乎是一个不错的良性循环，而做起来，其实很难很难。

如果有什么需要讨论的，也可以来我的qq群6383003
