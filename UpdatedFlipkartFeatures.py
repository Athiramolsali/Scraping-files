# Modified last on 09-09-2021
import re
from urllib.parse import urlparse
import urllib.request
import pandas as pd
import requests
from urllib.request import urlopen as uReq
import csv
from bs4 import BeautifulSoup as soup
import os.path
import logging
import substring

####SETTINGS VALUES
logging.basicConfig(handlers=[logging.FileHandler(filename="varunlog.txt",
                                                  encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%F %A %T",
                    level=logging.DEBUG)
# logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
csvfilename = 'DDflipkart_varun.csv'
theReviewCsvFilename = 'DDreviewCsvvarun.csv'
urlFileName = 'latest-urls.txt'
urlFile = open(urlFileName, 'r')
###################

logging.info('OutputFile =' + csvfilename)
logging.info('InputFile =' + str(urlFile))
startLine = input("Enter the start line: ")
logging.info('startLine =' + startLine)


def fileExists(csvname):
    return os.path.exists(csvname)


###########

def flipkartGrabReview(productUrl, thefilename):
    import substring

    # productUrl="https://www.flipkart.com/poco-c3-arctic-blue-64-gb/p/itm7f632fdb49b3b?pid=MOBFVQJ5NV9ZSYEF&lid=LSTMOBFVQJ5NV9ZSYEFCPQTX8&marketplace=FLIPKART&q=mobiles&store=tyy%2F4io&srno=s_1_2&otracker=AS_Query_TrendingAutoSuggest_1_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_1_0_na_na_na&fm=organic&iid=f19eb550-31f6-4106-ab7a-0a8c504bfc4f.MOBFVQJ5NV9ZSYEF.SEARCH&ppt=None&ppn=None&ssid=du83yy48ww0000001631118250665&qH=eb4af0bf07c16429"
    print(productUrl)
    domain = urlparse(productUrl).netloc
    p = substring.substringByChar(productUrl, startChar="=", endChar="&")
    productId = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,&]", "", p)
    uClient = uReq(productUrl)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    content = page_soup.find("div", {"class": "aMaAEs"})
    title = content.find("span", {"class": "B_NuCI"}).text
    # print(title)
    rev = page_soup.find("div", {"class": "row _3AjFsn _2c2kV-"})  # Extracting the content under specific tags
    links = rev.find("a").attrs['href']
    flipkart = "https://www.flipkart.com" + links
    # print(flipkart.replace('&aid',''))
    name = 'Flipkart'
    split_string = flipkart.split("&aid", 1)
    substring = split_string[0]
    # print(substring)
    url = "&marketplace=FLIPKART&page="
    reviewpageurl = substring + url
    pagenum = 5  # number of pages scraping
    reviews = []
    rating_data = []
    review_heading = []
    reviewed_customer = []
    location = []
    certified_customer = []
    dislikes = []
    likes = []
    for i in range(1, int(pagenum) + 1):
        reviewurl = reviewpageurl + str(i)
        # print(reviewurl)
        req_url = requests.get(reviewurl)
        if req_url.status_code == 200:
            page_soup = soup(page_html, "html.parser")
            for rating in page_soup.findAll("div", {"class": "_3LWZlK _1BLPMq"}):
                rate = rating.text
                rating_data.append(rate)  # ratings of reviews
            for feedback in page_soup.findAll("div", {"class": "t-ZTKy"}):
                feedback_text = feedback.text
                reviews.append(feedback_text)
            for rating in page_soup.findAll("div", {"class": "col JOpGWq"}):
                for rating1 in rating.findAll("div", {"class": "_2c2kV-"}):
                    for reviewhead in rating1.findAll("div", {"class": "_16PBlm"}):
                        # print(reviewhead)
                        for reviewhead1 in reviewhead.findAll("div", {"class": "col"}):
                            for reviewhead2 in reviewhead1.findAll("div", {"class": "col _2wzgFH"}):
                                for reviewhead3 in reviewhead2.findAll("p", {"class": "_2-N8zT"}):
                                    review_heads = reviewhead3.text
                                    review_heading.append(review_heads)  # main headings of reviews
                for rating in page_soup.findAll("div", {"class": "col JOpGWq"}):
                    for rating1 in page_soup.findAll("div", {"class": "_2c2kV-"}):
                        for reviewhead in rating1.findAll("div", {"class": "_16PBlm"}):
                            # print(reviewhead)
                            for reviewhead1 in reviewhead.findAll("div", {"class": "col"}):
                                for reviewhead2 in reviewhead1.findAll("div", {"class": "col _2wzgFH"}):
                                    for reviewhead2 in reviewhead1.findAll("div", {"class": "row _3n8db9"}):
                                        for reviewhead3 in reviewhead2.findAll("p", {"class": "_2sc7ZR _2V5EHH"}):
                                            customername = reviewhead3.text
                                            reviewed_customer.append(customername)  # customer name
                for rating in page_soup.findAll("div", {"class": "col JOpGWq"}):
                    for rating1 in page_soup.findAll("div", {"class": "_2c2kV-"}):
                        for reviewhead in rating1.findAll("div", {"class": "_16PBlm"}):
                            # print(reviewhead)
                            for reviewhead1 in reviewhead.findAll("div", {"class": "col"}):
                                for reviewhead2 in reviewhead1.findAll("div", {"class": "col _2wzgFH"}):
                                    for reviewhead2 in reviewhead1.findAll("div", {"class": "row _3n8db9"}):
                                        for reviewhead3 in reviewhead2.findAll("p", {"class": "_2mcZGG"}):
                                            t = reviewhead3.text
                                            certified_customer.append(t)  # certified customer and location
                for rating in page_soup.findAll("div", {"class": "col JOpGWq"}):
                    for rating1 in page_soup.findAll("div", {"class": "_2c2kV-"}):
                        for reviewhead in rating1.findAll("div", {"class": "_16PBlm"}):
                            # print(reviewhead)
                            for reviewhead1 in reviewhead.findAll("div", {"class": "col"}):
                                for reviewhead2 in reviewhead1.findAll("div", {"class": "col _2wzgFH"}):
                                    for reviewhead2 in reviewhead1.findAll("div", {"class": "row _3n8db9"}):
                                        for reviewhead3 in reviewhead2.findAll("p", {"class": "_2sc7ZR"}):
                                            for reviewhead3 in reviewhead2.findAll("span"):
                                                place = reviewhead3.text
                                                location.append(place)  # certified customer and location
                for rating in page_soup.findAll("div", {"class": "col JOpGWq"}):
                    for rating1 in page_soup.findAll("div", {"class": "_2c2kV-"}):
                        for reviewhead in rating1.findAll("div", {"class": "_16PBlm"}):
                            # print(reviewhead)
                            for reviewhead1 in reviewhead.findAll("div", {"class": "col"}):
                                for reviewhead2 in reviewhead1.findAll("div", {"class": "col _2wzgFH"}):
                                    for reviewhead3 in reviewhead2.findAll("div", {"class": "row _3n8db9"}):
                                        for reviewhead4 in reviewhead3.findAll("div", {"class": "_1LmwT9 pkR4jH"}):
                                            for d in reviewhead4.findAll("span", {"class": "_3c3Px5"}):
                                                # like = reviewhead4.text
                                                dislike = d.text
                                                dislikes.append(dislike)  # dislikes of review

    print(reviews.count)
    input("waitt..press any key to continue")
    review_details = pd.DataFrame({"Reviews": reviews, "Rating": rating_data, "Title": title, "Source": name,
                                   "Reviewed Customer": reviewed_customer, "Review Heading": review_heading,
                                   "Certified": certified_customer, "Dislikes": dislikes})
    print(review_details)
    rowcount = review_details.count
    review_details["SITENAME"] = domain
    review_details["PRODUCTID"] = productId
    review_details.insert(0, 'SITENAME', review_details.pop('SITENAME'))
    review_details.insert(1, 'PRODUCTID', review_details.pop('PRODUCTID'))
    # input('CHECKING FILE DETAILSSSSSSSS')
    # filename = "mytest.csv"
    ##review_details.to_csv(thefilename,index=False)
    if fileExists(thefilename):
        # input('EXISTS---')
        # code to read csv and append
        print('Review File exists..read the csv and append')
        df_fromcsv = pd.read_csv(thefilename)

        finaldf = review_details.append(df_fromcsv, sort=False)
        finaldf = finaldf.fillna(' ')
        finaldf.to_csv(thefilename, index=False, mode='w')
        # print('====FINAL DF====')
        # print (finaldf)
        # print(df_fromcsv)
    else:
        # input('DO NOT EXISTS---')
        print('Review File Doesnot exists..creating a new csv.')
        review_details.to_csv(thefilename, index=False)


###########

def usesoup(theurl, linecount):
    my_url = theurl
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    content = page_soup.find("div", {"class": "aMaAEs"})

    price = content.find("div", {"class": "_30jeq3 _16Jk6d"}).text
    price = re.sub(r"[^a-zA-Z0-9]", "", price)

    rating = content.find("div", {"class": "_3LWZlK"})
    overoll_rating = rating.text
    scrapped_headers = []
    scrapped_headers.append('SITENAME')
    scrapped_headers.append('PRODUCTID')
    scrapped_headers.append('PRICE')
    scrapped_headers.append('OVEROLL RATING')

    # count = 0

    cast_list = page_soup.findAll("table", {"class": "_14cfVK"})
    for t in page_soup.findAll("table", {"class": "_14cfVK"}):
        for m in t.findAll("tr", {"class": "_1s_Smc row"}):

            for d in m.find_all("td", {"class": "_1hKmbr col col-3-12"}):
                headings = d.text.translate(' \n\t\r')
                scrapped_headers.append(headings)
                # print(scrapped_headers)
                # count = count+1
                # print(count)
    # print("total_headings",count) # Headings

    values_data = []
    domain = urlparse(my_url).netloc
    values_data.append(domain)
    ###productId = my_url.split('/')[5]
    ###productId = productId.split('?')[0]
    p = substring.substringByChar(my_url, startChar="=", endChar="&")
    productId = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,&]", "", p)
    values_data.append(productId)
    values_data.append(price)
    values_data.append(overoll_rating)

    # print('productId=',productId)
    #######################################################################
    # if not fileExists(csvfilename):
    #    print("Writing header...")
    #    with open(csvfilename, 'a', encoding='UTF8') as ff:
    #       writer = csv.writer(ff)
    # write the header
    #   writer.writerow(scrapped_headers)
    # ff.close()
    #######################################################################
    countx = 0

    for t in page_soup.findAll("table", {"class": "_14cfVK"}):
        for m in t.findAll("tr", {"class": "_1s_Smc row"}):
            for d in m.find_all("td", {"class": "URwL2w col col-9-12"}):
                colnum = -1
                for l in d.find_all("li", {"class": "_21lJbe"}):
                    colnum = colnum + 1
                    values = l.text
                    # .replace(",", "~")
                    values_data.append(values)  # Features
                    # print(colnum)
                    # print("feature_text=========================",l.text.replace(",", "|"))
    # print("total countx",countx)

    # print('HEADERS LENGTH IS====>',len(scrapped_headers))
    # print('DATA LENGTH IS ====>',len(values_data))
    logging.info('HEADERS LENGTH IS====>' + str(len(scrapped_headers)))
    if (len(scrapped_headers) != len(values_data)):
        print("SCRAPPING ERROR Remove Line==", str(linecount))
        logging.info("SCRAPPING ERROR Remove Line==" + str(linecount))
        exit()
    ######CREATE KEY VALUE PAIR
    dataDictionary = {};
    for index in range(len(scrapped_headers)):
        theheader = scrapped_headers[index]
        theData = values_data[index]
        dataDictionary[theheader] = theData
        # print(theheader,'====>', theData)
    # print(dataDictionary)
    ##productDF = pd.DataFrame(dataDictionary)
    productDF = pd.DataFrame.from_dict(data=dataDictionary, orient='index')
    productDF = productDF.transpose()
    # productDF.to_csv(csvfilename,index=False)
    # print(productDF)
    if fileExists(csvfilename):
        # code to read csv and append
        print('File exists..read the csv and append')
        df_fromcsv = pd.read_csv(csvfilename)

        finaldf = productDF.append(df_fromcsv, sort=False)
        finaldf = finaldf.fillna(' ')
        finaldf.to_csv(csvfilename, index=False, mode='w')
        # print('====FINAL DF====')
        # print (finaldf)
        # print(df_fromcsv)
    else:
        print('File Doesnot exists..creating a new csv.')
        productDF.to_csv(csvfilename, index=False)

    # for aHeader in scrapped_headers:
    #    print(aHeader)
    # for index, element in zip(range(0,countries),countries):

    #     print('Index : ',index)
    #     print(' Element : ', element,'\n')
    ###########################
    ##with open(csvfilename, 'a', encoding='UTF8') as f:
    ##    writer = csv.writer(f)


##
# write the header
##    writer.writerow(values_data)

# write the data
# print('##############')
# print(values_data)
##TEMP writer.writerow(values_data)


###################################################END OF FUNCTION
#####GRABBING PRODUCT DETAILS
print('Starting product details grabbing....')
Lines = urlFile.readlines()
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if count >= int(startLine):
        # print("Line{}: {}".format(count, line.strip()))
        logging.info('Processing Line : ' + str(count))
        print('Processing Line : ' + str(count))
        with urllib.request.urlopen(line.strip()) as response:
            # html = response.read()
            # print("==================================================================")
            # print(html)
            usesoup(line.strip(), count)
        # input("press any key to continue...")
    else:
        print('Skipping line..', count)
print('==Product Description CSV===')
# print(pd.read_csv (csvfilename))
############EXTRACTING REVIEWS FROM FLIPKART
# print('Starting product review grabbing....' )
# input('startLine is '+str(startLine))
# input('startLine is '+str(startLine))
urlFile = open(urlFileName, 'r')
Lines = urlFile.readlines()
# input('Lines is '+str(Lines))
county = 0
# Strips the newline character
print(startLine)
print(Lines)
input("Going to check flipkartGrabReview ")

for line in Lines:
    # input("inside Line")
    county += 1
    if county >= int(startLine):
        print("Line{}: {}".format(county, line.strip()))
        logging.info('Processing Line : ' + str(county))
        with urllib.request.urlopen(line.strip()) as response:
            # html = response.read()
            # print("==================================================================")
            # print(html)
            flipkartGrabReview(line.strip(), theReviewCsvFilename)
            # usesoup(line.strip(),county)
    else:
        # startLine = input("Enter the start line: ")

        print('Skipping line..', county)
# print('===Final CSV===')
print('==Product Review CSV===')
print(pd.read_csv(theReviewCsvFilename))









