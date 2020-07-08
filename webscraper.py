import os
import glob
import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup


# global variables
internal_urls = set()
total_urls_visited = 0
current_file_number = 1


def is_valid(url: str) -> bool:
    """
    Checks whether the url (inside the href tag) is a valid link.

    :param url: The url for the webpage
    :return:    True if url is a valid link, False otherwise
    """

    # Parses the domain name of the url
    domain = urlparse(url)
    return bool(domain.netloc) and bool(domain.scheme)


def get_all_website_links(url: str) -> list:
    """
    Gets all urls that are found on `url` webpage hosted on medium.com.

    :param url: The url for the webpage
    :return:    List of urls for the 'url' parameter
    """

    # All urls of `url` parameter
    urls = set()

    # Domain name of the url without the protocol (https)
    domain_name = urlparse(url).netloc

    # HTTP GET request to the url
    result = requests.get(url)

    # BeautifulSoup gets the html of the url's webpage
    soup = BeautifulSoup(result.content, "html.parser")

    # Begin looking for all links ie. <a href=""> on the current webpage
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        
        if href == "" or href is None:
            # href empty tag, links nowhere
            continue

        # Join the url if it's relative (not absolute link)
        href = urljoin(url, href)
        # urlparse() returns a ParseResult object with [scheme, netloc, path, params, query]
        parsed_href = urlparse(href)

        # Combines url pieces to get ready to insert into final list of all the urls
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # Not a valid URL
            continue
        if href in internal_urls:
            # Already in the set
            # We only want unique url links
            continue
        if domain_name not in href:
            # External link
            continue

        print(f"[*] Internal link: {href}")
        urls.add(href)
        internal_urls.add(href)

    return urls


def crawler(url: str, max_urls=50):
    """
    Crawls starting url web page and extracts all links. Performs recursive crawling on those links and repeat until base case.
    
    :params max_urls: Number of urls to crawl. This is to prevent infinite recursive calls and crash my/your computer :)
    :return:          None
    """

    global total_urls_visited
    total_urls_visited += 1

    # First stores all the urls that are on the webpage given by the user
    links = get_all_website_links(url)

    # Loop through each url and recursively get all links on that page
    for link in links:
        # Specify a base case to exit recursion
        if total_urls_visited > max_urls:
            break
        crawler(link, max_urls=max_urls)


def getHTML(userURL):
    """
    
    """
    try:
        # result = requests.get(url = resource, headers=headers, cookies=cookie)
        # Perform an HTTP GET request on the given url link
        result = requests.get(url = userURL)

        # Status code 200 is success
        if result.status_code != 200:
            print('Webpage is not giving data: Error ', result.status_code)
            raise Exception
            
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        print('\nSuccessfully Parsed')
        
        # Returns the html of the webpage
        print(type(soup))
        return soup
    except:
        print('Something went wrong in getting the HTML code\n')
        return 
    


def scraper(url):
    """

    """
    parsedPage = getHTML(url)

    articleTitle = getArticleTitle(parsedPage)
    wordCount = getWordCount(parsedPage)
    clapCount = getClapCount(parsedPage)
    articleText = getArticleText(parsedPage)
    
    wantedInfo = [articleTitle, url, wordCount, clapCount, articleText]

    return wantedInfo


def getArticleTitle(parsedPage):
    """
    # Finds the first <h1> tag which seems to be a reasonable target for the article's title.    
    """
    if parsedPage is None or parsedPage.find('h1') is None:
        return ""
    
    title = parsedPage.find('h1').text
    return title


def getWordCount(parsedPage):
    """
    Finds all the <p> tags with an "id" attribute.
    Not 100% accurate word count since this also grabs <p> tags not in the article.
    ie. "About the author" text may also be counted.
    """
    if parsedPage is None or parsedPage.find_all('p', {'id': True}) is None:
        return 0

    wordList = parsedPage.find_all('p', {'id': True})

    textFromArticle = ""

    for i in range(len(wordList)):
        textFromArticle = textFromArticle + wordList[i].text + " "

    numWords = len(textFromArticle.split())
    return numWords


def getClapCount(parsedPage):
    """

    """
    if parsedPage is None or parsedPage.find_all('h4') is None:
        return 0

    numClapsCandidates = parsedPage.find_all('h4')
    numClaps = 0

    for j in range(len(numClapsCandidates)):
        child = numClapsCandidates[j].find('button')
        if child is not None:
            numClaps = child.text

    return numClaps


def getArticleText(parsedPage):
    """
    Finds all the <p> tags with an "id" attribute.
    Not 100% accurate word count since this also grabs <p> tags not in the article.
    ie. "About the author" text may also be counted.
    """
    if parsedPage is None or parsedPage.find_all('p', {'id': True}) is None:
        return ""
    
    wordList = parsedPage.find_all('p', {'id': True})

    textFromArticle = ""

    for i in range(len(wordList)):
        textFromArticle = textFromArticle + wordList[i].text + " "

    return textFromArticle


# Accepts a list of all the info that were scraped
def saveTextFile(infoList):

    currentFileLocation = os.path.dirname(os.path.abspath(__file__))

    # Global variable to increment data file number ie. data_1.txt ---> data_2.txt
    global current_file_number

    filePath = currentFileLocation + '/data_' + str(current_file_number) + '.txt'

    with open(filePath, 'w', encoding="utf-8") as myfile:
        for item in infoList:
            myfile.write("%s\n" % item)

    myfile.close()
    current_file_number += 1


# Credit to Greenstick for the awesome progress bar code
# Code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def main():    
    url = "https://medium.com/shallow-thoughts-about-deep-learning/how-would-we-find-a-better-activation-function-than-relu-4409df217a5c"
    minWords = 1000
    minClaps = 30

    # Change this to alter how much crawling should be done
    # Misleading name, doesn't actually only crawl for specified number of max url
    max_urls = 1

    directoryPath = os.path.dirname(os.path.abspath(__file__))
    all_url_links_file = 'all_url_links.txt'

    crawler(url, max_urls=max_urls)

    print("[+] Total URL links:", len(internal_urls))

    # domain_name = urlparse(url).netloc
    
    # Save the internal links to a file
    with open(all_url_links_file, 'w') as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    for i in range(len(internal_urls)):
        with open(directoryPath + '/' + all_url_links_file, 'r') as f:
            # index = 1
            printProgressBar(i+1, len(internal_urls), prefix='Progress', suffix='Complete', length=len(internal_urls))
            # Gets the second line in the file which has the url.
            # eachURL = f.read().split('\n')[line]
            eachURL = f.read().split('\n')[i+1]

            wantedInfo = scraper(eachURL)

            number_of_words = wantedInfo[2]

            # ie. turns "1.2K claps" into "1.2K"
            claps_only_number = str(wantedInfo[3]).split()[0]
            # ie. turns "1.2K" into "1200"
            if claps_only_number[-1] == "K":
                # [:-1] drops the last character from the string
                number_of_claps = claps_only_number[:-1] * 1000
            else:
                number_of_claps = claps_only_number * 1000

            if int(number_of_words) < minWords or int(number_of_claps) < minClaps:
                # Article info does not meet specified requirement
                continue
            
            # Making it here means that the article successfully met our criteria
            # Saves all information into a text file
            saveTextFile(wantedInfo)


# Automatically removes every .txt file from the directory before beginning new scrape run
for f in glob.glob("*.txt"):
    os.remove(f)

main()