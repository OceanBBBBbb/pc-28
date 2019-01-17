'''
    一切付之一注，我不适合玩博弈。。。
    高赔率策略，在结束前多少秒（越接近停止投注越好），买入高于标准赔率的。
    不一定赔率高的刚好是 赔率的一半
    止盈策略：当前资产大于1.2倍原始资产:
    如果超过了当前总额盈利的20%，就按止损期倍率0.05下单，当资产少于初始资产的1.19倍的时候，重新进入新的周期
    实际按1.23倍和0.055吧，我感觉1.2还不是回归期
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from Include import data_by_trend

vol_rate=0.000033#投入的总资金比例
achive_targ = 1.23 # 止损盈利倍数
init_cash=12345600 #每个周期的初始资金。再次警告，不要手动操作超过每期下单额度资产！手动操作是导致归零的原罪！
#归零后 一次将毫无意义！
is_targ_perid=False #是否在止盈期

def auto_trade():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # profileDir = r'C:\Users\binhaiyang\AppData\Local\Temp\rust_mozprofile.6c3riUYxyBky'  # 这样的话才会每次是新的，建一堆文件啊
    # fp = webdriver.FirefoxProfile(profileDir)
    fp = webdriver.FirefoxProfile(r'C:\Users\binhaiyang\AppData\Roaming\Mozilla\Firefox\Profiles\s74r4l93.default')
    browser = webdriver.Firefox(firefox_profile=fp,
                                executable_path=r'D:\files\chromedriver\geckodriver-v0.23.0-win64\geckodriver.exe',
                                firefox_options=options)  # D:\Program Files\Mozilla Firefox webdriver.Firefox(executable_path = 'D:\files\chromedriver\geckodriver-v0.23.0-win64')
    browser.maximize_window()  # 最大化进入头条的发文章页面

    try:
        time.sleep(1)
        browser.get("http://www.pceggs.com/play/pxya.aspx")
        time.sleep(3)
        jd = browser.find_element_by_xpath("//*[text()='金蛋：']")
        jdtext = jd.text
        cash = int(str(jdtext[3:]).replace(',', ''))#当前余额
#这些地方可以短暂sleep一下
        time.sleep(1)
        table = browser.find_element_by_id('panel')
        trs = table.find_elements_by_tag_name('tr') # 指定要第7行就行了
        tds = trs[6].find_elements_by_tag_name('td')

        rate_adjust = 1
        global is_targ_perid
        global init_cash
        if (0 == init_cash):  # 未设置初始资金，则把初次获取的资金为初始资产
            init_cash = cash
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        print(strTime + ",当前cash:" + str(cash) + ",init_cash:" + str(init_cash))
        if (not is_targ_perid):  # 如果非止盈期，当前的cash是1.23倍init—cash ,进入止盈期
            if (float(cash) > init_cash * achive_targ):
                print("进入止盈期")
                is_targ_perid = True  # 进入止盈期
                rate_adjust = 0.09
                init_cash = cash
        else:  # 在止盈期
            rate_adjust = 0.09
            if (float(cash) < init_cash * 0.988):
                print("退出止盈期")
                is_targ_perid = False  # 退出止盈期
                init_cash = cash
        rate = vol_rate * float(cash) * rate_adjust
        # 先观察一下投注倒计时时间
        span = browser.find_element_by_id('RemainS')
        strong = span.find_element_by_tag_name('strong').text#剩余时间
        touzhu = tds[7]  # 投注按钮
        url_art = touzhu.find_element_by_class_name('a0')
        if(int(strong)>300):
            sleeping_l(int(strong))
        else:
            time.sleep(int(strong)-9) #留10s进行 如果这个时间大于300，则是夜间休市时间，需要分段sleep
        # time_start = time.time()
        url_art.click()
        time.sleep(0.5)
        trs_tz = browser.find_elements_by_xpath("//tr[@height='27' and @bgcolor='#FFFFFF' and @align='center']")
        for i,tr in enumerate(trs_tz):
            now_odds = tr.find_elements_by_tag_name('td')[2].text # 这就是当前赔率，按0-13,27-14排序的
            num = is_high(i, now_odds) #如果当前赔率比标准赔率高，返回这个数，否则返回-1
            if(int(num)>-1):# 如果当前赔率比标准赔率高，加入待买清单
                txt_num = browser.find_element_by_id('txt' + str(num))
                touzhue = int(float(get_trade_com_vol(num))*rate)
                txt_num.send_keys(touzhue)
        conform_btn=browser.find_element_by_id('conform_btn') #comfirm 这里报错说明已经延后了
        conform_btn.click()
        time.sleep(0.3)
        comfirm_btn=browser.find_element_by_id('fc_an_l170223') #comfirm
        comfirm_btn.click()
        # time_end = time.time()
        # print("下注耗时：" + str(time_end-time_start))
        time.sleep(1)
        return 1

    except Exception as e:
            print("出现异常了：" + str(e))
            return 0
    finally:
        browser.close()
        browser.quit()



def sleeping_l(stime):
    # turn_t = int((stime-20)/300)
    for i in range(108):
        time.sleep(300)
        print("休市中" + str(i))
    time.sleep(stime - 32420)

def is_high(i, now_odds):
    real_num=get_real_num(i)
    common_odds=get_common_odds(real_num)
    return real_num if(float(now_odds)>float(common_odds*0.99))else(-1)

#获取对应数字的标赔
def get_common_odds(num):
    return {
        0: 1000,
        1: 333,
        2: 166,
        3: 100,
        4: 66,
        5: 48,
        6: 36,
        7: 28,
        8: 22,
        9: 18,
        10: 16,
        11: 15,
        12: 14,
        13: 13,
        14: 13,
        15: 14,
        16: 15,
        17: 16,
        18: 18,
        19: 22,
        20: 28,
        21: 36,
        22: 48,
        23: 66,
        24: 100,
        25: 166,
        26: 333,
        27: 1000,
    }.get(num, 0)


def get_real_num(num):  # 这里最好得到一下当前资产
    if(num<=13):
        return num
    else:
        return {
            14: 27,
            15: 26,
            16: 25,
            17: 24,
            18: 23,
            19: 22,
            20: 21,
            21: 20,
            22: 19,
            23: 18,
            24: 17,
            25: 16,
            26: 15,
            27: 14,
        }.get(num, 14)

#标准下单额
def get_trade_com_vol(num):
    return {
        0: 1,
        1: 3,
        2: 6,
        3: 10,
        4: 15,
        5: 21,
        6: 28,
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
        21: 28,
        22: 21,
        23: 15,
        24: 10,
        25: 6,
        26: 3,
        27: 1,
    }.get(num, 0)


if __name__ == '__main__':
    while 1:
        time_start = time.time()
        try:
            num = auto_trade()
            if(num==1):
                print("下单成功")
            else:
                print("下单失败")
                time.sleep(60)
                continue
        except Exception as e:
            print("出现异常了：" + str(e))
        time_end = time.time()
        try:
            time.sleep(5*60- (time_end-time_start)) # 5分钟一次 不能休息这么长时间，运行需要时间
        except:
            pass