from selenium import webdriver
import mytoken as token

# headless mode
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

browser = webdriver.Firefox(options = options)

# login
browser.get(r'http://academic.tsinghua.edu.cn/')
browser.find_element_by_name('userName').send_keys(token.username)
browser.find_element_by_name('password').send_keys(token.pswd)
browser.find_element_by_id('logining').click()

# enter choose lesson page
browser.get(r'http://zhjw.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do?m=kkxxSearch&p_xnxq=2018-2019-2')
with open('page1.html', 'w') as f:
    f.write(browser.page_source)

# all pages
pages = 2
total_pages = 226
for i in range(2,total_pages+1):
    browser.find_element_by_id('nextpage').click()
    with open('page%s.html'%pages, 'w') as f:
        f.write(browser.page_source)
    print('%ssucceed!'%pages)
    pages = pages + 1
