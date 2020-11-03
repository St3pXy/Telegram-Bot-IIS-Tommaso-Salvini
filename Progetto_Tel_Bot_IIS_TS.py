import telebot
import requests
from bs4 import BeautifulSoup
import time, os

# School Site
comunications_school_link = 'https://www.iistommasosalvini.edu.it/comunicazioni-e-progetti/comunicazioni-e-news'

# Bot Token
token = '1133927300:AAEAGmQVerwhZ13D_dzi-7kqBUI_rVucH2s'
chat_id = '-1001398133767'
bot = telebot.TeleBot(token)

# Global Values
titles = []
last_read = ''
first_in_list = ''
last__circ = True

# Bot function for Send Messages
def send_message(token, chat_id, text):
    url_req = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text=' + text
    telbot_result = requests.get(url_req)
    print("Message sended")

def search_news():
    global comunications_school_link, titles, last_read, first_in_list, last__circ
    global token, chat_id

    # Get Connection to the Web-Site
    result = requests.get(comunications_school_link)
    # Print Connection Status Code
    print("School Website Connection Status Code: " + str(result.status_code))
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    # Initialize Values
    conta = 0

    for x in soup.findAll('td', {'class': 'list-title'}):
        full_title = x.get_text()
        title = full_title[8:-1]

        if last__circ:
            last_read = title
            first_in_list = title
            titles.append(last_read)
            last__circ = False

        print(title)
        print(first_in_list)
        conta += 1

        if conta == 0 and first_in_list == title:
            pass
        elif conta == 0 and first_in_list != title:
            titles.append(title)
            last__circ = True

# While Loop to be Active Always
run_app = True
while run_app:
    titles = []
    search_news()
    print(title)
    if len(titles) != 0:
        for title in titles:
            send_message(token, chat_id, title)
            print("Sended Message")
        send_message(token, chat_id, comunications_school_link)
        print("Sended Link")
    time.sleep(10)
