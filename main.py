''' Main file '''
from os import getenv
from json import loads
import logging
from dotenv import load_dotenv
import telebot
from telebot import types
from src.bot import Bot
from src.texts import ru
from src.storage import ExcelStorage
from src.auth import OAuth
from src.storage_api_client import StorageApiClient
from src.constants import SUBJECTS
from src.cache import Cache
from src.scheduler import Scheduler

# Initialize logging to a file
LOGS_FILENAME = 'logs.log'

logging.basicConfig(
    filename=LOGS_FILENAME,
    encoding='utf-8',
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)

# Load env
load_dotenv()

# Settings
spreadsheet_id = getenv('SPREADSHEET_ID')
contactsEmail = getenv('CONTACTS_EMAIL')
TOKEN = getenv('TELEGRAM_CHAT_TOKEN')

tgbot = telebot.TeleBot(TOKEN)

config = {
    'key': loads(getenv('EXCEL_KEY')),
    'path': getenv('EXCEL_PATH'),
    'storage_path': getenv('EXCEL_STORAGE_PATH')
}

# Auth service initialization
auth_srv = OAuth()

# Storage initialization
api_client_srv = StorageApiClient()
dataStorage = ExcelStorage(auth_srv, api_client_srv, spreadsheet_id, config)

# Cache initialization
cache = Cache()

# Bot initialization
bot = Bot(tgbot, types, dataStorage, cache, ru)

# Scheduler initialization
sch_config = {
    'log_filename': LOGS_FILENAME,
    'scheduler_time': int(getenv('SCHEDULER_TIME_SEC'))
}
scheduler = Scheduler(cache, sch_config)
scheduler.run()

# Message handlers
@tgbot.message_handler(commands=['start'])
def start(message):
    ''' "start" command handling '''
    bot.start(message)


@tgbot.message_handler(commands=['help'])
def help_handler(message):
    ''' "help" command handling '''
    bot.help(message)


@tgbot.message_handler(commands=['question_chemistry'])
def question_chemistry(message):
    ''' "question_chemistry" command handling '''
    bot.question(message, SUBJECTS['chemistry'])


@tgbot.message_handler(commands=['question_latin'])
def question_latin(message):
    ''' "question_latin" command handling '''
    bot.question(message, SUBJECTS['latin'])


@tgbot.message_handler(commands=['question_biology'])
def question_biology(message):
    ''' "question_biology" command handling '''
    bot.question(message, SUBJECTS['biology'])


@tgbot.message_handler(commands=['contacts'])
def contacts(message):
    ''' "contacts" command handling '''
    bot.contacts(message, contactsEmail)


@tgbot.message_handler(func=lambda message: message.text == ru['menuQuestionChemistry'])
def question_chemistry_menu(message):
    ''' Show question from chemistry on menu button click '''
    bot.question(message, SUBJECTS['chemistry'])


@tgbot.message_handler(func=lambda message: message.text == ru['menuQuestionLatin'])
def question_latin_menu(message):
    ''' Show question from latin on menu button click '''
    bot.question(message, SUBJECTS['latin'])


@tgbot.message_handler(func=lambda message: message.text == ru['menuQuestionBiology'])
def question_biology_menu(message):
    ''' Show question from latin on menu button click '''
    bot.question(message, SUBJECTS['biology'])


@tgbot.message_handler(func=lambda message: message.text == ru['menuContacts'])
def contacts_menu(message):
    ''' Show contacts information on menu button click '''
    bot.contacts(message, contactsEmail)


@tgbot.message_handler(func=lambda message: message.text == ru['menuHelp'])
def help_menu(message):
    ''' Show help information on menu button click '''
    bot.help(message)


@tgbot.callback_query_handler(lambda query: 'show_answer' in query.data )
def show_answer(message):
    ''' Show answer for question on inline button click '''
    bot.show_answer(message)


if __name__ == '__main__':
    logging.info('Polling is started')
    tgbot.polling()
