import urllib.request


def url_is_alive(url):

    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


url = "http://pp.iis.p.lodz.pl/reports/subsp/413-2602/215669-c7da/"
if url_is_alive(url) is True:
    print("url exists:\n", url)

input()
