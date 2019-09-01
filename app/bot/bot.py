import os
from telebot import TeleBot, types

token = os.environ['TELEGRAM_BOT_TOKEN']
bot = TeleBot(token)


@bot.message_handler(commands=['hello'])
def hello_handler(message):
    bot.reply_to(message, 'Howdy, how are you doing?')


@bot.message_handler(commands=['register'])
def register_handler(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    choice_project_button = types.KeyboardButton('choice project')
    markup.add(choice_project_button)
    bot.send_message(message.chat.id, "Please, enter your email:", reply_markup=markup)


EMAIL_REGEXP = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
@bot.message_handler(regexp=EMAIL_REGEXP)
def email_handler(message):
    bot.send_message(message.chat.id,
                     "Registration confirmation! We sent you an email. Please check your mailbox.")


CHOICE = 'choice project'


def choice_checker(message):
    return message.text == CHOICE


@bot.callback_query_handler(func=lambda message: message == CHOICE)
def choice_project_hanlder(message):
    bot.send_message(message.chat.id, 'Please choice your project')


@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Hello my friend. It is mock message.')


print('bot started...')
bot.polling()
