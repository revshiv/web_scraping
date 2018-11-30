from bs4 import BeautifulSoup
import requests
import json
import pprint

user = '@NucleusVision'

All = requests.get('https://medium.com/{}/latest?format=json'.format(user))

data = json.loads(str(All.text)[16:])

posts = data['payload']['references']

pprint.pprint(posts)

slugs = []

for key, value in posts['Post'].items():
    slugs.append(value['uniqueSlug'])

# extract data from particular post
for slug in slugs:
    postURL = 'https://medium.com/{}/{}'.format(user, slug)
    print("POST URL : " + postURL)

    post = requests.get(postURL)
    soup = BeautifulSoup(post.text, "html.parser")

    content = soup.find("div", {"class", "section-content"})


    print(soup.find("span", ))

    # HEADER
    title = content.find("h1").text
    print("TITLE : " + title)

    # BODY
    rows = soup.find("div", {"class", "section-inner sectionLayout--insetColumn"}).findAll(["p", "figure"], recursive=False)

    for row in rows:
        image = row.find("img")
        if image is None:
            temp_data = row.text
        else:
            temp_url = image.get('src')

    # print(rows)
    # break
