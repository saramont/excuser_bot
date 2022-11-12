import requests
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

'''
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sono bok, un bot. Vaffantasca.")
    
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
 '''
    
def excuse(update: Update, context: CallbackContext):

    categories = ['family', 'office', 'children', 'college', 'party', 'funny', 'unbelievable', 'developers', 'gaming']
    url = "https://excuser.herokuapp.com/v1/excuse"
    headers = {}

    if (len(context.args) > 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please, choose only one valid category")
        return

    if (len(context.args) == 1 and not (context.args[0] in categories)):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please, choose a valid category")
        return

    if (len(context.args) == 1 and (context.args[0] in categories)):
        url = url+"/"+context.args[0]

    response = requests.request("GET", url, headers=headers)
    if response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response.json()[0].get('excuse'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, a strange error occurred :(")


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Are you in need of an excuse?\nI'm the right bot for you!\n\nType /excuse [category] to get the perfect excuse for you.\nType /excuse to get a random excuse.\n\nExcuse categories are:\n- family\n- office\n- children\n- college\n- party\n- funny\n- unbelievable\n- developers\n- gaming")
        


def main():
    
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher  

    excuse_handler = CommandHandler('excuse', excuse)
    dispatcher.add_handler(excuse_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    
    # start the bot
    updater.start_polling()
    
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
        
        
if __name__ == '__main__':
    main()