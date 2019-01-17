from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import data_by_trend
'''
    先打开页面http://www.pceggs.com/play/pxya.aspx
    找到最靠下方的一个“投注”，点击进去
    对应id="txt14"，输入对应的值，就可以下注
    id="conform_btn"确认投注
'''
vol_rate=0.00004#投入的总资金比例,实际最高=这个数*总资产*1000，即0.0002，相当于没把最高当前资产的0.2

def auto_trade(trade_nums):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    fp = webdriver.FirefoxProfile(r'C:\Users\binhaiyang\AppData\Roaming\Mozilla\Firefox\Profiles\s74r4l93.default')
    browser = webdriver.Firefox(firefox_profile=fp,
                                executable_path=r'D:\files\chromedriver\geckodriver-v0.23.0-win64\geckodriver.exe',
                                firefox_options=options)  # D:\Program Files\Mozilla Firefox webdriver.Firefox(executable_path = 'D:\files\chromedriver\geckodriver-v0.23.0-win64')
    browser.maximize_window()  # 最大化进入头条的发文章页面
    time.sleep(1)
    browser.get("http://www.pceggs.com/play/pxya.aspx")
    time.sleep(3)
    table = browser.find_element_by_id('panel')
    trs = table.find_elements_by_tag_name('tr') # 指定要第7行就行了
    tds = trs[6].find_elements_by_tag_name('td')
    touzhu = tds[7] #投注按钮
    url_art = touzhu.find_element_by_class_name('a0')
    url_art.click()
    time.sleep(2)
    # url = url_art.get_attribute("href")
    sreach_window = browser.current_window_handle # 此行代码用来定位当前页面
    cash = data_by_trend.get_cash();
    is_win_last = data_by_trend.get_if_win()# False为win
    if(is_win_last): #True为亏了
        rate = vol_rate * float(cash) * 0.5
    else:
        rate = vol_rate * float(cash)
    for num in trade_nums:
        txt_num=browser.find_element_by_id('txt'+str(num))
        touzhue = int(float(get_trade_vol(num))*rate)
        txt_num.send_keys(touzhue)
    time.sleep(1)
    conform_btn=browser.find_element_by_id('conform_btn') #comfirm
    conform_btn.click()
    time.sleep(1)
    comfirm_btn=browser.find_element_by_id('fc_an_l170223') #comfirm
    comfirm_btn.click()
    time.sleep(1)
    browser.close()
    browser.quit()

def get_trade_vol(num): #这里最好得到一下当前资产
    return {
        0: 1,
        1: 1,
        2: 1,
        3: 5,
        4: 12,
        5: 20,
        6: 27,
        7: 36,
        8: 45,
        9: 57,
        10: 63,
        11: 69,
        12: 73,
        13: 75,
        14: 75,
        15: 73,
        16: 69,
        17: 63,
        18: 57,
        19: 45,
        20: 36,
        21: 27,
        22: 20,
        23: 12,
        24: 5,
        25: 1,
        26: 1,
        27: 1,
        }.get(num, 1)

if __name__ == '__main__':
    while 1:
        time_start = time.time()
        try:
            auto_trade(data_by_trend.get_need_data())
        except Exception as e:
            print("出现异常了：" + str(e))
        time_end = time.time()
        try:
            time.sleep(5*60 - (time_end-time_start)) # 5分钟一次 不能休息这么长时间，运行需要时间
        except:
            pass