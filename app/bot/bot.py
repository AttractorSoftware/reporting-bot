import os
from telebot import TeleBot, types

token = os.environ['TELEGRAM_BOT_TOKEN']
bot = TeleBot(token)


CHOICE_PROJECT = 'choice project'
NEW_REPORT = 'new report'
PROJECT_SUFFIX = 'project'
TICKET_SUFFIX = 'tiket'


class Report(object):
    def __init__(self):
        self.code = ''
        self.title = ''
        self.comment = ''
        self.tracked_time = ''
        self.status = ''

    def set_code(self, code):
        self.code = code

    def set_title(self, title):
        self.title = title

    def set_comment(self, title):
        self.title = title


class ReportSetter(object):
    def __init__(self, report, steps):
        self.report = report
        self.steps = steps
        self.step_index = 0
        self._enabled = False

    def reset_step(self):
        self.step_index = 0

    def is_finish(self):
        return self.step_index >= len(self.steps)

    def set_step(self, value):
        current = self.steps[self.steps_index]
        set_func = getattr(self.report, current)
        set_func(value)
        self.step_index += 1

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self):
        return self._enabled


REPORT_STEPS = ['set_code', 'set_title', 'set_comment']
report_setter = ReportSetter(Report(), REPORT_STEPS)


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


def choice_checker(message):
    return message.text == CHOICE_PROJECT


@bot.message_handler(func=lambda message: message.text == CHOICE_PROJECT)
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
def select_project_callback_query(call):
    print('project call ', call)
    project_name = call.data.replace(f'-{PROJECT_SUFFIX}', '')
    tickets_markup = create_tikets_buttons()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    choice_project_button = types.KeyboardButton('choice project')
    new_report_button = types.KeyboardButton('new report')
    markup.row(choice_project_button, new_report_button)
    callback_message = f'You selected the "{project_name}" project.\n'
    bot.answer_callback_query(call.id, callback_message)
    bot.send_message(call.message.chat.id, callback_message, reply_markup=markup)
    tickets_message = 'Please select ticket which assigned to you.'
    bot.send_message(call.message.chat.id, tickets_message, reply_markup=tickets_markup)


def create_tikets_buttons():
    markup = types.InlineKeyboardMarkup()
    mock_tickets = [
        ('CKL-114', 'Add some changes'),
        ('TEST-3254', 'Fix tests fixtures for unit tests'),
        ('GMP-478', 'Fix database data'),
        ('PTSK-1145', 'Realize data science implementation for application\'s core')
    ]
    for ticket in mock_tickets:
        code, title = ticket
        button = types.InlineKeyboardButton(f'[{code}] - {title}', callback_data=f'{code}-{TICKET_SUFFIX}')
        markup.add(button)
    return markup


@bot.message_handler(func=lambda message: message.text == NEW_REPORT)
def new_report_callback_query(message):
    report_setter.reset_step()
    report_setter.enable() 
    text = 'Please number(code) of ticket:'
    bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data.endswith(TICKET_SUFFIX))
def select_ticket_callback_query(call):
    print('call ', call)
    ticket_code = call.data.replace(f'-{TICKET_SUFFIX}', '')
    sended_message = f'You selected the  "{ticket_code}" ticket.'
    bot.send_message(call.message.chat.id, sended_message)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if report_setter.is_enabled():
        report_setter.set_step(message.text)
        if report_setter.is_finish():
            report_setter.disable()
    bot.send_message(message.chat.id, 'Hello my friend. It is mock message.')


if __name__ == '__main__':
    print('bot started...')
    bot.polling()
