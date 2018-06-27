# -*- coding: utf-8 -*-
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import telepot
import os
import tweepy
import sys
from textblob import TextBlob
from googlesearch import search
from settings import TWITTER
import logging

logging.basicConfig(level=logging.INFO)
TelBot = telepot.Bot("587254001:AAFmCdn_YI8s79td4t48WFeXSXmLtpJFP2c")

Bot = ChatBot('Bast')
Bot.set_trainer(ListTrainer)
for arq in os.listdir('Bast_arq'):
    print("AAA")
    chats = open('Bast_arq/' + arq, 'r').readlines()
    Bot.train(chats)

filterQuest = ['como', 'porque' , 'por', 'que', ',' , '.', '?', '!', 'meu', 'esta']
filterBad = ['foder', 'vadia', 'negro', 'cu', 'arrombado', 'vadio', 'pênis']
notresponse = "Desculpe, ainda não há uma resposta"
print("\nSTART\n")

def twitter(quest, msg_id):
    TwiBot = ChatBot(
        "Bast",
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        database="./DBtwitter.storage.SQLStorageAdapter",
        twitter_consumer_key=TWITTER["CONSUMER_KEY"],
        twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
        twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
        twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
        trainer="chatterbot.trainers.TwitterTrainer",
        twitter_lang ="pt",
        random_seed_word=quest
    )

def google(quest, msg_id):
    sear = '"' + quest + '" google' 
    for result in search(sear, tld="co.in", num=1, stop=1, pause=2):
        print('Bot: ', result )
        TelBot.sendMessage(msg_id, str(result))

def Getmessage(msg):
    msg_id = msg['from']
    msg_id = msg_id['id']
    msg = msg['text']
    quest = msg
    searchen = str(msg)
    responseI = Bot.get_response(quest)
    print(msg)
    print(responseI.confidence)
    R = True
    if responseI == notresponse or responseI == "Ainda não há uma resposta" :
        R = False
    if float(responseI.confidence) > 0.6 and R == True:
        print('Bot: ', responseI )
        TelBot.sendMessage(msg_id, str(responseI))
    else:
        print('Bot: ', notresponse + ", porem podemos retirar uma resposta do twitter")
        TelBot.sendMessage(msg_id, notresponse + ", porem podemos retirar uma resposta do twitter e uma recomendação do google")
        twitter(quest, msg_id)
        google(quest, msg_id)
        if responseI != notresponse:
            try:
                with open('Bast_arq/novas_conversas.txt', 'a') as arq:
                    arq.write('\n' + str(msg))
                    arq.write('\n' + notresponse)
                    arq.close()
            except IOError:
                arq = open('Bast_arq/novas_conversas.txt', 'w')
                arq.write('perguntas')
                arq.write('\n' + str(msg))
                arq.write('\n' + notresponse)
                arq.close()
            for arq in os.listdir('Bast_arq'):
                chats = open('Bast_arq/' + arq, 'r').readlines()
                Bot.train(chats)
                    
TelBot.message_loop(Getmessage)

while True:
    pass

