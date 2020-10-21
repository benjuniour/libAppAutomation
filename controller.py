from acqStatusViewer import BookDataService
from libappsAutomate import LibAppsDataPopulator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from getpass import getpass

import requests, bs4
import time
from random import randint

'''
@author: Bernard Boadu
@purpose: This class serves as the bridge between the fetched data and the
automation process.
'''
class LibAppsController:
    
    def __init__(self):
        self.dataService = None
        self.bot = None
        self.subject_book_category = {}
        
    def run(self):
        year = input("Funding year(e.g. 2020): ")
        subject = input("Subject area(e.g.SOC): ").upper()
        num_books = int(input("Num of Books: "))
        password = getpass("Password: ") 
        the_email = "bkb5@students.calvin.edu"
        
        print("Performing book request...")
        res = requests.get("http://ukeke.calvin.edu/cgi-bin/acq_status_viewer.pl?year={0}&fund={1}".format(year,subject))
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        #retrieve the new books to be entered into the assets
        service = BookDataService(soup)
        for i in range(num_books):
            service.getBookData()
        bookDetails = service.getBookDetails()
        
        # Setup up driver and bot for automation process
        driver = webdriver.Chrome("./chromedriver")
        driver.get("https://calvin.libapps.com/libguides/assets.php")
        self.bot = LibAppsDataPopulator(driver)
        self.bot.logIn(the_email, password)
        
        print("Initializing automation...")
        
        # continuously populating the asset database
        for key, value in bookDetails.items():
            self.bot.populateBookAssets(value[0], value[1], value[2])
            next_step = input("All good? Y/N: ")
            
            if (next_step.lower() == "y"):
                self.writeSuccessBooksToFile(subject, key, year, value[0])
                self.bot.submitBookToAssets()
                print("Submitted book to assets...")
                # self.subject_book_category[subject].append(key)
                time.sleep(2)
            else:
                self.writeFailedBooksToFile(subject, key, year, value[0])
                
    def writeSuccessBooksToFile(self, subject, title, year, isbn):
        with open("bookSucesses.txt", 'a') as file:
            file.write("Subject: {}, Funding Year: {}, Title: {}, ISBN: {}\n".format(subject, year, title, isbn))
    
    def writeFailedBooksToFile(self, subject, title, year, isbn):
        with open("bookFailures.txt", 'a') as file:
            file.write("Subject: {}, Funding Year: {}, Title: {}, ISBN: {}\n".format(subject, year, title, isbn))
    

if __name__ == "__main__":        
    LibAppsController().run()