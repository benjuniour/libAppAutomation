from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from getpass import getpass
import time


class LibAppsDataPopulator:
    
    def __init__(self, a_webDriver):
        self.webDriver = a_webDriver
    
    
    def logIn(self, an_email, a_password):
        email_field = self.webDriver.find_element_by_name("s-libapps-email")
        email_field.clear()
        email_field.send_keys(an_email)
        
        password_field = self.webDriver.find_element_by_name("s-libapps-password")
        password_field.clear()
        password_field.send_keys(a_password)
        
        login_button = self.webDriver.find_element_by_id("s-libapps-login-button")
        login_button.click()
        
        # #to be removed: Placed here because the website had an annoying Ad
        # wait(self.webDriver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Got')]")))
        # skip_ad_button = self.webDriver.find_element_by_xpath("//button[contains(text(), 'Got')]")
        # self.webDriver.execute_script("arguments[0].click();", skip_ad_button)
        
        wait(self.webDriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
        print("active") 


    def populateBookAssets(self, book_isbn_num, callnumber="", booklink=""):
        #click on the book from catalog popup menu
        book_catalog_popup_menu = self.webDriver.find_element_by_xpath("//a[contains(text(), 'Book') and contains(text(), 'from')]")
        self.webDriver.execute_script("arguments[0].click();", book_catalog_popup_menu)
        
        #send an isbn number to find the book
        isbn_field = wait(self.webDriver, 5).until(EC.presence_of_element_located((By.ID, "book_isbn")))
        isbn_field.send_keys(book_isbn_num)
        
        #execute finding the book
        get_book_button = self.webDriver.find_element_by_xpath("//button[contains(text(), 'Book') and contains(text(), 'Info')]")
        self.webDriver.execute_script("arguments[0].click();", get_book_button)
        
        time.sleep(1)
        
        #clear out unnecessary fields
        author_field = wait(self.webDriver, 10).until(EC.presence_of_element_located((By.NAME, "book_author")))
        author_field.clear()
        
        publication_field = self.webDriver.find_element_by_name("book_pub_date")
        publication_field.clear()
        
        call_number_field =  self.webDriver.find_element_by_name("book_call_number")
        call_number_field.clear()
        call_number_field.send_keys(callnumber)
        
        url_field =  self.webDriver.find_element_by_name("book_url")
        url_field.clear()
        url_field.send_keys(booklink)
        
    
    def submitBookToAssets(self):
        save_button = self.webDriver.find_element_by_id("s-lib-alert-btn-first").click()

if __name__ == "__main__":
    username = input("Username: ")
    password = getpass("Password: ")           
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://calvin.libapps.com/libguides/assets.php")
    
    
    the_email = username + "@students.calvin.edu"
    assetPopulator = LibAppsDataPopulator(driver)
    assetPopulator.logIn(the_email, password)
    assetPopulator.populateBookAssets("9783777429335")
    assetPopulator.submitBookToAssets()

#title associated with test "Splendor and Misery in the Wei.."











