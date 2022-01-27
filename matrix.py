from matrixbot import MatrixBot
from matrix_client.room import Room
from bs4 import BeautifulSoup
import asyncio
import datetime
import os
import requests
import time
import threading

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
watchlist = []

#watchfile location on bot's computer to keep track of links on bot restart
watchfile_location = "/home/john/matrix_in_stock_bot/watchlist.txt"

#######################################
#MATRIX SETTINGS
HOST="matrix.example.com",
BOT_DISPLAY_NAME="in-stock-bot",
BOT_ACCESS_TOKEN="GosaHFIpIyWnYIGOCArQPwNhYiLzzp_YwyGrcNJwkXLzZtJe",
BOT_USER_ID="@bot.in-stock:example.com"
matrix_bot_room_id= "!RigMuWPscsCUYxJPuy:example.com"
#MATRIX SETTINGS
#######################################

def add_to_list(bot, room, user, link):
    #find index of RTX-XXXX in link string
    ci = link.find("rtx")
    while True:
        try:
            # Making a GET request
            r = requests.get(link, headers=headers)
            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')
            #check if OOS
            s = soup.select('button[data-button-state="SOLD_OUT"]')
            if s:
                print(RandomVariableToCauseException)
            else:
                print("Stock found")
        except:
            print("{} Retry in 30 sec".format(datetime.datetime.now()))
            time.sleep(30)
            continue

        print("{} Sending matrix message.".format(datetime.datetime.now()))
        bot.say(room, "IN STOCK (lol??): "+ link[ci:ci+12] + "\n\n" + link, mention=user)
        time.sleep(60)

class MyBot(MatrixBot):
    def start(self):
        watchfile = open(watchfile_location, "r")
        watchfile_list = watchfile.read().split('\n')
        self.start_listening()
        for line in watchfile_list:
            if len(line.split()) == 2:
                link = line.split()[0]
                user = line.split()[1]
                watchlist.append(link)
                th = threading.Thread(target=add_to_list, args=(self, Room(self.client, matrix_bot_room_id), user, link))
                th.start()
        watchfile.close()
        while self.client.should_listen:
            pass

    def process_event(self, room, event):
        if event["type"] == "m.room.message":
            if event["content"]["body"].split()[0] == "!add":
                watchlist.append(event["content"]["body"].split()[1])
                watchfile = open(watchfile_location, "w")
                watchfile.write(event["content"]["body"].split()[1] + " " + event["sender"] + '\n')
                watchfile.close()
                self.say(room, "Link added to watch list!", mention=event["sender"])
                th = threading.Thread(target=add_to_list, args=(self, room, event["sender"], event["content"]["body"].split()[1]))
                th.start()
            elif event["content"]["body"].split()[0] == "!list":
                self.say(room, watchlist, mention=event["sender"])
            elif event["content"]["body"].split()[0] == "!help":
                self.say(room, "!add [link]\n\n!list")

bot = MyBot(
    host=HOST,
    display_name=BOT_DISPLAY_NAME,
    token=BOT_ACCESS_TOKEN,
    user_id=BOT_USER_ID
)
bot.start()
