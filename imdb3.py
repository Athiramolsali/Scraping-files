import requests
from bs4 import BeautifulSoup
import csv
from scrapy.selector import Selector

site = 'https://www.imdb.com'
top = '/chart/top'
movies = []

html_doc = requests.get(site+top)
if html_doc.status_code == 200:
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    titleColumn = soup.find_all("td", {"class":"titleColumn" })
    for i, title in enumerate(titleColumn, start=1):
        movie_link = title.find("a").get("href")
        movies.append(movie_link)

movies_data = []

for idxer, p in enumerate(movies, start=0):
    html_doc = requests.get(site+p)
    movie = {}
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        title = soup.find("div", {"class": "title_wrapper"}).h1.get_text()
        rating = soup.find("span", {"itemprop": "ratingValue"}).get_text()
        year = soup.find('span', {'id': 'titleYear'}).get_text()

        movie["Movie"] = title
        movie["Rating"] = rating
        movie['Release Year'] = year

        #Budget
        sel = Selector(html_doc)
        budget = ' '.join(sel.css(".txt-block:contains('Budget')::text").extract()).strip()
        movie['Budget'] = budget
        #Country
        country = ' '.join(sel.css(".txt-block:contains('Country')::attr(href)").extract()).strip()
        movie['Country'] = country
        print(country)
        #genre Genres
        genres= ' '.join(sel.css(".txt-block:contains('Genres')::text").extract()).strip()
        movie['Genres'] = genres
        #print(genres)

        #Language
        language = ' '.join(sel.css(".txt-block:contains('Language')::text").extract()).strip()
        movie['Language'] = language

        #Plot
        plot =  ' '.join(sel.css(".txt-block:contains('Plot Keywords')::text").extract()).strip()
        movie['Plot'] = plot


        #Runtime
        #runtime = ' '.join(sel.css(".txt-block:contains('Runtime')::text").extract()).strip()
        #movie['Runtime'] = runtime
        #print(runtime)
        #run = soup.findAll("h4",{"text":"Runtime:"})[0].parent
        #run_time = run.text.split()[1]
        #runs =  run.text.split()[2]
        #run_join = run_time + runs
        #movie['Duration'] = run_join

        #summery
        summerys={}
        summery = soup.find("div", {"class": "summary_text"}).get_text()
        movie["Summery"] = summery

        #meta titles
        metas = {}
        meta = soup.find_all("div", {"class": "credit_summary_item"})

        for m in meta:
            values = []
            for a in m.find_all('a'):
                values.append(a.text)
            value = ", ".join(values)
            movie[m.find("h4").get_text()] = value
            #print(value)

        #genres
            #genres = []
            #html_genre =((soup.findAll("div", itemprop="genre"))[0])
            #for genre_tags in html_genre.find_all("a"):
                #for genre in genre_tags:
                    #genres.append(genre.string)
                    #print(genres)


        #budget
            #budget =  soup.findAll("h4", text="Budget:")[0].parent
            #bud_text = budget.text.split("Budget:")[1]
            #bud = bud_text.split("$")
            #print(bud)


        #Cast
        casts = {}
        cast_list = soup.find("table", {"class": "cast_list"})
        for idx, row in enumerate(cast_list.find_all("tr"), start=0):
            if idx != 0 :
                if len(row.find_all("td")) == 4:
                    key = row.select_one("td:nth-child(2)")
                    #value = row.select_one("td:nth-child(4)")
                    if key.find("a") is None:
                        v_key = key.get_text()
                    else:
                        v_key = key.find("a").get_text()

                    movie["Cast " + str(idx)] = v_key.strip()

        #print(movie)

        #print(movie.values())

        #print(movie.keys())
        if idxer == 0:
            movies_data.append(movie.keys())
        movies_data.append(movie.values())

with open("imdb3.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(movies_data)
    f.close()