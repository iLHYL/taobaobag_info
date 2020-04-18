# import time
# from selenium.webdriver import Chrome,ChromeOptions
# #设置无头模式，爬取不需打开网页
# option = ChromeOptions()
# #option.add_argument("--headless")
# option.add_argument("--no-sandbox")
#
# url = "https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200413&ie=utf8"
# #创建浏览器对象
# browser = Chrome(options = option) #如果当前目录下有对应驱动，就不需要传参数，否则需要传入路径参数
# browser.get(url)
# # print(browser.page_source)
# #获取要点击的按钮并点击
# # more_button = browser.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-5_32AY4F.VirusHot_1-5-5_2RnRvg > section > div')
# # more_button.click()
# # time.sleep(1) #等待一秒
# # res = browser.find_elements_by_xpath(r'//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
# # for i in res:
# #     print(i.text)
#
# browser.close()
import pandas as pd
import time
from selenium.webdriver import Chrome,ChromeOptions
#创建selenium对象
option = ChromeOptions()
option.add_argument("--no-sandbox")
url = 'https://www.taobao.com/'
browser = Chrome(options = option)
browser.implicitly_wait(20)
browser.get(url)
#获取单页所有商品简要信息，包括价格，商品名，销售量，店铺，地区
def getInfo(browser):
    thisPageInfo = []
    for i in range(44):
        selector = '#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child('+str(i+1)+') > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew'
        a =  browser.find_element_by_css_selector(selector)
        res = a.text
        thisPageInfo.append(res)
    return thisPageInfo
#获取设置页数的商品信息
def getPagesInfo(pagenum,broweser):
    res = []
    for i in range(pagenum):
        print('获取第'+str(i+1)+'页信息')
        time.sleep(3)
        temp = getInfo(browser)
        res.extend(temp)
        print('第'+str(i+1)+'页信息获取完毕')
        time.sleep(2)
        nextPageButton = browser.find_element_by_css_selector('#mainsrp-pager > div > div > div > ul > li.item.next > a')
        nextPageButton.click()
        print('已跳转到下一页')
    return res

# x = getPagesInfo(50,browser)
#分割数据
def dataclear(str):
    a = str.split('\n')
    res = a[0:3]
    return res
#将目标数据分割
def finalData(alist):
    res = []
    for i in alist:
        temp = dataclear(i)
        res.append(temp)
    return res
#将数据保存为csv
def save_csv(data,csvname):
    name = ['price','order_num','product_info']
    csv = pd.DataFrame(columns=name,data=data)
    csv.to_csv(csvname,encoding='utf-8')