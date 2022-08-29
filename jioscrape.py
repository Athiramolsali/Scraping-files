# import re
# from urllib.parse import urlparse
# import urllib.request
# import pandas as pd
import requests
# from urllib.request import urlopen as uReq
# import csv
from bs4 import BeautifulSoup as soup
# import os.path
# import logging
# import substring
# import requests
from bs4 import BeautifulSoup
# import csv
# from scrapy.selector import Selector

site = 'https://db-ip.com/137.97.119.158'

data = []

html_doc = requests.get(site)
if html_doc.status_code == 200:
    datas = {}
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    #print(soup)
    geo_location = soup.find("div", {"class":"sub purple" }).text
    ip_address= soup.find("h1", {"class": "main"}).text
    datas[geo_location] = ip_address
    description = soup.find("div", {"class":"title head" })
    for des in description.findAll('p'):
        datas["Description"] = des.text


#     tab_headers = []
#     tab_values = []
#     table_lis = soup.findAll("table", {"class": "table light"})
#     for t in soup.findAll("table", {"class": "table light"}):
        
#         for table_list in t.findAll("th"):
#             table_heads = table_list.text
#             #table_heads = table_list.
#             tab_headers.append(table_heads)
#             #print(tab_headers)
    

        
#     for t in soup.findAll("table", {"class": "table light"}):
#         for table_values  in t.findAll("td"):
#             table_values = table_values.text
#             table_values = "".join(table_values.split())
#             tab_values.append(table_values)
#     #print(tab_values)


#     dataDictionary = {};
#     for index in range(len(tab_headers)):
#         theheader = tab_headers[index]
#         theData = tab_values[index]
#         dataDictionary[theheader] = theData
#     #print(dataDictionary)

#     datas.update(dataDictionary)
#     #print('Updated dictionary:',datas)


# ############
# heads = []
# values = []
# table_lis = soup.findAll("table", {"class": "table light tcol-33 mb-3"})
# for t in soup.findAll("table", {"class": "table light tcol-33 mb-3"}):
    
#     for tab_head in t.findAll("th"):
#         tab_head = tab_head.text
#         heads.append(tab_head)
#         #table_heads = table_list.
#         #tab_headers.append(table_heads)
# #print(heads)


    
# for t in soup.findAll("table", {"class": "table light tcol-33 mb-3"}):
#     for table_val  in t.findAll("td"):
#         table_val = table_val.text
#         table_val = "".join(table_val.split())
#         values.append(table_val)
# #print(values)


# dataDictionary1 = {};
# for index in range(len(heads)):
#     thekeyheader = heads[index]
#     theData = values[index]
#     dataDictionary1[thekeyheader] = theData


# #print(dataDictionary1)
# #print(datas)
# datas.update(dataDictionary1)



# estimated = soup.find("table", {"class":"table light tcol-33 mb-3" }).text









tr_list = []
table_data = soup.findAll("table", {"class": "table light"})
# for tr in  table_data:
#     # for td in tr.find("td"):
#         tr_list.append(tr.find_all('tr'))

l2 = list(map(lambda tr: tr_list.append(tr.find_all('tr')), table_data))
# print((tr_list[0]),type(tr_list))

l3 = [ (list(map(lambda i: datas.update({i.find("th").text:i.find("td").text}), tr_list[x]))) for x in range(len(tr_list))]


# for i in tr_list[1]:
#     # print(i.find("th").text)
#     datas.update({i.find("th").text:i.find("td").text})
    # list(map(lambda tr: print(tr.text), i))
print(datas)
# for td in range(len(tr_list)):
#     print(tr_list[td][td])
#for td in tr_list

    
            

       


    




