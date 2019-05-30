from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import datetime

PROXY = {'proxy_url': 'socks5://en.socksy.seriyps.ru:7777', 'urllib3_proxy_kwargs': {'username': 'tg-tmlen', 'password': 'q1n5spUC'}}
PLANETS = ['Mars', 'Mercury', 'Venus', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon']

#function thet greets user and explain about what is this bot
def greet_user(bot, update):
    greet = 'Привет,' + update.message.chat.first_name + '\n'
    text = greet + 'Тестовый бот\n/planet + <Имя планеты> Бот определит в каком она созвездии\n/help чтобы посмотреть список планет'
    update.message.reply_text(text)

#function outs list of avalible planets
def help_user(bot, update):
    text = 'Доступные планеты:\n'
    for planet in PLANETS:
        text += planet + '\n'
    update.message.reply_text(text)

#function thet answers to user his frase
def talk_to_me(bot, update):
    user_text = update.message.text 
    update.message.reply_text(user_text)

#function takes planet name and returns costellation in witch it is now
def check_constellation(planet):
    if planet == 'Mars':
        return (ephem.constellation(ephem.Mars(datetime.datetime.now())))
    elif planet == 'Mercury':
        return (ephem.constellation(ephem.Mercury(datetime.datetime.now())))
    elif planet == 'Venus':
        return (ephem.constellation(ephem.Venus(datetime.datetime.now())))
    elif planet == 'Jupiter':
        return (ephem.constellation(ephem.Jupiter(datetime.datetime.now())))
    elif planet == 'Saturn':
        return (ephem.constellation(ephem.Saturn(datetime.datetime.now()))) 
    elif planet == 'Uranus':
        return (ephem.constellation(ephem.Uranus(datetime.datetime.now())))
    elif planet == 'Neptune':
        return (ephem.constellation(ephem.Neptune(datetime.datetime.now())))    
    elif planet == 'Pluto':
        return (ephem.constellation(ephem.Pluto(datetime.datetime.now())))     
    elif planet == 'Sun':
        return (ephem.constellation(ephem.Sun(datetime.datetime.now())))     
    elif planet == 'Moon':
        return (ephem.constellation(ephem.Moon(datetime.datetime.now()))) 

#suggests user to input planet name
def get_constellation(bot, update):
    planet_name = update.message.text.split()[1]
    if planet_name in PLANETS:
        update.message.reply_text(check_constellation(planet_name))
    else:
        update.message.reply_text('Нет планеты '+ planet_name + '\nиспользуйте /help')

def wordcount(bot, update):
    user_words = update.message.text.split()
    words_count = 0
    for word in user_words:
        if word != '/wordcount' and word != '':
            words_count += 1
    update.message.reply_text(words_count)

def main():
    mybot = Updater('750789173:AAGVvB-vFBIl66gsYLqnbzUqSVP1fh9bphM', request_kwargs=PROXY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(CommandHandler("planet", get_constellation))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling(5, 20)
    mybot.idle()
main()
