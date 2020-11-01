import telebot
import requests
from bs4 import BeautifulSoup
import time

actual_notice = 120
titles = []
last = 0

# School Site
comunications_school_link = 'https://www.iistommasosalvini.edu.it/comunicazioni-e-progetti/comunicazioni-e-news'

# Bot Token
token = os.environ('token')
bot = telebot.TeleBot(token)
chat_id = os.environ('chat_id')


def search_news():
    global comunications_school_link, titles, actual_notice, last

    # Get Connection to the Web-Site
    result = requests.get(comunications_school_link)
    # Print Connection Status Code
    #print("School Website Connection Status Code: " + str(result.status_code))
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    last__circ = True

    for x in soup.findAll('td', {'class': 'list-title'}):
        full_title = x.get_text()

        if last__circ:
            try:
                last = int(full_title[14:17])
                last__circ = False
            except:
                run_search_for_notice_with_num = True
                while run_search_for_notice_with_num:
                    for i in soup.findAll('td', {'class': 'list-title'}):
                        new_title = i.get_text()
                        if new_title == full_title:
                            time.sleep(15)
                        elif new_title != full_title:
                            try:
                                last = int(full_title[14:17])
                                last__circ = False
                                run_search_for_notice_with_num = False
                            except:
                                time.sleep(15)

        if actual_notice != last:
            title = full_title[8:-1]
            titles.append(title)


# Bot function for Send Messages
def send_message(token, chat_id, text):
    url_req = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text=' + text
    telbot_result = requests.get(url_req)
    #print('\n \n \n Message sended \n')

# While Loop to be Active Always
if __name__ == "__main__":
    titles = []
    search_news()
    actual_notice = last
    if len(titles) != 0:
        for title in titles:
            send_message(token, chat_id, title)
        send_message(token, chat_id, comunications_school_link)
    time.sleep(10)
