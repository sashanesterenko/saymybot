
from glob import glob

from datetime import datetime
import ephem
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Hello, {}'.format(emo)
    contact_button = KeyboardButton('Send contact', request_contact=True)
    location_button = KeyboardButton('Send location', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Send derp','Change emoji'],
        [contact_button, location_button]])
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Hi {} {}! You wrote: {}".format(update.message.chat.first_name, emo, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username, update.message.chat.id,
                update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def change_emo(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Here you go, {}'.format(emo), reply_markup=get_keyboard())

def todays_constellation(bot, update, user_data):
    if len(update.message.text.split()) == 2:
        command, planet_name = update.message.text.split()
    now = datetime.now()
    planet_class = getattr(ephem, planet_name, None) #вернёт ephem.Mars()
    if planet_class:
        planet = planet_class(now) #planet = ephem.Mars(now)
        constellation = ephem.constellation(planet)
        update.message.reply_text(constellation, reply_markup=get_keyboard())

def send_derp_picture(bot, update, user_data):
    derp_list = glob('images/derp*.jp*g')
    derp_pic = choice(derp_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(derp_pic, 'rb'), reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']   

def get_keyboard():
    contact_button = KeyboardButton('Send contact', request_contact=True)
    location_button = KeyboardButton('Send location', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Send derp','Change emoji'],
        [contact_button, location_button]], resize_keyboard=True)

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Here you go: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Here you go: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def main():
    mybot = Updater (settings.API, request_kwargs=settings.PROXY)
    logging.info('Starting saymybot')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', todays_constellation, pass_user_data=True))
    dp.add_handler(CommandHandler('derp', send_derp_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Send derp)$', send_derp_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Change emoji)$', change_emo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


main()