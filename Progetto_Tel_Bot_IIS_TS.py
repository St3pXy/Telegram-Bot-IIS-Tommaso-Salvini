import requests
from bs4 import BeautifulSoup
import time

my_actual = 100
titles = []
last = 100

def search_news():
    global titles
    global last
    # Get Connection to the Web-Site
    comunications_school_link = 'https://www.iistommasosalvini.edu.it/comunicazioni-e-progetti/comunicazioni-e-news'
    result = requests.get(comunications_school_link)
    # Print Connection Status Code
    print("School Website Connection Status Code: " + str(result.status_code))
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    titles = []
    last__circ = True

    for x in soup.findAll('td', {'class': 'list-title'}):
        full_title = x.get_text()
        title = full_title[8:-1]
        titles.append(title)

        if last__circ:
            try:
                last = int(full_title[14:17])
                last__circ = False
            except:
                last__circ = True

while True:
    search_news()
    print(titles)
    print(last)
    time.sleep(10)
