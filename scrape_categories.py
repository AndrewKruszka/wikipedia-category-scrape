from typing import NewType
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
startTime = datetime.now() #Testing how long it took the program to run (~6 hours)

r = False
a = 0
pageNum = 0

#Creating class for practice, might not be necessary
class SortCategories:

    def __init__(self, category, url) -> None:
        self.category = category
        self.url = url

    #Creates link for the category pages
    def create_link(self, text=None, url = None):
        if text:
            newSec = re.sub('\s+', '_', text)
        else:
            newSec = re.sub('\s+', '_', self.category)
        newUrl = self.url + newSec
        return(newUrl)

    def subcatCheck(subCheck):
        global r
        r = False
        for i in subCheck:
            if i.text.lower() == 'subcategories':
                r = True
            return r


    #Searches through every wikipedia category and adds them to All_Categories.txt
    def catPage(self, link = None):
        global a
        global pageNum
        global soup

        text = '(page does not exist)'
        list_of_categories = []

        #Checks if link has been passed into the class or if it should make a new link
        if link:
            url = link
        else:
            url = self.create_link()

        #Gets html contents of created url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        catHeader = soup.find('div', class_='mw-body-content', id = 'bodyContent')

        #Finds the categories section within the html
        categories = catHeader.findAll('a', href = True, title = True)
        for i in categories:
            if text in i['title']:
                continue
            list_of_categories.append(i)

        #Appends the text from the list_of_categories into the txt file
        for i in list_of_categories:

            #If the text was any of the extras within the category header, then they're skipped and not appended to the file
            if i.text == 'first' or i.text == 'last' or i.text == 'previous' or i.text == 'next' or i.text == '20' or i.text == '50' or i.text == '100' or i.text == '250' or i.text == '500' or i.text == 'next 500' or i.text == 'next 50' or i.text == 'previous 500' or i.text == 'special page' or i.text == 'Categorical index' or i.text == 'Wikipedia:FAQ/Categories' or i.text == 'Wikipedia:Categorization' or i.text == 'Wikipedia talk:Special:Categories':
                continue
            a += 1
            
            #Opens the txt file and adds each category to a new line
            with open("All_Categories.txt", "a") as myfile:
                myfile.write(i.text + '\n')

        
    #Searches the txt file for a user-entered category
    def search(self):
        returns = ''
        list = []

        #Opens txt file
        with open('categories.txt', 'rt') as file:
                text = file.readlines()

                #Asks user which category to search for and iterates through the txt lines for the input
                string = input('What would you like to search for? ')
                for line in text:
                    if string.lower() in line.lower():
                        print(line)
                    elif string.title() in line.title():
                        print(line)


def main():

    #Wikipedia urls for the category page
    wikiUrl = 'https://en.wikipedia.org'
    mainUrl = 'https://en.wikipedia.org/wiki/'
    cat = 'Special:Categories'

    #Creating the category object
    catTry = SortCategories(cat, mainUrl)
    catTry.catPage()

    #At the bottom of each cateogry page is the option to go to the next page
    #This loop checks to see if the object has reached the bottom of the page
    while True:

        #If the loop is at the bottom, it changes the url sent to the object so that it parses the next page
        try:
            nextPage = soup.find('a', text = '500')
            nextPage500 = soup.find('a', text = 'next 500')
            if nextPage500:
                #Creating the new url
                nextPageLink = wikiUrl + nextPage500['href']
                #Calls the category method with the new link
                catTry.catPage(nextPageLink)
            else:
                nextPageLink = wikiUrl + nextPage['href']
                catTry.catPage(nextPageLink)
        
        #If there is no option to go to the next page, then there are no more cateogries
        #Takes the timestamp and calculates how long it took the program to run
        except:
            endTime = datetime.now
            print(endTime - startTime)

main()
