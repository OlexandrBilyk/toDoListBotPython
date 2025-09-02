from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START = Command('start')
GET_TASKS = Command('get_tasks')
ADD_TASKS = Command('add_tasks')
DEL_TASK_BY_ID = Command('del_task_by_id')
SEARCH_TASK_BY_NAME = Command('search_task_by_name')

BOT_COMMANDS = [
    BotCommand(command='start', description='Start using bot'),
    BotCommand(command='get_tasks', description='Get tasks from your list'),
    BotCommand(command='add_tasks', description='Add task to your list'),
    BotCommand(command='del_task_by_id', description='Delete task from your list'),
    BotCommand(command='search_task_by_name', description='Search task by name from your list'),
]