import urllib.request


def url_is_alive(url):

    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


for i in range(0, 9999):

    url = "http://pp.iis.p.lodz.pl/reports/subsp/444-2809/215730-a60b/22"
    x = str(i)
    while len(x) < 4:
        x = '0' + x
    url = url + x + "/index.html"

    if i % 50 == 0:
        print(i)

    if url_is_alive(url) is True:
        print(url)

input()
