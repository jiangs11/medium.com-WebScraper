# Web Scraper for medium.com
### Description: This is a simple web scraper specifically written for medium.com articles.
### Programming Language: Python
### Libraries Used:
    1. os
        - For saving the scraped output into a text file.
    2. requests
        - For getting an http request to the webpage.
    3. BeautifulSoup
        - For getting the actual html of the webpage.
### Information Scraped:
    - Article's Title
    - Link
    - Number of Words in the Article
    - Number of "Claps" for the Article
### How to Use:
    1. Open terminal and run "python webscraper.py" or run from your favorite python ide.
    2. Paste the URL of the medium.com article that you wish to scrape information about.
    3. In the current directory, a "data_1.txt" file should appear once the script finishes.
    4. View the scraped information in the "data_1.txt" file.
    5. Every time the script is run with a unique url, the script will automatically create a new 'data_#.txt' file, where # stands for a number.
