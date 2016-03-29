# -*- coding: utf-8 -*-
import argparse
import sys
import os
import time
import random
import urllib2
from threading import Thread
from Queue import Queue

parser = argparse.ArgumentParser(description="""Parallel Downloader supports proxy-file and user-agents-file. 
      For each url in urls.txt, this script will download it with a random selected http proxy and a random selected user agent. 
      It will retry 3 times until download succeed, Otherwise failed url will be logged into failed_urls.log.""")
parser.add_argument('--parallel', type=int, nargs=1, default=4, help='parallel download, default is 4')
parser.add_argument('--proxy-file', dest='proxy', default="proxy.txt", help='proxy file like sqlmap, random selected, default proxy.txt')
parser.add_argument('--user-agents-file', dest='UA',default="user-agents.txt", help='user agents file like sqlmap, random selected, default user-agents.txt')
parser.add_argument('--urls-file', dest='urls',default="urls.txt", help='urls to download, one url per line, default urls.txt')

args = parser.parse_args()

ua_file = open(args.UA)
user_agent_list = ua_file.readlines()

proxy_file = open(args.proxy)
proxy_list = proxy_file.readlines()

urls_file = open(args.urls)
urls_list = urls_file.readlines()

concurrent = args.parallel

def doWork():
    while True:
        #grabs url from queue
        url = queue.get()
        retry = 3
        while retry>0:
            result = True
            proxy_handler = urllib2.ProxyHandler({'http': random.choice(proxy_list)})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', random.choice(user_agent_list).strip()),('Refer','http://www.google.com')]

            try:
                # Notice: you may need to change the save file logic
                if url.index('/Upload')>0:
                    filename = url[url.index('/Upload')+1:]
                    path = url[url.index('/Upload')+1:url.rindex('/')]
                    if not os.path.exists(path):
                        os.makedirs(path)

                    resp = opener.open(url, timeout=3)
                    with open(filename,'wb') as output:
                        output.write(resp.read())
                        output.close()
                    print "success: ", url
                    break
            except urllib2.HTTPError, e:
                print "HTTP Error: ", e.code , url
                result = False
            except urllib2.URLError, e:
                print "URL Error: ", e.reason , url
                result = False
            except Exception, e:
                print "Other Exception:", e , url
                result = False
            finally:
                retry = retry - 1
                if (retry == 0) and (not result):
                    print "failed: ", url
                    logFailedUrl(url)
        #signals to queue job is done
        queue.task_done()

def logFailedUrl(url):
    with open('failed_urls.log', 'a') as output:
        output.write(url+"\n")
        output.close()

start = time.time()

queue = Queue(concurrent * 10)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in urls_list:
        queue.put(url.strip())
    queue.join()
except KeyboardInterrupt:
    sys.exit(1)

print "Elapsed Time: %s" % (time.time() - start)