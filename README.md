# KKDAY_django_scrapyers
python 爬蟲網站資料 將結果放在django 自製網站
程式透過物件導向(Object-oriented)方法製作 

        
## demo

https://github.com/Estherchao-tw/KKDAY_and_Klook_django_scrapyers/assets/74496288/396037c2-0d81-4898-b689-4b2bf3eacb6b



## 建立django 應用程式
### settings.py (in trip folder)


**Application definition**

為了要讓專案主程式能夠認得應用程式，就需要開啟專案主程式下的settings.py檔案，在NSTALL_APPS的地方，加入應用程式的設定檔

        
    'tickets.apps.TicketsConfig',

## 建立Djanog 應用程式網址
### urls.py (in tickets pockets)
設定一組網址，讓使用者透過這個瀏覽器來進行請求(Request)
ex: https://127.0.0.1:80/index

        from django.urls import path
        from . import views

        app_name = "tickets"
 
        urlpatterns = [
            path('',views.index, name='index')
        ]
        
### urls.py (in trip pockets，專案主程式資料夾)
 Including another URLconfiguration <br>
    1. Import the include() function: from django.urls import include, path <br>
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')) <br>

        # URLconf
        from django.contrib import admin
        from django.urls import path, include
        
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include("tickets.urls")),
        ]

>cmd excute: <br>
>>        python manage.py run server<br>
>chrome browser excute:<br>
>>        http://127.0.0.1:8000/tickets


## 建立爬蟲
開發KKDAY 網站的一日遊票券資訊
每個要爬蟲的網站都會有不同的方法，那每個爬蟲的方法我們就把它放在一個class，越多網站就越多class 去擴充網站要顯示的資訊。<br>
### scrapers.py(in tickets pockets)
因為顯示網站的網頁我們設定在tickets 資料夾當中，我們要新增scrapers.py <br>
定義一個網站抽象類別，其中包含城市名稱(city_name)屬性及爬取(scrape)抽象方法

**libraries**

        from abc import ABC, abstractmethod
        from datetime import datetime
        from bs4 import BeautifulSoup
        import time
        import json
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import pandas as pd


*票券網站抽象類別*
        class Website(ABC):
            
            def __init__(self,city_name):
                self.city_name = city_name # 城市名稱屬性


            @abstractmethod
            def scrape(self):  #爬取票券抽象方法
                pass

*kkday網站*
用selenium 連接網路，定義搜尋的城市名，如果city_name 不是空的，就可以進行爬蟲，將資料存在dict


    class Kkday(Website):
        #方法:爬蟲主程式
        def scrape(self):
        
            #使用selenium連接网络
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
                
            return result
        time.sleep(2)

打包的資料在 result.append裡面，回傳到index.html

                
## 建立fronted templete django 樣板
### index.html(in tickets/templates/tickets folder)
將post加入 template<br>
建立前端資料POST傳入ticlets/view.py>scrape.py 中的class ，打包資料，轉成tickets 物件回傳到前端網頁

        <form id ="city" actin="" method="Post">
          {% csrf_token %}
          <input name="city_name" placeholder="請輸入城市的中文名稱">
          <input type="submit" value="查詢">
        </form>
        
   *{% csrf_token %} 避免跨站請求攻擊*     
        
        
### views.py
將傳送過來的城市名稱關鍵字(city_name)，傳入Python網頁爬蟲的類別(Class:kkday)中，search city 對應的代號，進行scrapy，並且將爬取的結果打包成tickets物件(Context)回傳給網頁
<br>

**Libraries**

        from django.shortcuts import render
        from django.template import loader
        from .scrapers import Kkday

**define**

        def index(request):


        kkday = Kkday(request.POST.get("city_name"))


        context = {
            "tickets" : kkday.scrape()
        }

    return render(request, "tickets/index.html",context)


### index.html
**show table**
        
        <table class="table">
          <thead>
            <tr>
              <th>票券名稱</th>
              <th>價格</th>
              <th>最早可使用日期</th>
              <th>評價</th>
              <th>來源網站</th>
            </tr>
          </thead>
          <tbody>
            {% for ticket in tickets %}
            <tr>
              <td>
                <a href="{{ticket.link}}" target="_blank">{{ ticket.title }}</a>
              </td>
              <td>{{ticket.price}}</td>
              <td>{{ticket.date}}</td>
              <td>{{ticket.star}}</td>
              <td><img src={{ticket.source}} style="width: 32px;height: 32px;"/></td>
            </tr>
        
            {% endfor %}
          </tbody>

📝 **Note:** Only scrapy kkdaywebside 
