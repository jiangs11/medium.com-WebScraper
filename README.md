# Web Scraper for medium.com
### Description: This is a simple web crawler and web scraper specifically written for medium.com articles. The crawler will begin with the user specified webpage and crawl to all other links on that page while adding the links to a single text file. After the crawling is complete, the scraping part begins. The scraper will attempt to retrieve the information specified further down in the README. Articles whose information don't exceed user specified parameters will not have their own designated text files with all the information. 
### Programming Language: Python

### Libraries Used:
    1. os
        - Saving the scraped output into a text file.
    2. glob
        - Deleting all text files from current directory.
    3. requests
        - Getting an http request to the webpage.
    4. urlparse, urljoin
        - Perform parsing and merging of url pieces.
    5. BeautifulSoup
        - For getting the actual html of the webpage.

### Information Scraped:
    - Article's Title
    - Link
    - Number of Words in the Article
    - Number of "Claps" for the Article
    - Plain text of the Article

### How to Use:
    1. Download the code in this repository.
    2. Open terminal, locate the directory containing this project, and run "python webscraper.py" or run from your favorite python ide.
    3. Paste the URL of the medium.com article that you wish to scrape information about, as well as providing parameters about the minimum word count and minimum clap count. 
    4. In the current directory, a "all_url_links.txt" file should appear, which holds all urls that have been crawled, starting from the page given.
    5. Additionally, pages whose info meets the specified parameters will have their own "data_*.txt" file, where * represents a number.
    6. Every time the script is ran, all the previous .txt files will be deleted, so be sure to save them elsewhere before rerunning the script.
