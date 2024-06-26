#weather
'''import requests 
from bs4  import BeautifulSoup
url='https://www.timeanddate.com/weather'
res=requests.get(url).content
soup=BeautifulSoup(res,'html.parser')
data=soup.find('span',class_='my_city_city')
data1=soup.find('span',class_='my_city_temp')
data2=soup.find('span',class_='my_city_wtdesc')
city_element = soup.find('span', class_='my-city__city')
print(city_element.text,data1,data2)'''

'''url='https://www.timeanddate.com/'
res=requests.get(url).content
soup = BeautifulSoup(res, 'html.parser')
links=soup.find_all('a')
for link in links:
    print(link['href'])'''


'''import requests
from bs4 import BeautifulSoup
enter_search='chatrai'
url='https://www.timeanddate.com/weather/?query='+enter_search+''
res=requests.get(url).content
print(res)
soup=BeautifulSoup(res,'html.parser')
#print(soup.text)
data=soup.find_all('input',class_='picker-city__input')
print(data)
'''
#searching purpose 
'''import requests
from bs4 import BeautifulSoup
enter_search='mobiles'
url='https://www.flipkart.com/search?q='+enter_search+''
res=requests.get(url).content
#print(res)
soup=BeautifulSoup(res,'html.parser')
#print(soup.text)
data=soup.find_all('div',class_='KzDlHZ')
#print(data)

#-----vertical data--------
c=1
for item in data:
    print(c,'---',item.text)
    c+=1
#--------Horizontal data---------
data=soup.find_all('a',class_='WKTcLC')
for item in data:
    print(c,'-----',item.text)
    c+=1'''

#all images src 
'''import requests
from bs4 import BeautifulSoup
url='https://www.treehugger.com/the-most-amazing-waterfalls-in-the-world-4869333'
res=requests.get(url).content
#print(res)
soup=BeautifulSoup(res,'html.parser')
images=soup.find_all('img')
for img in images:
    print(img['src'])'''

#all links href
'''import requests
from bs4 import BeautifulSoup
url='https://www.treehugger.com/the-most-amazing-waterfalls-in-the-world-4869333'
res=requests.get(url).content
#print(res)
soup=BeautifulSoup(res,'html.parser')
links=soup.find_all('a')
for link in links:
    print(link['href'])'''
#getting data from multiple pages
'''import requests
from bs4 import BeautifulSoup
for i in range(1,11):
    #url='https://quotes.toscrape.com/page/'+str(i)+'/'
    url='https://www.flipkart.com/search?q=mobiles&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY&page='+str(i)
    res=requests.get(url).content
    soup=BeautifulSoup(res,'html.parser')
    #quotes=soup.find_all('span',class_='text')
    quotes=soup.find_all('div',class_='KzDlHZ')
    for quote in quotes:
        print(quote.text)
    print()
    print('Page_id:',i)'''

#title,div,id, tags data
'''import json, requests
from bs4 import BeautifulSoup
url='https://quotes.toscrape.com/'
res=requests.get(url).content
soup=BeautifulSoup(res,'html.parser')
title=soup.find('span',class_='text')
print(title.text)
tags=soup.find('div',class_='quote')
print('Tags:',tags.text)
#data=soup.find('script',id='lucky').text
#print(data)'''

#job search not working
'''import requests
from bs4 import BeautifulSoup
url='https://in.indeed.com/jobs?q=python+developer&l=Hyderabad%2C+Telangana&from=searchOnDesktopSerp&vjk=8c235a9d2feeae71'
res=requests.get(url).content
#print(res)
soup=BeautifulSoup(res,'html.parser')
\'''title=soup.find('span',title='Full Stack Developer')
location=soup.find('div',class_='jcss-1p0sjhy')
company=soup.find('h2',id_='jobTitle css-198pbd eu4oa1w0')
date=soup.find('span',id_='dateLabel')
print(soup.text)
print(title)
print(location)
print(date)\'''

data=soup.find_all('div',class_='jobsearch-JobCountAndSortPane')
for i in data:
    title=i.find('h1',class_='css-novqjp e1tiznh50')
    company=i.find('h2',id_='jobTitle css-198pbd eu4oa1w0')
    date=i.find('span',id_='dateLabel')
    print(soup.text)
    print(title)
    print(company)
    print(date)'''


#How to work with Api using in python
'''import requests
from bs4 import BeautifulSoup
city=input('enter the city name:')
url='https://openweathermap.org/'+city+''
res=requests.get(url).content 
#print(res)
soup=BeautifulSoup(res,'html.parser')
print(soup.text)'''