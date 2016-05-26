# WebCrawler

1. Iterative crawler for domain specific crawling.
2. Creates a directory with domain name in local path and adds all the URLS that has been visited as individual text files. 
3. The crawler writes all the available URLS in the file (named as the link that is being crawled), however, recursively crawls only the ones which has not been crawled earlier, results in 200 HTTPResponse code and is a part of the present URL being crawled (sub domain or directory of the same URL) 
4. Displays the URLs that are not responding or has HTTP errors and unable to open them on console.



### Files:

#### getLinks.py 
  the functions can be called in the following way within the file 
  >Usage :   getAllLinks(url) or getAllLinks(url,max_urls_needed_to_be_crawled)
  
eg : 

    getAllLinks('http://python.org',100)
    getAllLinks('http://www.bryanadams.com/')
    getAllLinks('http://avoidgeek.com/',1000)
  
#### getLinksMain.py
independent crawler file with command line argument input
>Usage : getLinksMain.py [-h] url [-m,--maxLinks]

eg : 

    getLinksMain.py http://python.org/ -m 100
    getLinksMain.py http://domain.com/
    getLinksMain.py http://avoidgeek.com/ -m 1000

### libraries used:

 - BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - Requests for Humans (https://pypi.python.org/pypi/requests/)
 
Test results  : 
  >getAllLinks('http://python.org',100)
  >Console out put : https://gist.github.com/void666/598c436f6f0e2cf671de5fa5a5d50036
  >
  >getAllLinks('http://bryanadams.com')
  >Console out put : https://gist.github.com/void666/d22b4e56852f90eae4023d96b94c3dbf
  >
  >getLinksMain.py http://www.bryanadams.com/
  >Console out put : https://gist.github.com/void666/da0c2e00c31e0e1800c4072ac76ad3b1
  >
  >getLinksMain.py http://python.org/ -m 100
  >Console out put : https://gist.github.com/void666/9f3d6e8041678abf6c586f9d62835bac
