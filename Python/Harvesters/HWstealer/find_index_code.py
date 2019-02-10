import urllib.request
from io import open


def url_is_alive(url):

    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

# 65 536 - liczba kombinacji


plik = open("codes.txt", "r")
content = plik.readlines()
i = 0
for x in content:

    url = "http://pp.iis.p.lodz.pl/reports/subsp/2-0101/215910-"
    url = url + x

    if i % 100 == 0:
        print(i)

    if url_is_alive(url) is True:
        print("znalazłem: ", url)
        break

    i = i + 1
