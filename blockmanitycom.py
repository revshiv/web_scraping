from bs4 import BeautifulSoup
import requests
import pymongo
import time

client = pymongo.MongoClient("mongodb://patrick:abc123456@ds119734.mlab.com:19734/patrickpan")

db = client["patrickpan"]
blockmanitycom = db.blockmanitycom

post_urls = []

for i in range(1, 58):

    All = requests.get('https://blockmanity.com/category/news/page/{0}/'.format(i))
    soup = BeautifulSoup(All.text, "html.parser")

    # Find posts list div with Beautiful soup find One
    sidebar_content_div = soup.find("div", {"class", "sidebar_content"})
    posts = sidebar_content_div.findAll("div", {"class", "post"})

    for j in posts:
        hFive_href = j.find("h5").find("a").get("href")
        post_urls.append(hFive_href)

    # break

# Extract data of single post

# print(post_urls)
for post_url in post_urls[1:]:
    time.sleep(2)
    try:
        print("=" * 10)
        print("POST URL : " + post_url)
        post = requests.get(post_url)
        soup = BeautifulSoup(post.text, "html.parser")

        # POST Header
        post_header = soup.find("div", {"class", "post_header"})

        # **TITLE**
        post_title = post_header.find("h1").text
        print("Title == " + post_title)

        # **AUTHOR**
        post_author = post_header.find("span", {"class", "post_info_author"}).find("a").text.strip()
        print("Author == " + post_author)

        # **POSTED DATE**
        post_date = post_header.find("span", {"class", "post_info_date"}).text.strip()
        print("Post Date == " + post_date)

        # **POST SHARE COUNT**
        post_share_count = soup.find("div", {"class", "social_share_counter_number"}).text.strip()
        print("Post Share Count === " + post_share_count)

        # **POST VIEW COUNT**
        post_view_count = soup.find("span", {"class", "post-views-count"}).text.strip()
        print("Post View Count === " + post_view_count)

        # **Image URL**
        # If Image exists it returns image div ELSE return None
        post_image = soup.find("div", {"class", "post_img"})

        post_image_url = ""

        if post_image is not None:
            post_image_url = post_image.find("img").get("src")
        print("Image URL == " + post_image_url)
        print("=" * 10)
        # ** BODY **
        post_data = soup.find("div", {"class", "post_header single"})

        all_p = post_data.findAll(["p", "blockquote", "h4", "ul", "b"], recursive=False)

        # find also read tag to REMOVE from the content {START}
        count = 0
        for ps in all_p:
            count += 1
            if ps.text.strip() == 'Also Read:':
                break

        if count != len(all_p):
            all_p = all_p[0:count - 1]
        # find also read tag to REMOVE from the content {END}

        # print(all_p)

        data = []
        for p in all_p:
            data.append(p.text)

        temp = {
            "URL": post_url,
            "title": post_title,
            "author": post_author,
            "date": post_date,
            "shareCount": post_share_count,
            "viewCount": post_view_count,
            "postImage": post_image_url,
            "data": data
        }
        result = blockmanitycom.insert_one(temp)

        # all_post_scraped_data.append(temp)

        print("*" * 50)

        # print()
        # break
    except:
        print("ERROR: " + post_url)

client.close()
