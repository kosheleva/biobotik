''' Bot class implementation'''
import logging
from utils import get_random_number, get_current_date


class Bot:
    ''' Bot is responsible to handle user's commands '''


    def __init__(self, bot, types, storage, cache, texts):
        self.lang = 'ru'
        self.txt = texts

        self.bot = bot
        self.types = types
        self.data_storage = storage
        self.cache = cache

        logging.info('Bot is initialized.')


    def start(self, message):
        ''' "start" command handler '''
        logging.info('Start command requested.')

        markup = self.types.ReplyKeyboardMarkup(resize_keyboard=True)
        chemistry_btn = self.types.KeyboardButton(self.txt['menuQuestionChemistry'])
        latin_btn = self.types.KeyboardButton(self.txt['menuQuestionLatin'])
        biology_btn = self.types.KeyboardButton(self.txt['menuQuestionBiology'])
        contacts_btn = self.types.KeyboardButton(self.txt['menuContacts'])
        help_btn = self.types.KeyboardButton(self.txt['menuHelp'])

        markup.add(chemistry_btn, latin_btn, biology_btn, contacts_btn, help_btn)

        img = 'src/biobotik.png'

        return self.bot.send_photo(
            message.chat.id,
            photo=open(img, 'rb'),
            caption=self.txt['welcomeMsg'],
            reply_markup = markup
        )


    def help(self, message):
        ''' "help" command handler '''
        logging.info('Help command requested.')

        return self.bot.send_message(
            message.chat.id,
            f'''
{self.txt["helpMsg"]}
<b>/start</b> {self.txt["helpMsgStart"]}
<b>/help</b> {self.txt["helpMsgHelp"]}
<b>/question_chemistry</b> {self.txt["helpMsgQuestionChemistry"]}
<b>/question_latin</b> {self.txt["helpMsgQuestionLatin"]}
<b>/question_biology</b> {self.txt["helpMsgQuestionBiology"]}
<b>/contacts</b> {self.txt["helpMsgContacts"]}
                ''',
            parse_mode='html'
        )


    def question(self, message, subject):
        ''' "question" command handler '''

        logging.info('Question command requested on %s.', subject)

        chat_id = message.chat.id
        try:
            total_rows = self.get_total_rows_count(subject)
            start_row_number = 1
            step = 1

            question_number = get_random_number(start_row_number, total_rows, step)

            question = self.data_storage.get_question(subject, question_number)

            markup = self.types.InlineKeyboardMarkup(row_width=1)

            answer_btn = self.types.InlineKeyboardButton(
                text=self.txt['showAnswerMsg'],
                callback_data=f"show_answer_{chat_id}_{subject}_{question_number}"
            )

            markup.add(answer_btn)

            if question['question_image']:
                return self.bot.send_photo(
                    chat_id,
                    photo = question['question_image'],
                    caption=f"{question['category']}: {question['question']}",
                    reply_markup = markup
                )

            return self.bot.send_message(
                chat_id,
                f"{question['category']}: {question['question']}",
                reply_markup=markup
            )

        except Exception as e:
            logging.error('Error on question request.')
            logging.exception(e)

            return self.bot.send_message(chat_id, self.txt['serviceErrorMsg'])


    def contacts(self, message, email):
        ''' "contacts" command handler '''

        logging.info('Contacts command requested.')

        msg = self.txt['contactsMsg'].replace('{{email}}', email)

        return self.bot.send_message(
                message.chat.id,
                f'''{msg}''',
                parse_mode='html'
            )


    def show_answer(self, message):
        ''' Show answer callback handler '''

        logging.info('Show answer requested.')

        splitted_data = message.data.split('_')
        chat = int(splitted_data[2])
        subject = splitted_data[3]
        question_number = int(splitted_data[4])

        question = self.data_storage.get_question(subject, question_number)

        if question["answer_image"]:
            return self.bot.send_photo(
                    chat,
                    photo=question["answer_image"],
                    caption=f'''{question["answer"]}''',
                    parse_mode='html'
                )

        return self.bot.send_message(chat, f'''{question["answer"]}''', parse_mode='html')


    def get_total_rows_count(self, subject):
        ''' 
        Function for getting total storage rows count.
        Value in cache is updated once per day.
        '''

        date = get_current_date()
        key = f'{date}:{subject}'
        cached_rows_count = self.cache.get(key)

        logging.info('Cached rows count is: %s.', cached_rows_count)

        if cached_rows_count:
            return cached_rows_count

        total_rows = self.data_storage.get_total_rows_count(subject)
        self.cache.set(key, total_rows)

        logging.info('Total rows requested from storage: %s.', total_rows)

        return total_rows
