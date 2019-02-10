import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
import errno
import datetime


headers = {'User-Agent': 'Mozilla'}
r = requests.get("https://www.reddit.com/r/dankmemes/top/?sort=top&t=week", headers=headers)
data = r.text
soup = BeautifulSoup(data, "lxml", parse_only=SoupStrainer("a"))

# print(soup)

count = 0

now = str(datetime.datetime.now())
print(now, '\n')
now = now[:now.find(' ')]
path = now + '/'
if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))

for a in soup.find_all('a', href=True):
    if a.find('img'):
        url = a.get("href")

        if url.startswith('/r/dankmemes'):
            url = 'https://reddit.com' + url

            count = count + 1
            name = url.split('/')[-2] + '.jpg'
            print(str(count) + ':', name)
# print(url)

            only_a_tags = SoupStrainer("img")

            r2 = requests.get(url, headers=headers)
            data2 = r2.text
            soup2 = BeautifulSoup(data2, "lxml", parse_only=only_a_tags)

# print('ok')

            for link in soup2.find_all('img'):
                image = link.get("src")

                if image.startswith('https://i.redditmedia.com/'):
                    print(image, '\n')
                    name = path + name
                    r3 = requests.get(image)
                    with open(name, "wb") as f:
                        f.write(r3.content)

                    break
