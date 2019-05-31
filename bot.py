from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import datetime
import json
import logging

from game import Game


PROXY = {'proxy_url': 'socks5://en.socksy.seriyps.ru:7777', 'urllib3_proxy_kwargs': {'username': 'tg-tmlen', 'password': 'q1n5spUC'}}
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

PLANETS = ['Mars', 'Mercury', 'Venus', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon']
game = Game()


#function thet greets user and explain about what is this bot
def greet_user(bot, update):
    greet = 'Привет,' + update.message.chat.first_name + '\n'
    text = greet + 'Тестовый бот\n/planet + <Имя планеты> Бот определит в каком она созвездии\n/help чтобы посмотреть список планет\n/wordcount + <фраза> вернет количество слов в фразе\n/next_full_moon покажет дату ближайшего полнолуния\n/cities запустит игру в города'
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

#takes user frase and returns words count
def wordcount(bot, update):
    user_words = update.message.text.split()
    words_count = 0
    for word in user_words:
        if word != '/wordcount' and word != '':
            words_count += 1
    update.message.reply_text(words_count)
    if words_count == 0:
        update.message.reply_text('Нужно ввести текст после команды /wordcount и бот посчитает количество слов в нём\nНапример "/wordcount Тут три слова"')

#calculate date of next full moon
def next_full_moon(bot, update):
    update.message.reply_text(f'Ближайшая полная луна будет {ephem.next_full_moon(datetime.date.today())}')

def cities_game(bot, update, args):
    if len(args) == 0:
        if game.prev_city[-1] in ['ь','ы','ъ']:
            update.message.reply_text(game.prev_city + f', вам на {game.prev_city[-2]}')
        else:
            update.message.reply_text(game.prev_city + f', вам на {game.prev_city[-1]}')
    else:
        if game.player_turn:
            result = game.try_city(args[0])
            if result == args[0].lower():
                update.message.reply_text(game.bot_turn())

            else: 
                update.message.reply_text(result)

def calc(bot, update):
    operators = ['+', '-', '*', '/', '%']
    command = update.message.text.replace('/calc ', '')
    operator = ''
    for opr in operators:
        if operator in command:
            print('success')
            operator = opr
            print(operator)
            break
    print(operator, command.split(operator)[0], command.split(operator)[1])
    if operator == '+':
        update.message.reply_text(float(command.split(operator)[0]) + float(command.split(operator)[1]))
    elif operator == '-':
        update.message.reply_text(float(command.split(operator)[0]) - float(command.split(operator)[1]))
    elif operator == '*':
        update.message.reply_text(float(command.split(operator)[0]) * float(command.split(operator)[1]))
    elif operator == '/':
        update.message.reply_text(float(command.split(operator)[0]) / float(command.split(operator)[1]))
    elif operator == '%':
        update.message.reply_text(float(command.split(operator)[0]) % float(command.split(operator)[1]))

def main():

    mybot = Updater('750789173:AAGVvB-vFBIl66gsYLqnbzUqSVP1fh9bphM', request_kwargs=PROXY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(CommandHandler("planet", get_constellation))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
    dp.add_handler(CommandHandler('cities', cities_game, pass_args=True))
    dp.add_handler(CommandHandler('calc', calc))
    mybot.start_polling(5, 20)
    mybot.idle()
main()
