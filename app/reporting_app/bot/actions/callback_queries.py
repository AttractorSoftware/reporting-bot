from reporting_app.bot import utils
from telebot import types


class BaseCallbackQueryAction(object):
    conditions = {}

    def __init__(self, bot):
        self.bot = bot
        self.register()

    def register(self):
        klass = self.__class__

        @self.bot.callback_query_handler(**klass.conditions)
        def decorated(m):
            return self.do(m)

    def do(self, m):
        raise NotImplementedError


class SelectProject(BaseCallbackQueryAction):
    conditions = {
        'func': lambda call: call.data.endswith(utils.PROJECT_SUFFIX)
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, call):
        print('project call ', call)
        project_name = call.data.replace(f'-{utils.PROJECT_SUFFIX}', '')
        main_buttons_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        select_project_button = types.KeyboardButton(f'/select_project ({project_name} selected)')
        new_report_button = types.KeyboardButton('/new_report')
        new_ticket_button = types.KeyboardButton('/new_ticket')
        show_tickets_button = types.KeyboardButton('/show_tickets')

        main_buttons_markup.row(select_project_button, new_report_button)
        main_buttons_markup.row(show_tickets_button, new_ticket_button)

        callback_message = f'You selected the "{project_name}" project.\n'
        self.bot.answer_callback_query(call.id, callback_message)
        self.bot.send_message(call.message.chat.id, callback_message, reply_markup=main_buttons_markup)
        utils.show_tickets(call.message, self.bot)


class SelectTicket(BaseCallbackQueryAction):
    conditions = {
        'func': lambda call: call.data.endswith(utils.TICKET_SUFFIX)
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, call):
        print('call ', call)
        ticket_code = call.data.replace(f'-{utils.TICKET_SUFFIX}', '')
        sent_message = f'You selected the  "{ticket_code}" ticket.'
        self.bot.send_message(call.message.chat.id, sent_message)
