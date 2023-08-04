from abc import ABC, abstractmethod
from datetime import datetime
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
#定義一個網站抽象類別，其中包含城市名稱(city_name)屬性及爬取(scrape)抽象方法

# 票券網站抽象類別
class Website(ABC):
    
    def __init__(self,city_name):
        self.city_name = city_name # 城市名稱屬性


    @abstractmethod
    def scrape(self):  #爬取票券抽象方法
        pass
    

 # KKday 網站
 # 
 # 
 # 
 # 
 # 
class Kkday(Website):

    #方法:爬蟲主程式
    def scrape(self):
        
        #使用selenium连接网络
        def selenium_chrome(url):
            option = Options()
            #使用無痕模式
            option.add_argument("--incognito")
            # 打開chrome網頁
            browser = webdriver.Chrome(options=option)
            browser.get(url)

            return browser

        def find_city_id(cityName):

        # 如果城市名 等於 cityList當中的城市，可以得知其城市的 i,j,k
        #返回 id 給網址
            
            with open("./search.json") as all_script:
                    script = json.load(all_script)
                    data = script['search']['areaData']['zh-tw']['continents']
                    N = len(data) #計算有多少洲:8
                    cityList =[]
                    # 將每個城市的id and name 抓出來
                    for i in range(0,N-1):
                        countries = data[i]['countries']
                        J = len(countries) # 計算每一洲(區域)有幾個國家:27
                        # print("J :",J)
                        for j in range(0,J-1):
                            cities = countries[j]['cities']
                            K = len(cities) # 計算每個國家的城市有幾個
                            # print("K:",K)
                            for k in range(0,K-1):
                                id = data[i]['countries'][j]['cities'][k]['id']
                                name = data[i]['countries'][j]['cities'][k]['name']

                                if cityName == name:
                                    print(i,j,k)
                                    print(id)
                                    return id
                                
                            
                            cityList.append([id,name])

        # 如果city_name 不是空的
        if find_city_id(self.city_name):
            result = [] #回傳資料#收集data
            url = "https://www.kkday.com/zh-tw/product/productlist?page=1&city={}&cat=TAG_4_4&sort=prec".format(find_city_id(self.city_name))
            browser = selenium_chrome(url)

            soup = BeautifulSoup(browser.page_source, 'html.parser',on_duplicate_attribute='ignore')
            # 取得資料dict
            data = soup.find_all('div',{'class':"product-listview search-info gtm-prod-card-element"})

            # 爬取想要的資料
            #　標題、連結、價格、可使用日期、評分
            for detail in data:
                title = detail.find('span',{'class':"product-listview__name"}).text
                date = detail.find('div',{'class':"product-time-icon"}).text[-18:-1].replace('\t','').replace('\n','')
                price = detail.find('div',{'class':"product-pricing"}).text.replace('\t','').replace('\n','')
                star = detail.find('span',{'class':"text-grey-light"})
                link= detail.find('a').get('href')
                source = "https://www.kkday.com/favicon.png"

                if star == None:
                    print('none:',type(star))
                else:
                    star = star.text
                    print(type(star))
                # 資料疊加
                result.append(dict(title= title,date=date,price=price,star=star,link=link,source=source))
                
            # print(result,type(result),"success")
            # type要是 list 才可以儲存到pandas
            # pandas 表格化
            # df = pd.DataFrame(result,columns = ["活動名稱","價格","星級","預定日期","連結","品牌"])
            # print(df)
            return result
        time.sleep(2)
        # browser.close(); #closes the browser

    




# Klook

