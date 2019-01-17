'''
    数据可能每次的三个数（得出和值的数），更有参考价值，更遵循线性回归
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import DB_lucky
import auto_trade
import data_by_trend
page_url="http://www.pceggs.com/play/pxya.aspx"

#先拿一次多一点的，之后每5分钟拿最新一期的就可以了。
def init_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    fp = webdriver.FirefoxProfile(r'C:\Users\binhaiyang\AppData\Roaming\Mozilla\Firefox\Profiles\s74r4l93.default')
    browser = webdriver.Firefox(firefox_profile=fp,
                                executable_path=r'D:\files\chromedriver\geckodriver-v0.23.0-win64\geckodriver.exe',
                                firefox_options=options)  # D:\Program Files\Mozilla Firefox webdriver.Firefox(executable_path = 'D:\files\chromedriver\geckodriver-v0.23.0-win64')
    browser.maximize_window()  # 最大化进入头条的发文章页面
    time.sleep(4)
    browser.get(page_url)
    table = browser.find_element_by_id('panel')
    trs = table.find_elements_by_tag_name('tr')
    index_tr = 0 # 前面7行不需要 后面就只需要取trs[7]
    for tr in trs:
        if(index_tr>6 and index_tr<21):
            # 期号、时间、三个数、后面的不要了
            tds = tr.find_elements_by_tag_name('td')
            series = tds[0].text
            print("qihao:" + series)
            open_time = tds[1].text
            print("时间:" + open_time)
            str_n = tds[2].text.replace(' ', '')
            array_n = str_n.split('+')
            first_n=array_n[0]
            second_n=array_n[1]
            thrid_n=array_n[2].strip('=')
            sum_n = int(first_n)+int(second_n)+int(thrid_n)
            print("去掉空格后的数字:" + str(sum_n))
            DB_lucky.insertOne(series, first_n, second_n, thrid_n, str(sum_n), open_time)
        index_tr+=1

    # driver.find_elements_by_class_name()

last_time=""
def get_new_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    fp = webdriver.FirefoxProfile(r'C:\Users\binhaiyang\AppData\Roaming\Mozilla\Firefox\Profiles\s74r4l93.default')
    browser = webdriver.Firefox(firefox_profile=fp,
                                executable_path=r'D:\files\chromedriver\geckodriver-v0.23.0-win64\geckodriver.exe',
                                firefox_options=options)  # D:\Program Files\Mozilla Firefox webdriver.Firefox(executable_path = 'D:\files\chromedriver\geckodriver-v0.23.0-win64')
    browser.maximize_window()  # 最大化
    time.sleep(4)
    try:
        browser.get(page_url)
        jd = browser.find_element_by_xpath("//*[text()='金蛋：']")
        jdtext = jd.text
        cash = str(jdtext[3:]).replace(',','')
        table = browser.find_element_by_id('panel')
        trs = table.find_elements_by_tag_name('tr')
        # index_tr = 0  # 前面7行不需要 后面就只需要取trs[7]
        tds = trs[7].find_elements_by_tag_name('td')
        series = tds[0].text # 期号
        open_time = tds[1].text # 时间
        is_win = str(tds[6].text).replace(',','')
        global last_time
        # print(last_time)
        print("open_time:"+open_time)
        if (open_time == last_time):
            print("pass这个时间")
            browser.close()
            return
        last_time = open_time
        # print(last_time)
        str_n = tds[2].text.replace(' ', '')
        array_n = str_n.split('+')
        first_n = array_n[0]
        second_n = array_n[1]
        thrid_n = array_n[2].strip('=')
        sum_n = int(first_n) + int(second_n) + int(thrid_n)
        DB_lucky.insertOne(series,first_n,second_n,thrid_n,str(sum_n),open_time,cash,is_win)
    except Exception as e:
        print("出现异常了：" + str(e))
        pass
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    while 1:
        time_start = time.time()
        try:
            get_new_data()
            # time.sleep(20)
            # auto_trade.auto_trade(data_by_trend.get_need_data())
        except Exception as e:
            print("出现异常了：" + str(e))
            pass
        time_end = time.time()
        try:
            time.sleep(5*60 - (time_end-time_start)) # 5分钟一次 不能休息这么长时间，运行需要时间
        except:
            pass
