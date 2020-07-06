import os
import requests
from bs4 import BeautifulSoup


#Use requests to get html and BeautifulSoup to parse it
def getHTML():
    userURL = input('Please enter the link: ')
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


def scraper(parsedPage):

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
    wantedInfo = [title, numWords, numClaps]
    return wantedInfo

    
# Accepts a list of all the info that were scraped
def saveTextFile(infoList):

    currentFileLocation = os.path.dirname(os.path.abspath(__file__))

    #Save it in html format
    myfile = open(currentFileLocation + '/data.txt', 'w')
    
    # Clears content of the text file everytime script gets run
    myfile.truncate(0)

    for item in infoList:
        myfile.write("%s\n" % item)

    myfile.close()
    print('Successfully Written')


def main():
    html = getHTML()
    info = scraper(html)
    saveTextFile(info)

main()
