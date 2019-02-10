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


file = open("secret_codes.txt", "r")
content = file.readlines()
i = 0
for x in content:
    url = "http://pp.iis.p.lodz.pl/reports/subsp/441-2806/"
    url = url + x

    if url_is_alive(url) is True:
        print(url, end='')
        i = i + 1


print("zadanie probowalo zrobic ", i, "z ", len(content) - 1, "osob na liście")

input()
