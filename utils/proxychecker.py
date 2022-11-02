import threading
from threading import Thread
from time import sleep
import time
import statistics
import requests

class proxyInfo:
    def __init__(self,
                 ip_port=None,
                 type=None,

                 ):
        self.ip_port = ip_port
        self.ip,self.port = ip_port.split(':')
        self.proxy={}
        self.run()
        super(proxyInfo, self).__init__()

    def run(self):
        if type == "socks":
            self.proxy['http'] = "socks5://{}".format(self.ip_port)
        else:
            self.proxy['http'] = "http://{}".format(self.ip_port)
            self.proxy['https'] = "https://{}".format(self.ip_port)


class proxyChecker:
    def calculateAverages(self):
        self.mean=None
        self.range=None
        self.median=None
        self.pings = [this.ping for this in self.proxyData if this.ping != None]
        self.mean = statistics.mean(self.pings)
        self.range = (min(self.pings),max(self.pings))
        self.median = statistics.median(self.pings)
        print("Ping Averages:\nMean: {}s\nMedian: {}s\nRange: {}s to {}s".format(
            round(self.mean,2),
            round(self.median,2),
            round(self.range[0],2),round(self.range[1],2)
        ))

    def waitThreads(self):
        while threading.active_count() > 1: sleep(0.5)
        print("finished threads!")


    def checkProxies(self):
        store=[]
        i=0
        for proxy_type in self.proxy_dict:
            for ipport in self.proxy_dict[proxy_type]:
                t = getProxyStats(ipport,proxy_type,self.timeout)
                while threading.active_count() > self.threadLimit: sleep(0.5)
                t.start()
                store.append(t)
                i+=1
                if i % self.threadLimit == 0: print("{}/{} Proxies being tested".format(i,self.totalRequests))

        self.waitThreads()
        self.proxyData = [obj for obj in store if obj.join()==None]


        for each in self.proxyData:
            if each.ping != None:
                self.proxyworks=True
        if self.proxyworks: self.calculateAverages()


    def save(self):
        with open('proxies.txt','w') as x:
            for ea in self.proxyData:
                if ea.ping != None:
                    x.write("{}\n".format(ea.proxyInfo.ip_port))




    def __init__(self,proxy_dict,threadlimit=150,timeout=30):
        self.onlineProxies=0
        self.totalRequests = 0
        self.displayProxyInfo = True
        self.proxycount = 0
        self.proxyworks = False
        self.pings = []
        for k in proxy_dict: self.totalRequests+=len(proxy_dict[k])

        self.proxy_dict = proxy_dict
        self.threadLimit = threadlimit
        self.timeout = timeout

        self.initTime = time.time()

        self.checkProxies()

        self.loadedTime = time.time()
        print("loaded {} proxies in {} seconds.".format(
            len(self.pings),
            round(self.loadedTime - self.initTime, 2))
        )
        if len(self.pings)>0: self.save()




class getProxyStats(Thread):
    def checkProxy(self):
        try:
            t = time.time()
            results = requests.get("https://api.ipify.org/?format=json",proxies=self.proxyInfo.proxy,timeout=self.timeout)
            if results.status_code == 200:
                if results.json()['ip'] == self.proxyInfo.ip:
                    self.ping = time.time() - t

                else:
                    pass # if you wanted transparent proxies could add code here to keep them


        except Exception as e:
            #print(e)
            return


    def __init__(self, ip_port,proxy_type,timeout):
        self.timeout = timeout
        self.ping=None
        self.proxyInfo = proxyInfo(ip_port,proxy_type)

        super(getProxyStats, self).__init__()

    def run(self):
        self.checkProxy()
