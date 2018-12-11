from glob import glob

from datetime import datetime
import ephem
import logging
from random import choice

from telegram import ReplyKeyboardMarkup, KeyboardButton


from utils import get_keyboard, get_user_emo

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

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Here you go: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Here you go: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())
