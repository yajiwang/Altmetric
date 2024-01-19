import csv
import math
import os
from queue import Queue
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from wos import scroll


# 1.获得chrome驱动器----------------------------------------------
def get_driver():

    # 修改页面加载策略, 注释这两行会导致最后输出结果的延迟, 即等待页面加载完成再输出
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    # 此步骤很重要, 设置为开发者模式, 防止被各大网站识别出来使用了Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # 隐式等待10秒
    return driver


# 2.1登录Altmetri网站---------------------------------------------
def login(driver):

    driver.get('https://www.altmetric.com/explorer/login')

    # 1)自动等登录~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 输入用户名
    name_input = driver.find_element_by_xpath('//input[@type="email"]')
    name_input.clear()  # 清空文本框
    name_input.send_keys('yajie.wang@hum.ku.dk')
    # 点击下一步
    next_btn = driver.find_element_by_xpath('//input[@type="submit"]')
    next_btn.click()
    # 输入密码
    pass_input = driver.find_element_by_xpath('//input[@type="password"]')
    pass_input.clear()  # 清空文本框
    pass_input.send_keys('qhq0318wyj0131')
    # 点击登录
    login_btn = driver.find_element_by_xpath('//input[@type="submit"]')
    login_btn.click()


# 2.2获得推特用户信息-----------------------------------------------
def get_tw_user(driver, url, file_name):

    print('page url: ', url)
    driver.get(url)

    # Note:设置滚动方式(最重要!!!)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    scroll.smoot_scroll(driver)

    # 获取推特用户信息~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    article_list = driver.find_elements_by_xpath(
        '//section[@class="post-list"]/article')
    for article in article_list:
        twt_id = article.find_element_by_xpath('./a/div/div[3]/div[2]').text
        name = article.find_element_by_xpath('./a/div/div[3]/div[1]').text
        # Note:过滤掉name中的表情符号并将其翻译为英文
        # name = filter_emoji(name)
        # name = Translator().translate(name).text
        twt_url = article.find_element_by_xpath('./a').get_attribute('href')
        tweet = article.find_element_by_xpath('./div[1]/p').text
        tweet = tweet.replace('\n', '')
        if tweet.startswith('RT'):
            rt = 'true'
        else:
            rt = 'false'
        twt_time = article.find_element_by_xpath('./time/a').text
        user_infor = [twt_id, name, twt_url, rt, twt_time, tweet]
        save_user_infor(user_infor, file_name)


# 过滤表情等特殊符号
def filter_emoji(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


# 3.获得所有推文链接-----------------------------------------------
def get_url_queue(driver, url):
    # 先装载页面
    driver.get(url)
    url_queue = Queue()
    try:
        page_cells = driver.find_elements_by_xpath(
            '//div[contains(@class, "top")]/div[@class="pagination_page_links"]//a[not(@class)]'
        )
        last_page = page_cells[-1].text
        print('len(page_cells)', len(page_cells), 'last_page: ', last_page)
        for i in range(1, int(last_page) + 1):
            url_queue.put(url + '/page:{}'.format(i))
    except Exception:
        print('one page........................')
        url_queue.put(url)
    finally:
        return url_queue


# 4.1用户信息保存为CSV格式---------------------------------------------
def save_user_infor(user_infor, file_name):
    mutex = threading.Lock()  # 多个线程共享文件, 要加锁
    mutex.acquire()
    if os.path.exists(file_name):
        # 以追加模式添加文件对象
        with open(file_name, 'a') as f:
            writer = csv.writer(f)
            # 填入用户信息:[twt_id, name, twt_url]
            writer.writerow([
                user_infor[0], user_infor[1], user_infor[2], user_infor[3],
                user_infor[4], user_infor[5]
            ])
    else:
        # 先填入表头
        with open(file_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['twt_id', 'name', 'twt_url', 'RT', 'Time', 'tweet'])
            # 再填入用户信息:[twt_id, name, twt_url]
            writer.writerow([
                user_infor[0], user_infor[1], user_infor[2], user_infor[3],
                user_infor[4], user_infor[5]
            ])
    mutex.release()


# 4.2用户推特保存为CSV格式---------------------------------------------
def save_tw_infor(file_name, tw_csv, save_csv):
    # 以追加模式添加文件对象
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
        next(reader)
        tw_file = open(save_csv, 'w', encoding='utf-8-sig', newline='')
        tw_writer = csv.writer(tw_file)
        tw_writer.writerow([
            'No', 'title', 'twitter mentions', 'tweets', 'retweets',
            'citations'
        ])
        for row in reader:
            no = row[0]
            title = row[2]
            tw_mens = int(row[30])
            cits = int(row[44])
            if tw_mens > 0:
                with open(tw_csv.format(no),
                          'r',
                          encoding='utf-8-sig',
                          newline='') as alt_file:
                    alt_reader = csv.reader(alt_file)
                    # Note:不读标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
                    next(alt_reader)
                    retw_list = [
                        alt_row for alt_row in alt_reader
                        # csv中要转为string
                        if str(alt_row[3]) == 'true'
                    ]
                    retws = len(retw_list)
                    print('retws: ', retws)
                tws = tw_mens - retws
                tw_writer.writerow([no, title, tw_mens, tws, retws, cits])
            else:
                tw_writer.writerow([no, title, 0, 0, 0, cits])
        tw_file.close()


# 5.基于队列进行数据爬取-----------------------------------------------
def run(paper_frag):
    driver = get_driver()
    # 1.登录altmetric并获取所有重推页面链接~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    login(driver)
    # Note:停顿3秒,不是登录状态不能获取
    time.sleep(3)
    while paper_frag:
        item = paper_frag.pop()
        file_name = '/Users/moqi/Altmetric/journal/joi-clc-tw/{}.csv'.format(
            item[0])
        print(item[0], item[1])
        url_queue = get_url_queue(driver, item[1])
        while not url_queue.empty():
            url = url_queue.get()
            get_tw_user(driver, url, file_name)


# 6.多线程爬取推文作者内容----------------------------------------------
def thrd_run(paper_list, thrd_no):

    thrd_list = []
    # 将paper_list切分为thrd_no,每块并发爬取
    paper_frags = chunks(paper_list, thrd_no)
    for i in range(len(paper_frags)):
        # Note:一个参数后面跟一个","
        thrd = threading.Thread(target=run, args=(paper_frags[i], ))
        thrd.start()
        thrd_list.append(thrd)
    for thrd in thrd_list:
        thrd.join()


# 将arr分为m块,自动分(尽可能平均)
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


if __name__ == '__main__':

    # paper_list = []
    # jou_csv = '/Users/moqi/Altmetric/journal/Journal of Informetrics.csv'
    # # Note:'utf-8-sig'去除'/u'
    # with open(jou_csv, 'r', encoding='utf-8-sig', newline='') as f:
    #     reader = csv.reader(f)
    #     # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     next(reader)
    #     for row in reader:
    #         index = row[0]
    #         # Note:若推特数或引用数为0则跳过
    #         # if int(row[30]) == 0 or int(row[44]) == 0:
    #         if int(row[30]) == 0:
    #             continue
    #         tw_page = row[45] + '/twitter'
    #         paper_list.append([index, tw_page])

    # # 2.多线程爬取所有页面中的推特用户~~~~~~~~~~~~~~~~~~~~~
    # thrd_run(paper_list, 3)

    # save_tw_infor(
    #     '/Users/moqi/Altmetric/journal/Information Processing & Management.csv',
    #     '/Users/moqi/Altmetric/journal/ipm-clc-tw/{}.csv',
    #     '/Users/moqi/Altmetric/journal/ipm-tw.csv')

    # save_tw_infor('/Users/moqi/Altmetric/journal/Journal of Informetrics.csv',
    #               '/Users/moqi/Altmetric/journal/joi-clc-tw/{}.csv',
    #               '/Users/moqi/Altmetric/journal/joi-tw.csv')

    save_tw_infor('/Users/moqi/Altmetric/journal/Scientometrics.csv',
                  '/Users/moqi/Altmetric/journal/sci-clc-tw/{}.csv',
                  '/Users/moqi/Altmetric/journal/sci-tw.csv')
