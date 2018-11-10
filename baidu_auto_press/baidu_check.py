# -*- coding:UTF-8 -*-

from selenium import webdriver
import time
import re
import json
from selenium.common.exceptions import NoSuchElementException


class AutoSearchAndPress:
    def __init__(self, configFileName='config.json'):
        self.browser = self.InitDirver()
        self.rootHand = self.browser.current_window_handle

        with open(configFileName, encoding='UTF-8') as file:
            str_dirct = json.load(file)

            self.keywordList = str_dirct['searchWord']
            self.filterWeb = str_dirct['filterWebAddr']
            self.webStopTime = str_dirct['webStopTime']
            self.maxPageNum = str_dirct["maxPageNum"]
            self.currWebNum = str_dirct["currWebNum"]


    def InitDirver(self):
        browser = webdriver.Chrome() 
        browser.maximize_window()
        browser.get("https://www.baidu.com")
        time.sleep(1)
        return browser

    #搜索百度
    def StartSearchBaidu(self, keyWord):
        obj = self.browser.find_element_by_xpath('//*[@id="kw"]')
        obj.clear()
        obj.send_keys(keyWord)

        #搜索
        self.browser.find_element_by_xpath('//*[@id="su"]').click()

    def IsWebNeedFilter(self, webAddr):
        for addr in self.filterWeb:
            if webAddr.find(addr) > 0:
                return True
        return False


    def IsXpathElementExist(self, xpath):
        all = self.browser.find_elements_by_xpath(xpath)
        if len(all) > 0:
            return True

        return False

    def IsTagElementExist(self, parentObj, serachName):
        all = parentObj.find_elements_by_tag_name(serachName)
        if len(all) > 0:
            return True

        return False

    def GetWebExistXpath(self, webIndex):

        firstNum = 0
        divNum = 0

        while(firstNum < 9):
            firstNum += 1
            divNum = 0
            while(divNum < 9):
                divNum += 1
                xpathStr = '//*[@id="%d00%d"]/div[%d]/h3/a'%(firstNum, webIndex, divNum)
                if self.IsXpathElementExist(xpathStr) == True:
                    return xpathStr
        return ""

    def PressSearchWebType(self):
        
        num = 0
        #先点击3001开始的10个
        while num < 10:
            num += 1

            xpathStr = self.GetWebExistXpath(num)
            if xpathStr == "":
                continue

            print("ok xpath:", xpathStr)
            xpathObj = self.browser.find_element_by_xpath(xpathStr)

            #过滤.......
            urlAddr = xpathObj.get_attribute("data-landurl")
            if self.IsWebNeedFilter(urlAddr):
                continue

            #点击
            time.sleep(2)
            xpathObj.click()
                            

            time.sleep(self.webStopTime )

            #关闭打开的窗口
            self.CloseNotRootWeb()

    def NextPage(self):
        self.browser.find_element_by_xpath('//*[@id="page"]/a[10]').click()

    #点击网页
    def PressSearchedWeb(self):

        num = 0
        while num < self.maxPageNum:
            time.sleep(3)

            self.PressSearchWebType()
            self.NextPage()

            num += 1


    #关闭打开的网页
    def CloseNotRootWeb(self):
        
        handles = self.browser.window_handles
        for newhandle in handles:
            if newhandle != self.rootHand:
                self.browser.switch_to_window(newhandle)
                self.browser.close()
                self.browser.switch_to_window(self.rootHand)

    def Start(self):

        while True:
            for keyWord in self.keywordList:

                #self.StartSearchBaidu(keyWord)
                #self.PressSearchedWeb()

                try:
                    self.StartSearchBaidu(keyWord)
                    self.PressSearchedWeb()
                except:
                    time.sleep(10)
                    print("any error,please wait 10s")
                    self.browser.get("https://www.baidu.com")

if __name__ == "__main__":
    auto = AutoSearchAndPress("config.json")
    auto.Start()

    print("game over")