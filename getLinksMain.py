import requests
import urllib
from bs4 import BeautifulSoup
import re
import os
import argparse

curr = []#list of all current crawls
urls = [] #urls that needed to be crawled
ref = [] #set for all links fetched
totalLinksCrawled =[] #list of total links crawled so far

def getAllLinks(url,max_count):
    """
    segregate function, initializes the crawler based on the availability of max_count
    :param url: url to be crawled
    :param max_count: max urls to be crawled
    """
    url = addPathEnd(url)
    urls.append(url)
    ref.append(url)
    folderName = createFolder(url)

    if max_count is not None:
        loopWithMaxCount(max_count,folderName)
    else:
        loopWithoutMaxCount(folderName)


def loopWithMaxCount(max_count,folderName):

    """
    Main looper to of the crawler, runs till the end of the link stack or till the max links achieved
    :param max_count:  max urls to be crawled
    :param folderName: folder name where the files will be created
    """
    while urls and max_count>0:
        url = urls.pop(0)
        domain = urllib.parse.urlparse(url)[1]
        try:
            request = requests.get(url)
            if request.status_code == 200:
                max_count -= 1
                print("Current link being crawled",url,request.status_code)
                processRequest(url,request,domain,max_count)
                file = open(getFileName(url,folderName),'w')
                writeFile(file,curr)
                curr.clear()
            else:
                print('Unable to open url',url,'Response code :',request.status_code)
        except requests.exceptions.RequestException as e:
            print('Unable to get URL',e)
            pass

    print("links crawled = ",len(totalLinksCrawled))


def loopWithoutMaxCount(folderName):

    """
    Main looper to of the crawler, runs till the end of the link stack
    :param folderName: folder name where the files will be created
    """
    while urls:
        url = urls.pop(0)
        domain = urllib.parse.urlparse(url)[1]
        try:
            request = requests.get(url)
            if request.status_code == 200:
                print("Current link being crawled",url,request.status_code)
                processRequest(url,request,domain)
                file = open(getFileName(url,folderName),'w')
                writeFile(file,curr)
                curr.clear()
            else:
                print('Unable to open url',url,'Response code :',request.status_code)
        except requests.exceptions.RequestException as e:
            print('Unable to get URL',e)
            pass

    print("links crawled = ",len(totalLinksCrawled))


def processRequest(url,request,domain,max_count=None):

    """
    Extractor function, which takes the processed request source text and extracts the urls, adds them for further crawl
    :param url: url to crawled
    :param request: request response
    :param domain: domain name from the main or starting url
    :param max_count: max number of links to be crawled, if any.
    """
    totalLinksCrawled.append(url)
    sourceCode = BeautifulSoup(request.text, "html.parser")

    for link in sourceCode('a',href=True):
        link['href'] = urllib.parse.urljoin(url,link['href'])
        link['href'] = addPathEnd(link['href'])
        curr.append(link['href'])
        if max_count is not None:
            if domain in link['href'] and link['href'] not in ref and 'mailto:' not in link['href'] and max_count > 0:
                urls.append(link['href'])
                ref.append(link['href'])
                print('stack length',len(urls),' |url being added :',link['href'])
        else:
            if domain in link['href'] and link['href'] not in ref and 'mailto:' not in link['href']:
                urls.append(link['href'])
                ref.append(link['href'])
                print('stack length',len(urls),' |url being added :',link['href'])


def writeFile(file,curr):

    """
    Function to write files in the list.
    :param file: File to write the current links
    :param curr: current list of links extracted in this pass
    """
    for links in curr:
        try:
            file.write(str(links))
            file.write('\n')
        except BaseException:
            print("Unabel to write link to file :",links.encode("utf-8"))
            pass


def getFileName(url,folderName):
    """
    function to create a valid file name from current url being crawled.

    :param url: current url being crawled
    :param folderName: parent folder created for all file storage
    :return: processed valid file name
    """

    fileName = url.replace('http://','').replace('https://','').replace('/','-')
    fileName = re.sub('[^-a-zA-Z0-9_.()#]+','',fileName)
    fileName = str(folderName)+'/'+fileName
    return fileName

def createFolder(url):
    """
    function to create folder / path for the files to be written in to.
    :param url: main  URL being crawled
    :return: valid folder.
    """

    try:
        domain = urllib.parse.urlparse(url)[1]
        if not os.path.exists(domain):
            os.makedirs(domain)
            return domain
    except BaseException:
        print('Invalid URL')
        pass

def addPathEnd(url):
    """
     auxiliary function to check the end of link if path exists , if not then add path, to avoid duplication.
     :param url: url being crawled
     :return: url with path end.
     """
    if url[-1] is not '/':
        url += '/'
    return url


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("url" ,help =' Enter valid URL to be crawled',type = str)
    parser.add_argument("-m","--maxLinks", type = int, help="Enter max links to crawled (optional)")
    args = parser.parse_args()
    if args.maxLinks:
        getAllLinks(args.url,args.maxLinks)
    else:
        getAllLinks(args.url)
