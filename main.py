import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

brand = []

def extract_brand():
  result = requests.get(alba_url)
  soup = BeautifulSoup(result.text, "html.parser")
  findbrand = soup.find(id="MainSuperBrand").find("ul", {"class":"goodsBox"}).find_all("li")
  global brand
  for i in range(len(findbrand)):
    brand.append(findbrand[i].find("a")["href"])
  brand = brand[:-3]

def extract_infos():
  extract_brand()
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for i in range(len(brand)):
    result = requests.get(brand[i])
    soup = BeautifulSoup(result.text, "html.parser")
    try:
      table = soup.find("div", {"id":"NormalInfo"}).find("table")
      jobs = table.find("tbody").find_all("tr")
      for i in range(len(jobs)):
        try:
          place = jobs[i].find("td",{"class":"local first"}).get_text().replace(u'\xa0', u' ')
          title = jobs[i].find("td",{"class":"title"}).find("span",{"class":"company"}).get_text()
          pay =  jobs[i].find("td",{"class":"pay"}).find_all("span")
          pay = str(pay[0].get_text()) + str(pay[1].get_text())
          time = jobs[i].find("td",{"class":"data"}).get_text()
          date = jobs[i].find("td",{"class":"regDate last"}).get_text()
          dic = {'place': place, 'title':title, 'time':time, 'pay':pay, 'date':date}
          writer.writerow(dic.values())
        except:
          continue
    except:
      continue

extract_infos()