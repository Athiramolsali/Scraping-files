
import requests
from bs4 import BeautifulSoup as soup
#import
from bs4 import BeautifulSoup


site = 'https://db-ip.com/'
ip = '137.97.119.158'

def Scraping(ip):
    data = []
    url = 'https://db-ip.com/' + ip
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        datas = {}
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        geo_location = soup.find("div", {"class":"sub purple" }).text
        ip_address= soup.find("h1", {"class": "main"}).text
        datas[geo_location] = ip_address
        description = soup.find("div", {"class":"title head" })
        for des in description.findAll('p'):
            datas["Description"] = des.text    #description



    heads = []
    values = []
    table_lis = soup.findAll("table", {"class": "table light tcol-33 mb-3"})
    for t in soup.findAll("table", {"class": "table light tcol-33 mb-3"}):
        
        for tab_head in t.findAll("th"):
            tab_head = tab_head.text
            heads.append(tab_head)
            
    for t in soup.findAll("table", {"class": "table light tcol-33 mb-3"}):
        for table_val  in t.findAll("i"):            
            table_val = table_val.attrs["title"]
            table_val = table_val.strip('\n')
        
            values.append(table_val)



    dataDictionary1 = {};
    for index in range(len(heads)):
        thekeyheader = heads[index]
        theData = values[index]
        dataDictionary1[thekeyheader] = theData

    datas.update(dataDictionary1)



    tr_list = []
    table_data = soup.findAll("table", {"class": "table light"})

    l2 = list(map(lambda tr: tr_list.append(tr.find_all('tr')), table_data))

    l3 = [ (list(map(lambda i: datas.update({i.find("th").text:i.find("td").text.replace('\xa0', ' ').replace('\n', ' ')}), tr_list[x]))) for x in range(len(tr_list))]

    estimated= soup.find("span", {"class":"label badge-success" })  #Thread Level
    datas["Thread level"] = estimated.text
    return datas




scrapdetails = Scraping('137.97.119.158')
print(scrapdetails)




    
            

       


    




