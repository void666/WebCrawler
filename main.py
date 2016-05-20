__author__ = 'susdutta'
import requests
import urllib
from bs4 import BeautifulSoup
import re

url = 'http://python.org/'
curr = []#list of all current crawls
urls = [] #urls that needed to be crawled
ref = [] #referencing to previously crawled
urls.append(url)
ref.append(url)
max_count = 20
while urls and max_count>0:
    url = urls.pop(0)
    domain = urllib.parse.urlparse(url)[1]
    print(domain)
    max_count -= 1
    print(url)
    print(len(urls))
    request = requests.get(url)
    if request.status_code is not requests.HTTPError:
        sourceCode = BeautifulSoup(request.text, "html.parser")
        for link in sourceCode('a',href=True):
            link['href'] = urllib.parse.urljoin(url,link['href'])
            curr.append(link['href'])
            if domain in link['href'] and link['href'] not in ref and max_count>0:
                urls.append(link['href'])
                ref.append(link['href'])
                print('stack length',len(urls))
        fileName = url.replace('http://','').replace('/','-')
        fileName = re.sub('[^-a-zA-Z0-9_.() ]+','',fileName)
        file = open(fileName,'w')
        for links in curr:
            file.write(links+'\n')
        curr.clear()
