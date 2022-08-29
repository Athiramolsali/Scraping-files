import requests
from bs4 import BeautifulSoup
import csv
tds = []
r = requests.get('https://www.imdb.com/title/tt7286456/')
if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html.parser')
    title_tags = soup.find("div",{"class":"title_wrapper"})
    credit_summary_tags = soup.find_all("div",{"class":"credit_summary_item"})
for cst in credit_summary_tags:
    if cst.h4.text:
             print(cst.a.text)
#title tags
title_tags = title_tags.h1.text
print(title_tags)
#castlist
divs = soup.find_all("table",{"class":"cast_list"})
for div in divs:
 rows = soup.findAll("tr", {'class': ['odd', 'even']})
for tr in rows:
    for data in tr.findAll("td"):
            print(data.get_text())
#links = [a.attrs.get('href') for a in soup.select('td.a')]
#movie = (' '.join(data.get_text().split()).replace('.', ''))
#print(movie)

#print("Name:" + list)
tds.append([data.get_text()])
#print(tds)

#header = "Director, Name, Cast"+"\n"
#open csv
with open("imdb.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(tds)

#table
#divs = soup.find_all("table",{"class":"cast_list"})
#for div in divs:
#rows = div.findAll("tr")
#for row in rows:
#tds.append(row.findAll("td",{"class":"character"}))

#tds = tds.text
#print(tds)


#phone = str[tds]
#phone = phone.replace("<td>", "").replace("</td>", "").strip()
#phone = phone.text
#print(phone)


