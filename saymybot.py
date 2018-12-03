from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
import settings
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update):
    text = '/start requested'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = "Hi {}! You wrote: {}".format(update.message.chat.first_name, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username, update.message.chat.id,
                update.message.text)
    update.message.reply_text(user_text)

def todays_constellation(bot, update):
    if len(update.message.text.split()) == 2:
        command, planet_name = update.message.text.split()
    now = datetime.now()
    planet_class = getattr(ephem, planet_name, None) #вернёт ephem.Mars()
    if planet_class:
        planet = planet_class(now) #planet = ephem.Mars(now)
        constellation = ephem.constellation(planet)
        update.message.reply_text(constellation)

def main():
    mybot = Updater (settings.API, request_kwargs=settings.PROXY)
    logging.info('Starting saymybot')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', todays_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()


main()