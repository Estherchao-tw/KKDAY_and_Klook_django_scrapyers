from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from datetime import datetime

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


# Klook


