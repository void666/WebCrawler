# WebCrawler

1. Recursive crawler for domain specific crawling.
2. Creates a directory with domain name in local path and adds all the URLS that has been visited as individual files. 
3. The crawler writes all the available URLS in the file (named as the link that is being crawled), however, recursively crawls only the ones which has not been crawled earlier, results in 200 HTTPResponse code and is a part of the present URL being crawled (sub domain or director of the same URL) 
4. Displays the URLs that are not responding or has HTTP errors and unable to open them on console.



Files -

getLinks.py --  the functions can be called in the following way within the file
Usage :   getAllLinks(url) or getAllLinks(url,max_urls_needed_to_be_crawled)

eg : getAllLinks('http://python.org') or getAllLinks('http://python.org/',1000)

getLinksMain.py -- independent crawler file with command line argument input
Usage : getLinksMain.py [-h] url [-m,--maxLinks]
eg : getLinksMain.py http://python.org/ -m 100
