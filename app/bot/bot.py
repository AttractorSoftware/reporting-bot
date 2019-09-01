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
PROJECT_SUFFIX = 'project'


def choice_checker(message):
    return message.text == CHOICE


@bot.message_handler(func=lambda message: message.text == CHOICE)
def choice_project_hanlder(message):
    projects_markup = create_projects_buttons()
    bot.send_message(message.chat.id, 'Please select your project in list', reply_markup=projects_markup)


def create_projects_buttons():
    markup = types.InlineKeyboardMarkup()
    for project in ['Keystone', 'Sametrica', 'Glimse', 'Garder']:
        button = types.InlineKeyboardButton(project, callback_data=f'{project}-{PROJECT_SUFFIX}')
        markup.add(button)
    return markup


@bot.callback_query_handler(func=lambda call: call.data.endswith(PROJECT_SUFFIX))
def select_project_calback_query(call):
    print('call ', call)
    sended_message = f'You selected the "{call.data}" project'
    bot.answer_callback_query(call.id, sended_message)
    bot.send_message(call.message.chat.id, sended_message)


@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Hello my friend. It is mock message.')


if __name__ == '__main__':
    print('bot started...')
    bot.polling()
