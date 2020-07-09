# Name: Steven Jiang
# Date: 7/9/2020
# Purpose: Coding Challenge
# Description: Simple web crawler and web scraper for medium.com articles


# Libraries
import os
import glob
import shutil
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
    # Using a set for unique elements
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
            # External link; links to domain outside of medium.com
            continue

        urls.add(href)
        internal_urls.add(href)

    return urls


def crawler(url: str, layers: int):
    """
    Crawls starting url web page and extracts all links. Performs recursive crawling on those links and repeat until base case.
    
    :params url:    URL of webpage
    :params layers: Number of layers to crawl. This is to prevent infinite recursive calls and crash my/your computer :)
    :return:        None
    """

    global total_urls_visited
    total_urls_visited += 1

    # First stores all the urls that are on the webpage given by the user
    links = get_all_website_links(url)

    # Loop through each url and recursively get all links on that page
    for link in links:
        # Specify a base case to exit recursion
        if total_urls_visited > layers:
            break
        crawler(link, layers)


def get_html(userURL: str):
    """
    Uses BeautifulSoup to get the HTML of the given url.

    :params userURL: URL of webpage
    :return:         BeautifulSoup object, which is essentially a HTML document
    """
    try:
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
        return soup
    except:
        print('Something went wrong in getting the HTML code\n')
        return 
    

def scraper(url) -> list:
    """
    Uses BeautifulSoup to scrape data from the webpages.

    :params url: URL of webpage
    :return:     List of scraped data
    """
    parsedPage = get_html(url)

    # Call appropriate functions to scrape data
    articleTitle = get_article_title(parsedPage)
    wordCount = get_word_count(parsedPage)
    clapCount = get_clap_count(parsedPage)
    articleText = get_article_text(parsedPage)
    
    # Store all scraped data into a list
    wantedInfo = [articleTitle, url, wordCount, clapCount, articleText]

    return wantedInfo


def get_article_title(parsedPage) -> str:
    """
    Finds the first <h1> tag which seems to be a reasonable target for the article's title.   

    :params parsedPage: HTML provided by BeautifulSoup 
    :return:            String of the article's title          
    """
    if parsedPage is None or parsedPage.find('h1') is None:
        # Error in getting HTML or <h1> tag does not exist
        return ""
    
    title = parsedPage.find('h1').text
    return title


def get_word_count(parsedPage) -> int:
    """
    Finds all the <p> tags with an "id" attribute.
    Not 100% accurate word count since this also grabs <p> tags not in the article.
    ie. "About the author" text may also be counted.

    :params parsedPage: HTML provided by BeautifulSoup 
    :return:            Close estimate number of words in the article       
    """
    if parsedPage is None or parsedPage.find_all('p', {'id': True}) is None:
        # Error in getting HTML or <p> tag does not exist
        return 0

    # Each <p> tag element will be stored in the list
    wordList = parsedPage.find_all('p', {'id': True})

    textFromArticle = ""

    for i in range(len(wordList)):
        # Save all text into a string variable
        textFromArticle = textFromArticle + wordList[i].text + " "

    numWords = len(textFromArticle.split())
    return numWords


def get_clap_count(parsedPage) -> int:
    """
    Medium.com has a clap count for each article, which is basically equivalent to a like.

    :params parsedPage: HTML provided by BeautifulSoup 
    :return:            Number of claps for the article     
    """
    if parsedPage is None or parsedPage.find_all('h4') is None:
        # Error in getting HTML or <h4> tag does not exist
        return 0

    # The pattern I saw for number of claps in the page was a <h4> tag followed by a <button>
    # Therefore, below I have found all <h4> tag elements, which will be considered as my candidates
    numClapsCandidates = parsedPage.find_all('h4')
    numClaps = 0

    for j in range(len(numClapsCandidates)):
        # Here, we begin looking for <button> right after in the DOM
        child = numClapsCandidates[j].find('button')

        if child is not None:
            # Found the first <button> after a <h4> tag
            numClaps = child.text

    return numClaps


def get_article_text(parsedPage) -> str:
    """
    Finds all the <p> tags with an "id" attribute.
    Not 100% accurate word count since this also grabs <p> tags not in the article.
    ie. "About the author" text may also be counted.

    :params parsedPage: HTML provided by BeautifulSoup 
    :return:            String of the article's text   
    """
    if parsedPage is None or parsedPage.find_all('p', {'id': True}) is None:
        # Error in getting HTML or <p> tag does not exist
        return ""
    
    # Each <p> tag element will be stored in the list
    wordList = parsedPage.find_all('p', {'id': True})

    textFromArticle = ""

    for i in range(len(wordList)):
        # Save all text into a string variable
        textFromArticle = textFromArticle + wordList[i].text + " "

    return textFromArticle


def save_text_file(infoList: list):
    """
    Saves scraped data of articles that meet the user specified criteria.
    Automatically generates new text file in the current directory.

    :params infoList: List returned by the scrape() function
    :return:          None
    """

    # Gets the current directory path holding this python script
    currentFileLocation = os.path.dirname(os.path.abspath(__file__))

    # Global variable to increment data file number ie. data_1.txt ---> data_2.txt
    global current_file_number

    # Forge a directory path for the text file to be saved to (still in this directory)
    filePath = currentFileLocation + '/data_' + str(current_file_number) + '.txt'

    with open(filePath, 'w', encoding="utf-8") as myfile:
        # For each element in the list, writes the data on a new line
        for item in infoList:
            myfile.write("%s\n" % item)

    myfile.close()
    current_file_number += 1


# Credit to Greenstick for the awesome progress bar code
# Code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = False):
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
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


def main():    
    ###############################################################
    ## PLEASE FILL IN THESE PARAMETERS BEFORE RUNNING THE SCRIPT ##
    ###############################################################
    
    # url = "https://medium.com/shallow-thoughts-about-deep-learning/how-artificial-general-intelligence-might-be-created-1e2476d1516a"
    url = ""
    minWords = 
    minClaps = 
    # For some reason, the script doesn't like the input() function

    # Change this to alter how much crawling should be done
    # Warning!!! Don't set it too high or your computer might crash!!!
    layers = 1

    directoryPath = os.path.dirname(os.path.abspath(__file__))
    all_url_links_file = 'all_url_links.txt'

    crawler(url, layers)

    print("Total URL links:", len(internal_urls))
    
    # Save all links crawled to a file
    with open(all_url_links_file, 'w') as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # Loops through each link that was crawled
    for i in range(len(internal_urls)):
        with open(directoryPath + '/' + all_url_links_file, 'r') as f:

            print_progress_bar(i+1, len(internal_urls), prefix='Progress', suffix='Complete', length=len(internal_urls), autosize=True)

            eachURL = f.read().split('\n')[i+1]

            # Starts scraping each URL in the all_url_links.txt file
            wantedInfo = scraper(eachURL)

            number_of_words = wantedInfo[2]

            # ie. turns "1.2K claps" into "1.2K"
            claps_only_number = str(wantedInfo[3]).split()[0]

            # ie. turns "1.2K" into "1200"
            if claps_only_number[-1] == "K":
                # [:-1] drops the last character from the string
                number_of_claps = claps_only_number[:-1] * 1000
            else:
                number_of_claps = claps_only_number

            # Making sure criteria is met before saving their data
            try:
                if int(number_of_words) < minWords or int(number_of_claps) < minClaps:
                    # Article info does not meet specified requirement
                    continue
            except: 
                continue

            # Making it here means that the article successfully met our criteria
            # Saves all scraped information into their own text file
            save_text_file(wantedInfo)


# Automatically removes every .txt file from the directory before beginning new scrape run
for f in glob.glob("*.txt"):
    os.remove(f)

main()