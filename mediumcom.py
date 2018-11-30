from bs4 import BeautifulSoup
import requests
import json
import pymongo
import pprint
import time

'''MONGODB CONNECTION STARTS'''

client = pymongo.MongoClient("mongodb://patrick:abc123456@ds119734.mlab.com:19734/patrickpan")
db = client["patrickpan"]
mediumcom = db.mediumcom

'''MONGODB CONNECTION ENDS'''

'''GET OLD FROM DATABASE STARTS'''

server_urls = []
server_data = mediumcom.find({})
for i in server_data:
    server_urls.append(i["URL"])

'''GET OLD FROM DATABASE ENDS'''

'''USER WHOM DATA IS EXTRACTED'''
user = '@NucleusVision'

'''GET TOP 10 POSTS OF URLS [LATEST] STARTS'''

All = requests.get('https://medium.com/{}/latest?format=json'.format(user))
data = json.loads(str(All.text)[16:])
posts = data['payload']['references']

'''GET TOP 10 POSTS OF URLS [LATEST] ENDS'''


slugs = []

for key, value in posts['Post'].items():
    slugs.append(
        {"s": value['uniqueSlug'], "claps": value["virtuals"]["totalClapCount"], "tags": value["virtuals"]["tags"]})

# extract data from particular post
for slug in slugs:
    time.sleep(2)

    try:
        postURL = 'https://medium.com/{}/{}'.format(user, slug["s"])

        if postURL in server_urls:
            print("SKIPING URL => Data Already Exists")
            continue

        post = requests.get(postURL)
        soup = BeautifulSoup(post.text, "html.parser")

        content = soup.find("div", {"class", "section-content"})

        # DATE
        article_date = soup.find("time")
        if article_date is None:
            article_date = ''
        else:
            article_date = article_date.get("datetime")

        # READ TIME
        read_time_element = soup.find("span", {"class", "readingTime"})
        if read_time_element is None:
            read_time_element = ''
        else:
            read_time_element = read_time_element.get("title")

        # HEADER
        title = content.find("h1").text
        print("TITLE : " + title)

        # BODY
        rows = soup.find("div", {"class", "section-inner sectionLayout--insetColumn"}).findAll(["p", "figure"],
                                                                                               recursive=False)

        data = []
        for row in rows:
            image = row.find("img")

            if image is None:
                temp_data = row.text
                data.append({"text": temp_data})
            else:
                temp_url = image.get('src')
                data.append({"img": temp_url})

        temp = {
            "URL": postURL,
            "title": title,
            "date": article_date,
            "read_time": read_time_element,
            "claps": slug["claps"],
            "tags": slug["tags"],
            "data": data
        }

        result = mediumcom.insert_one(temp)
        print("*" * 50)
    except:
        print("Error while getting data " + postURL)
