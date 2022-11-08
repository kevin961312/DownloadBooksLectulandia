from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import time
import urllib.request
import urllib.parse


class DownloadBooksLectulandia:
    def __init__(self, authors, numberPages=1, timeSleepDownload=15):
        self.authors = authors
        self.numberPages = numberPages
        self.timeSleepDownload = timeSleepDownload
        
    def __GetSearchPage(self, url):
        SearchUrl = urllib.parse.unquote(url)
        SearchPage = requests.get(SearchUrl)
        SearchPage.encoding = 'latin1'
        Soup = BeautifulSoup(SearchPage.text, "lxml", from_encoding="latin1")
        return Soup
    
    def __DownloadByBook(self, varJavascript):
        if (len(varJavascript)!=0):
            UrlDownloadPage = urllib.parse.unquote("https://www.antupload.com/file/" + str(varJavascript).split('=')[1].strip()[1:10])
            Driver = webdriver.Chrome (executable_path="./chromedriver.exe")
            Driver.get(UrlDownloadPage)
            Driver.find_element("xpath","//a[@id='downloadB']").click()
            time.sleep(self.timeSleepDownload)
            Driver.quit()
    
    def Download(self):
        for author in self.authors: 
            page = 1
            while (page <= self.numberPages):
                SubheadingsLectulandia = self.__GetSearchPage(f"https://ww2.lectulandia.com/autor/{author}/page/{page}/").find_all("a", class_="title",href=True)
                if (len(SubheadingsLectulandia) != 0):
                    for htmlhref in SubheadingsLectulandia:
                        SubheadingsSearchLectulandiaUrl = self.__GetSearchPage(f"https://ww2.lectulandia.com{htmlhref['href']}").find_all(href=re.compile("download.php"))
                        SubheadingsPageRedirection = self.__GetSearchPage(f"https://ww2.lectulandia.com{SubheadingsSearchLectulandiaUrl[0]['href']}").find_all('script')
                        VarJavascript= re.findall(r'var linkCode = .*;', str(SubheadingsPageRedirection[-1]))
                        self.__DownloadByBook(VarJavascript)
                    page +=1
                else:
                    break