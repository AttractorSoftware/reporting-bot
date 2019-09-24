from telebot import types
from reporting_app.bot import utils


class BaseAction(object):
    conditions = {}

    def __init__(self, bot):
        self.bot = bot
        self.register()

    def register(self):
        klass = self.__class__

        @self.bot.message_handler(**klass.conditions)
        def decorated(m):
            return self.do(m)

    def do(self, m):
        raise NotImplementedError


class NewReportAction(BaseAction):
    conditions = {
        'commands': ['new_report']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        report_setter.reset_step()
        report_setter.enable()
        text = report_setter.get_message()
        self.bot.send_message(m.chat.id, text)

    # @bot.message_handler(content_types=['text'])
    # def send_message(message):
    #     if report_setter.is_enabled():
    #         report_setter.set_step(message.text)
    #         if report_setter.is_finish():
    #             report_setter.disable()
    #             bot.send_message(
    #                 message.chat.id,
    #                 'Your report was saved. Do you add new report? If yes please click to "new report" button.')
    #         else:
    #             message_text = report_setter.get_message()
    #             bot.send_message(message.chat.id, message_text)


class NewTicketAction(BaseAction):
    conditions = {
        'commands': ['new_ticket']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        self.bot.send_message(m.chat.id, 'Please write ticket code down:')
        self.bot.register_next_step_handler(m, self.process_ticket_code_step)

    def process_ticket_code_step(self, m):
        try:
            chat_id = m.chat.id
            code = m.text
            if chat_id not in utils.user_dict:
                utils.user_dict[chat_id] = {}
            utils.user_dict[chat_id]['code'] = code
            self.bot.send_message(m.chat.id, 'Ok, then add title for ticket:')
            self.bot.register_next_step_handler(m, self.process_ticket_title_step)
        except Exception as e:
            self.bot.reply_to(m, 'ooops - process_ticket_code_step')

    def process_ticket_title_step(self, m):
        try:
            chat_id = m.chat.id
            title = m.text
            if chat_id not in utils.user_dict:
                utils.user_dict[chat_id] = {}
            code = utils.user_dict[chat_id]['code']
            self.bot.send_message(m.chat.id, f'Nice, now we can create ticket "{code}" with title "{title}"')
            utils.create_ticket(code, title)
            utils.show_tickets(m, self.bot)
        except Exception as e:
            self.bot.reply_to(m, 'ooops')


class PingAction(BaseAction):
    conditions = {
        'commands': ['ping']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        self.bot.reply_to(m, 'pong!')


class RegisterAction(BaseAction):
    conditions = {
        'commands': ['register']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        self.bot.send_message(m.chat.id, '/register command sent')
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        select_project_button = types.KeyboardButton('/select_project')
        markup.add(select_project_button)
        self.bot.send_message(m.chat.id, "Please, enter your email:", reply_markup=markup)


class ShowProjectsAction(BaseAction):
    conditions = {
        'commands': ['select_project']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        projects_markup = utils.create_projects_buttons()
        self.bot.send_message(m.chat.id, 'Please select your project from list', reply_markup=projects_markup)


class ShowTicketsAction(BaseAction):
    conditions = {
        'commands': ['show_tickets']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        utils.show_tickets(m, self.bot)


class StartAction(BaseAction):
    conditions = {
        'commands': ['start']
    }

    def __init__(self, bot):
        super().__init__(bot)

    def do(self, m):
        self.bot.send_message(m.chat.id, 'You know what to do')


REPORT_STEPS = [
    {
        'action': 'set_code',
        'message': 'Please enter number(code) of ticket'
    },
    {
        'action': 'set_title',
        'message': 'Please enter title of ticket'
    },
    {
        'action': 'set_comment',
        'message': 'Please add comment about what did you do?'
    },
    {
        'action': 'set_time',
        'message': 'Please enter your time spent (Example 6h (six hours)' +
                   '3m(three minutes), 6.5h (six and a half hours))'
    },
    {
        'action': 'set_status',
        'message': 'Please enter status of ticket'
    }
]


class Report(object):
    def __init__(self):
        self.code = ''
        self.title = ''
        self.comment = ''
        self.tracked_time = ''
        self.status = ''
        self.time = ''

    def set_code(self, code):
        self.code = code

    def set_title(self, title):
        self.title = title

    def set_comment(self, comment):
        self.comment = comment

    def set_time(self, time):
        self.time = time

    def set_status(self, status):
        self.status = status


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
        current = self.steps[self.step_index]['action']
        self._do_step(current, value)
        self.step_index += 1

    def _do_step(self, current, value):
        func = getattr(self.report, current)
        return func(value)

    def get_message(self):
        return self.steps[self.step_index]['message']

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self):
        return self._enabled


report_setter = ReportSetter(Report(), REPORT_STEPS)


# class FallbackAction(BaseAction):
#     @staticmethod
#     @bot.message_handler(func=lambda message: True, content_types=['text'])
#     def do(m):
#         # this is the standard reply to a normal message
#         bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")
