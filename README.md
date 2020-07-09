# Web Scraper for medium.com
### Description: This is a simple web crawler and web scraper specifically written for medium.com articles. The crawler will begin with the user specified webpage and crawl to all other links on that page while adding the links to a single text file. After the crawling is complete, the scraping part begins. The scraper will attempt to retrieve the information specified further down in the README. Articles whose information don't exceed user specified parameters will not have their own designated text files with all the information. 
### Programming Language: Python

### Libraries Used:
    1. os
        - Saving the scraped output into a text file.
    2. glob
        - Deleting all text files from current directory.
    3. shutil
        - Gets terminal size for auto-adjust terminal progress bar.
    4. requests
        - Getting an http request to the webpage.
    5. urlparse, urljoin
        - Perform parsing and merging of url pieces.
    6. BeautifulSoup
        - For getting the actual html of the webpage.

### Information Scraped:
    - Article's Title
    - Link
    - Number of Words in the Article
    - Number of "Claps" for the Article
    - Plain text of the Article

### How to Use:
    1. Download the code in this repository.
    2. Open terminal and locate the directory containing this project.
    3. Download required libraries with "pip install os, glob3, pytest-shutil, requests, urllib3, beautifulsoup4".
    4. Before running, please be sure to fill in the required parameters first (url, minWords, minClaps) inside the script itself.
    5. Run the script in terminal with "python webscraper.py" or with your favorite Python IDE.
    6. In the current directory, a "all_url_links.txt" file should appear, which holds all urls that have been crawled, starting from the page inputted.
    7. Additionally, pages whose information meets the specified parameters will have their own "data_*.txt" file, where * represents a number.
    8. Every time the script is ran, all the previous .txt files will be deleted, so be sure to save them elsewhere before rerunning the script.
