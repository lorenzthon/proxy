import base64
import html_to_json
import requests

def decodeBase64String(s):
    sample_string_bytes = base64.b64decode(bytes(s, 'utf-8'))
    return sample_string_bytes.decode("ascii")

def advancedName(page):
    categories = {
        "http": [],
        "socks": [],
    }
    unwanted=0
    try:

        tableHtml = "<tbody>"+page.split('<tbody>')[1].split('</tbody>')[0]+"'</tbody>'"
        tableJson = html_to_json.convert(tableHtml)
        for ea in tableJson['tbody'][0]['tr']:
            #print(ea)
            thisType = None
            for proxyType in ea['td'][3]['a']:
                if "SOCKS5" in proxyType['_value']: thisType="socks"
                if "HTTP" in proxyType['_value']: thisType = "http"

            proxy="{}:{}".format(decodeBase64String(ea['td'][1]['_attributes']['data-ip']),
                           decodeBase64String(ea['td'][2]['_attributes']['data-port']))
            if thisType != None:
                categories[thisType].append(proxy)
            else:
                unwanted += 1

        return categories,unwanted
    except:
        return categories,unwanted

def advancedNamePageIterator():
    socks=[]
    http = []
    for x in range(1,25): # I doubt they will have more than 25 pages.. they only had 4 when I checked
        v = visitPage("https://advanced.name/freeproxy?page={}".format(x))
        if v.page != None:
            proxies_found,unwanted = advancedName(v.page)
            found = len(proxies_found['socks'])+len(proxies_found['http'])+unwanted # just added the socks4 proxies to the counter so we can check 100 were grabbed from page
            socks+=proxies_found['socks']
            http += proxies_found['http']
            print("{} - {} proxies downloaded".format("advancedName",found))
            if found < 100: break # if less than 100 proxies found in page then we know it's the last page
    return http,socks

def openProxy(pageResponse):
    proxies = []
    for res in pageResponse.split('code:"'):
        if "items:[\"" in res: proxies += res.split("items:[\"")[1].split("]")[0].replace('"', '', -1).split(',')
    return proxies

class visitPage:
    def request(self):
        try:
            result = requests.get(self.url,headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})

            if result.status_code == 200:
                self.page = result.text
            else:
                print(result.status_code)


        except Exception as e:
            print(e)
            return

    def __init__(self,url):
        self.url = url
        self.page = None
        self.request()