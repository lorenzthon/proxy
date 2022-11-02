from utils.sites import *
from utils.proxychecker import *
from termcolor import colored, cprint
import json
greenOut = lambda x: cprint(x, "green")

class proxyDler:
    def getProxylist(self):
        for type in self.apiSites:
            v = visitPage(self.apiSites[type])
            try:
                for proxy in v.page.splitlines(): self.results[type].append(proxy)
            except:
                self.results[type] = v.page.splitlines()

        h, s = advancedNamePageIterator()
        if self.socks:
            type = "socks"
            try:
                for proxy in s: self.results[type].append(proxy)
            except:
                self.results[type] = s
            for site in self.socks_sites:
                v = visitPage(site)
                if v.page != None:
                    this = self.socks_sites[site](v.page)
                    try:
                        for proxy in this: self.results[type].append(proxy)
                    except:
                        self.results[type] = this
            print("Finished collecting socks Proxies.")
            greenOut("You now have {} Socks5 Proxies!".format(len(self.results['socks'])))
        if self.http:
            type = "http"
            try:
                for proxy in h: self.results[type].append(proxy)
            except:
                self.results[type] = h

            for site in self.http_sites:
                v = visitPage(site)
                if v.page != None:
                    this = self.http_sites[site](v.page)
                    try:
                        for proxy in this: self.results[type].append(proxy)
                    except:
                        self.results[type] = this
            print("Finished collecting http(s) Proxies.")
            greenOut("You now have {} http(s) Proxies!".format(len(self.results['http'])))

            greenOut("Total of {} Proxies loaded!".format(len(self.results['http']) + len(self.results['socks'])))
    def loadSettings(self):
        try:
            with open('settings.json','r') as x:
                settings = json.loads(x.read())
            self.socks = settings['socks']
            self.http = settings['http']
            self.threadlimit = settings['threads']
            self.timeout = settings['timeout']

        except Exception as e:
            print(e)
            print("settings.json is required")

    def __init__(self):
        self.loadSettings()
        greenOut("Downloading proxy lists.")
        self.results = {}
        self.apiSites = {
            "http": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "socks": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all"
        }
        self.http_sites = {"https://openproxy.space/list/http": openProxy,}
        self.socks_sites = {"https://openproxy.space/list/socks5": openProxy,}
        self.getProxylist()
        proxyChecker(
            self.results,
            threadlimit=self.threadlimit,
            timeout=self.timeout
        )


if __name__ == "__main__":
    proxyDler()