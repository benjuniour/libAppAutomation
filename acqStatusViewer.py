import requests, bs4
from random import randint

class BookDataService:
    
    def __init__(self, book_request):
        self.random_idx_tracker = 0
        self.all_table_rows = book_request.select("tr")
        self.book_details = {}
        
    def getBookData(self):
        
        #ensuring we don't get the sme book data twice
        random_index = randint(1,len(self.all_table_rows))
        while(random_index == self.random_idx_tracker or random_index == len(self.all_table_rows)):
            random_index = randint(1,len(self.all_table_rows))
        self.random_idx_tracker = random_index  
        chosen_row = self.all_table_rows[random_index]
        
        #access the title of the book and its isbn number
        book_title = chosen_row.select("td")[1].text
        isbn = chosen_row.select("td")[3].text
        
        #access the status column and book link
        status_column = chosen_row.select("td")[6]
        book_link = status_column.select("a")[0].get('href')
        
        #use book link to get the call number
        actual_book_request = requests.get(book_link)
        new_soup = bs4.BeautifulSoup(actual_book_request.text, 'html.parser')
        call_number = new_soup.select("td")[1].text.replace(" (Text)","")
        
        self.addBookToBookDetails(book_title, isbn, call_number, book_link)
        
        
    def addBookToBookDetails(self, bookTitle, bookISBN, bookCallNumber, bookLink): 
        additional_bookInfo = []
        additional_bookInfo.append(bookISBN)
        additional_bookInfo.append(bookCallNumber)
        additional_bookInfo.append(bookLink)
        #adding the new book information to our dictionary
        self.book_details[bookTitle] = additional_bookInfo

    def getBookDetails(self):
        return self.book_details
    
    
if __name__ == "__main__":
    year = input("Funding year: ")
    subject = input("Subject area: ")
    
    print()
    res = requests.get("http://ukeke.calvin.edu/cgi-bin/acq_status_viewer.pl?year={0}&fund={1}".format(year,subject))
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    bookService = BookDataService(soup)
    for i in range(8):
        bookService.getBookData()

    thebookDetails = bookService.getBookDetails()
    for key, value in thebookDetails.items():
        print("Title: ",key)
        print("ISBN: ", value[0])
        print("Call Number: ", value[1])
        print("Book link: ", value[2])
        print("---------------------------------------------------")