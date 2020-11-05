import telebot
import requests
from bs4 import BeautifulSoup
import time, os

# School Site
comunications_school_link = 'https://www.iistommasosalvini.edu.it/comunicazioni-e-progetti/comunicazioni-e-news'

# Bot Token
token = os.environ['TELEGRAMBOTTOKEN']
chat_id = os.environ['TELEGRAMCHATID']
bot = telebot.TeleBot(token)

# Global Values
last_read = ''
first_in_list = ''
last__circ = True

# Bot function for Send Messages
def send_message(token, chat_id, text):
    global comunications_school_link
    if text == comunications_school_link
        url_req = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text=' + text + '&disable_web_page_preview=True'
        telbot_result = requests.get(url_req)
        print("Message sended (LINK)")
    else:
        url_req = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text=' + text
        telbot_result = requests.get(url_req)
        print("Message sended (TEXT)")
        

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
    not_saw_my_last = True
    count = 0
    titles = []

    for x in soup.findAll('td', {'class': 'list-title'}):
        full_title = x.get_text()
        title = full_title[8:-1]

        if last__circ:
            last_read = title
            #first_in_list = title
            titles.append(last_read)
            print("variable last_read updated to: " + str(last_read))
            last__circ = False
        
        if last_read != title and count == 0:
            last_read = title
            #first_in_list = title
            titles.append(last_read)
            last__circ = False

        # Debug Code
        print(title)
        print(last_read)
        print(count)

        if last_read != title:
            if not_saw_my_last:
                titles.append(title)
                print("News to read ! (Appended to the titles list)")
        if last_read == title:
            not_saw_my_last = False
            print("Saw my last !")

        count += 1

# While Loop to be Active Always
run_app = True
while run_app:
    search_news()
    print(titles)
    if len(titles) != 0:
        for title in titles:
            send_message(token, chat_id, title)
            print("Sended Message")
        send_message(token, chat_id, comunications_school_link)
        print("Sended Link")
    time.sleep(10)
