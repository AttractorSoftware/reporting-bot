from ..app import bot
from .actions import commands, callback_queries


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


action_classes = inheritors(commands.BaseAction)
actions = []

for ActionClass in action_classes:
    actions.append(ActionClass(bot))

print(len(actions))

callback_query_classes = inheritors(callback_queries.BaseCallbackQueryAction)
callback_queries = []

for CallbackQueryActionClass in callback_query_classes:
    callback_queries.append(CallbackQueryActionClass(bot))

print(len(callback_queries))
