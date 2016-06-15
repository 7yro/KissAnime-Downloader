# import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ConfigParser
import time
import datetime
import os
# import requests
# import re
# from contextlib import closing
import subprocess
# from selenium.common.exceptions import NoSuchElementException

class episodeList:
    def main(self):
        print "Started at "+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        section = "Kissanime"
        config = self.getConfig()
        user = config.get(section, "username")
        passwrd = config.get(section, "password")
        length = config.get(section, "length")
        qlty = config.get(section, "quality")
        IDM_path = config.get(section, "IDM_location")
        chromeDriverLoc = config.get(section, "chromedriver_location")
        #os.environ["webdriver.chrome.driver"] = chromeDriverLoc
        browser = webdriver.Chrome(chromeDriverLoc)  # Get local session of chrome
        browser.get("https://kissanime.to/Login")  # Load page
        os.chdir(IDM_path)
        time.sleep(10)  # Let the page load, will be added to the API
        assert "Login" in browser.title
        userName = browser.find_element_by_name("username")  # Find the username box
        userName.send_keys(user)
        passWord = browser.find_element_by_name("password")
        passWord.send_keys(passwrd + Keys.RETURN)
        print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " Logged in"
        found = "Not found"
        while found == "Not found":
            keyword = raw_input("Enter search string: ")
            search = browser.find_element_by_id("keyword")
            search.send_keys(keyword + Keys.RETURN)
            time.sleep(5)
            dictUrl = {}
            if "Find anime" in browser.title:
                i = 3
                found = browser.find_elements_by_xpath('//*[@id="leftside"]/div/div[2]/div[2]')[0].text
                while i > 2 and found != "Not found":
                    try:
                        table = browser.find_element_by_xpath('//*[@id="leftside"]/div/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[1]/a')
                        dictUrl[i-2] = table.get_attribute("href")
                        i += 1
                    except:
                        break
                if found != "Not found":
                    for k in dictUrl:
                        print str(k)+" : "+dictUrl[k]
                    k = raw_input("Enter Selection: ")
                    url = dictUrl[int(k)]
                    browser.get(url)
                    time.sleep(3)
                else:
                    print found
            else:
                break
        browser.get(browser.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[last()]/td[1]/a").get_attribute("href"))
        linksList = []
        print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " Started retrieving links"
        j = 1
        while j <= length:
                try:
                    HD = browser.find_element_by_xpath(".//div[@id='divDownload']/a["+qlty+"]")
                except:
                    print "Can't find the required quality for "+browser.title()
                    continue
                name = browser.title.replace(" ", "%20")
                link = HD.get_attribute("href")+"&title="+name
                linksList.append(link)
                subprocess.call(["IDMan.exe", '/d', link, '/a'])
                if j == 1:
                    subprocess.call(["IDMan.exe", '/s'])
                j += 1
                try:
                    next = browser.find_element_by_id("btnNext")
                    next.click()
                except:
                    print "Reached end of series."
                    break
        browser.close()
        print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " Done retrieving links and adding to IDM queue."

    def getConfig(self):
        configUtil = ConfigUtil('./script.cfg')
        return configUtil.getAllProperties()


class ConfigUtil:
    configFile = "script.cfg"

    def __init__(self, file):
        self.configFile = file

    def getProperty(self, section, key):
        config = self.getAllProperties()
        val = config.get(section, key)
        return val

    def getAllProperties(self):
        config = ConfigParser.ConfigParser()
        config.read(self.configFile)
        return config


if __name__ == '__main__':
    episodeList().main()

'''with open(fileLoc, 'a') as links:
            for i in linksList:
                links.write(i)
                links.write('\n')
                print i
                name = re.search(r"&title=(.*)", "%s" % i).group(1)
                name = name.replace("%20", " ")

                #print name
                #print "get url"
                with closing(requests.get(i, stream=True)) as r:
                    #r = requests.get(i,stream=True)
                    #print r
                    video = open(name+".mp4", 'wb')
                    #print "start"
                    k = 1
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        if chunk:
                            print k
                            video.write(chunk)
                            k += 1
                    print "end"
                    video.close()'''