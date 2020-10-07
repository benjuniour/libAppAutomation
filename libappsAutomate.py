from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from getpass import getpass

driver = webdriver.Chrome("./chromedriver")
driver.get("https://calvin.libapps.com/libguides/assets.php")

email_field = driver.find_element_by_name("s-libapps-email")
email_field.clear()
email_field.send_keys("email")

password_field = driver.find_element_by_name("s-libapps-password")
password_field.clear()
password_field.send_keys("password")

login_button = driver.find_element_by_id("s-libapps-login-button")
login_button.click()

wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
print("active")

#click on the book from catalog popup menu
book_catalog_popup_menu = driver.find_element_by_xpath("//a[contains(text(), 'Book') and contains(text(), 'from')]")
driver.execute_script("arguments[0].click();", book_catalog_popup_menu)

#send an isbn number to find the book
isbn_field = wait(driver, 5).until(EC.presence_of_element_located((By.ID, "book_isbn")))
isbn_field.send_keys("isbnnumber")

#execute finding the book
get_book_button = driver.find_element_by_xpath("//button[contains(text(), 'Book') and contains(text(), 'Info')]")
driver.execute_script("arguments[0].click();", get_book_button)

#clear out unnecessary fields
# author_field = wait(driver, 5).until(EC.presence_of_element_located((By.NAME, "book_author")))
# # author_field.clear()
# publication_field = driver.find_element_by_name("book_pub_date").clear()
# publication_field.send_keys("hello")

driver.find_element_by_id("s-lib-alert-btn-first").click()

print("came here")

