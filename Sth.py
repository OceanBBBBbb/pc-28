import time
last_time=""
def test_data(open_time):
    global last_time
    if (open_time is last_time):
        print("pass这个时间")
        return
    last_time = open_time
    print("ss:" + last_time)

'''
有17个人围成一圈(编号0~16),从第0号的人开始从1报数，凡报到3的倍数的人离开圈子，然后再数下去，
直到最后只剩下一个人为止，问此人原来的位置是多少号?
'''
if __name__ == '__main__':
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    # strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    # print(strTime)
    n = 0
    for i in range(2,5):
        n = (n + 3) % i;
    print(n)

    # a = False
    # print(a)
    # time.sleep(0.5)
    # print(not a)
    # a = 0
    # while 1:
    #     a+=1
    #     if(a%3==0):
    #         print("aa")
    #     else:
    #         print("bb")
    #         continue
    #     time.sleep(5)
        # sss=['a b','b c','c d','a b','a b']
        # for ss in sss:
        #     test_data(ss)
        # time.sleep(10)