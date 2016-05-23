import requests
import urllib
from bs4 import BeautifulSoup
import re
from multipledispatch import dispatch
import os

curr = []#list of all current crawls
urls = [] #urls that needed to be crawled
ref = [] #set for all links fetched
totalLinksCrawled =[] #list of total links crawled so far

@dispatch(str,int)
def getAllLinks(url,max_count):

    url = addPathEnd(url)
    urls.append(url)
    ref.append(url)
    folderName = createFolder(url)
    while urls and max_count>0:

        url = urls.pop(0)
        domain = urllib.parse.urlparse(url)[1]

        try:
            request = requests.get(url)

            if request.status_code == 200:
                max_count -= 1
                print("Current link being crawled",url,request.status_code)
                totalLinksCrawled.append(url)
                sourceCode = BeautifulSoup(request.text, "html.parser")
                for link in sourceCode('a',href=True):

                    link['href'] = urllib.parse.urljoin(url,link['href'])

                    #check to append path or not, else possibility of duplicate crawl
                    link['href'] = addPathEnd(link['href'])
                    curr.append(link['href'])

                    #check if link is of the same domain and has not been crawled previously, has the domain name as part of it.
                    if domain in link['href'] and link['href'] not in ref and 'mailto:' not in link['href'] and max_count > 0:
                        urls.append(link['href'])
                        ref.append(link['href'])
                        print('stack length',len(urls),' |url being added :',link['href'])

                file = open(getFileName(url,folderName),'w')
                writeFile(file,curr)
                curr.clear()
            else:
                print('Unable to open url',url,'Reponse code :',request.status_code)
        except requests.exceptions.RequestException as e:
            print('Unable to get URL',e)
            pass
    print("links crawled = ",len(totalLinksCrawled))

@dispatch(str)
def getAllLinks(url):

    url = addPathEnd(url)
    urls.append(url)
    ref.append(url)
    folderName = createFolder(url)
    while urls:

        url = urls.pop(0)
        domain = urllib.parse.urlparse(url)[1]
        try:
            request = requests.get(url)

            if request.status_code == 200:
                print("Current link being crawled",url,request.status_code)
                totalLinksCrawled.append(url)
                sourceCode = BeautifulSoup(request.text, "html.parser")
                for link in sourceCode('a',href=True):

                    link['href'] = urllib.parse.urljoin(url,link['href'])

                    #check to append path or not, else possibility of duplicate crawl
                    link['href'] = addPathEnd(link['href'])
                    curr.append(link['href'])

                    #check if link is of the same domain and has not been crawled previously, has the domain name as part of it.
                    if domain in link['href'] and link['href'] not in ref and 'mailto:' not in link['href']:
                        urls.append(link['href'])
                        ref.append(link['href'])
                        print('stack length',len(urls),' |url being added :',link['href'])

                file = open(getFileName(url,folderName),'w')
                writeFile(file,curr)
                curr.clear()

            else:
                print('Unable to open url',url,'Reponse code :',request.status_code)

        except requests.exceptions.RequestException as e:
            print('Unable to get URL',e)
            pass

    print("links crawled = ",len(totalLinksCrawled))


#Writing to file
def writeFile(file,curr):
     for links in curr:
        try:
            file.write(str(links))
            file.write('\n')
        except BaseException:
            print("Unabel to write link to file :",links.encode("utf-8"))
            pass

#function process URL as a valid File Name
def getFileName(url,folderName):

    fileName = url.replace('http://','').replace('https://','').replace('/','-')
    fileName = re.sub('[^-a-zA-Z0-9_.()#]+','',fileName)
    fileName = str(folderName)+'/'+fileName
    return fileName

#function to create folder
def createFolder(url):
    try:
        domain = urllib.parse.urlparse(url)[1]
        if not os.path.exists(domain):
            os.makedirs(domain)
        return domain
    except BaseException:
        print('Invalid URL')
        pass

#mandatory check at the end of link to add path, to avoid duplication.
def addPathEnd(url):
     if url[-1] is not '/':
         url += '/'
     return url


#Test run getAllLinks('http://bryanadams.com')
