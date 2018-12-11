


from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from handlers import *


import settings




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

if __name__ == "__main__":
    main()