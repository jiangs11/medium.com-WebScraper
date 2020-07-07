import os
import requests
from bs4 import BeautifulSoup
from itertools import islice


#Use requests to get html and BeautifulSoup to parse it
def getHTML(userURL):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    # cookie = {'Cookie': 'aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws_lang=en; x-wl-uid=1qqB55cbZjrg3L/5ASidPnKLm7vU+Fspwr5i6FzpE/D/NQqNHucB8ZPeffvOAZgBWLXj5tPN3fV0=; session-id-time=2082787201l; session-id=132-3769011-5781220; ubid-main=133-0861431-6797846; i18n-prefs=USD; skin=noskin; session-token=vKMvwRImxeCZqtHjutETl/AHyKTdXfv40HfxcTVN5epzu2TOe7U6nOLREziRnhmu6NO4H1Fjr5UuCJvYW6C+gm9beB+yLdKPEIWHDRjE6MTXoXftNecZgyL4GsXqxghL5jdYtgbazsYtaYDuERsBRY4do+yIwtVJAJVQgxfo+mSdkqGaCdVN2Tx5wtLipXzI'}

    try:
        # result = requests.get(url = resource, headers=headers, cookies=cookie)
        # Perform an HTTP GET request on the given url link
        result = requests.get(url = userURL)

        # Status code 200 is success
        if result.status_code != 200:
            print('Webpage is not giving data: Error ', result.status_code)
            raise Exception
    except:
        print('Something went wrong in getting the HTML code\n')
        quit()

    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    print('\nSuccessfully Parsed')
    
    # Returns the html of the webpage
    return soup


def scraper(parsedPage, url):

    # Finds the first <h1> tag which seems to be a reasonable target for the article's title.
    title = parsedPage.find('h1').text

    # Finds all the <p> tags with an "id" attribute.
    # Not 100% accurate word count since this also grabs <p> tags not in the article.
    # ie. "About the author" text may also be counted.
    wordList = parsedPage.find_all('p', {'id': True})

    textFromArticle = ""

    for i in range(len(wordList)):
        textFromArticle = textFromArticle + wordList[i].text + " "


    numWords = len(textFromArticle.split())
    print("number of words: ", numWords)

    numClapsCandidates = parsedPage.find_all('h4')
    numClaps = 0

    for j in range(len(numClapsCandidates)):
        child = numClapsCandidates[j].find('button')
        if child is not None:
            numClaps = child.text


    print(numClaps)
    wantedInfo = [title, url, numWords, numClaps]
    return wantedInfo

    
# Accepts a list of all the info that were scraped
def saveTextFile(infoList):

    currentFileLocation = os.path.dirname(os.path.abspath(__file__))

    # Variable to increment data file number ie. data_1.txt ---> data_2.txt
    currentFileNumber = 1

    #Save it in html format
    # myfile = open(currentFileLocation + '/data.txt', 'w')
    filePath = currentFileLocation + '/data_' + str(currentFileNumber) + '.txt'
    print("path testing: ", filePath)
    myfile = open(filePath, 'w')

    # Clears content of the text file everytime script gets run
    # myfile.truncate(0)

    for item in infoList:
        myfile.write("%s\n" % item)

    myfile.close()
    print('Successfully Written')
    currentFileNumber = currentFileNumber + 1


# To prevent scraping webpages that have already been scraped.
def check_url_unique(userURL):
    # Geting directory path and setting up path for directory iteration.
    directoryPath = os.path.dirname(os.path.abspath(__file__))
    currentDirectory = str(directoryPath)
    directory = os.fsencode(currentDirectory)

    # Loop through every file in the current directory.
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # Only check the text files.
        if filename.endswith(".txt"):
            # Open the text file for reading.
            with open(directoryPath + "/" + filename, 'r') as f:
                # Gets the second line in the file which has the url.
                urlFromFile = f.read().split('\n')[1]

            # Check scraped url with the url that the user just entered.
            if urlFromFile == userURL:
                # Getting here means that the url was found in the data.txt files
                # Therefore, webpage has already been scraped before.
                print("This webpage has already been scraped before!")
                print("The info is stored in", filename, "!")
                return False
        else:
            continue
    # Return true, meaning user inputted url webpage hasn't been scraped before.
    return True


def main():
    userURL = input('Please enter the link: ')
    uniqueURL = check_url_unique(userURL)
    
    # Only perform webscraping on url's that haven't been scraped before.
    if uniqueURL:
        html = getHTML(userURL)
        info = scraper(html, userURL)
        saveTextFile(info)

# Call main method
main()