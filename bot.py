import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import sys
from commands import START, GET_TASKS, ADD_TASKS, DEL_TASK_BY_ID, SEARCH_TASK_BY_NAME, BOT_COMMANDS
from data import register_user, get_tasks, add_task, del_task_by_id, get_task_by_name
from states import AddTask, DelTask, SearchTask
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()

@dp.message(START)
async def start_command(message: Message):
    id = str(message.from_user.id)
    register_user(id)
    await message.answer('start command')

@dp.message(SEARCH_TASK_BY_NAME)
async def search_command(message: Message, state: FSMContext):
    await state.set_state(SearchTask.name)
    await message.answer('Enter name of your task')

@dp.message(SearchTask.name)
async def search_command_name(message: Message, state: FSMContext) -> None:
    id = str(message.from_user.id)
    data = await state.update_data(name=message.text.strip())
    name = data.get('name', '')
    task = get_task_by_name(id, name)
    await state.clear()
    if task:
        for t in task:
            text = (
                f"━━━━━━━━━━━━━━━\n"
                f"🆔 <b>{t['_id']}</b>\n\n"
                f"📌 <b>{t['name']}</b>\n"
                f"📝 {t['description']}\n"
                f"⏰ <i>{t['deadline']}</i>\n"
                f"━━━━━━━━━━━━━━━"
            )
            await message.answer(text)

@dp.message(DEL_TASK_BY_ID)
async def del_task_command(message: Message, state: FSMContext):
    await state.set_state(DelTask.id)
    await message.answer('Enter id of your task')

@dp.message(DelTask.id)
async def del_task_id(message: Message, state: FSMContext):
    id = str(message.from_user.id)
    data = await state.update_data(id=message.text.strip())
    task_id = data.get('id', '')

    del_task_by_id(id, task_id)
    await state.clear()
    await message.answer('succsefully deleted')

@dp.message(GET_TASKS)
async def get_tasks_command(message: Message):
    id = str(message.from_user.id)
    tasks = get_tasks(id)
    if tasks:
        for t in tasks:
            text = (
                f"━━━━━━━━━━━━━━━\n"
                f"🆔 <b>{t['_id']}</b>\n\n"
                f"📌 <b>{t['name']}</b>\n"
                f"📝 {t['description']}\n"
                f"⏰ <i>{t['deadline']}</i>\n"
                f"━━━━━━━━━━━━━━━"
            )
            await message.answer(text)
    else:
        text = (
            "📭 У вас поки що <b>немає завдань</b>.\n\n"
            "➕ Щоб додати нове завдання, скористайтеся командою:\n"
            "<code>/add_tasks</code>"
        )
        await message.answer(text)

@dp.message(ADD_TASKS)
async def add_tasks_command(message: Message, state: FSMContext):
    await state.set_state(AddTask.name)
    await message.answer('Enter name of your task')

@dp.message(AddTask.name)
async def add_tasks_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddTask.description)
    await message.answer('Enter description of your task')

@dp.message(AddTask.description)
async def add_tasks_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddTask.deadline)
    await message.answer(
        "Выберите дедлайн:",
        reply_markup=await SimpleCalendar().start_calendar()
    )

@dp.message(AddTask.deadline)
async def add_tasks_deadline(message: Message, state: FSMContext):
    data = await state.update_data(deadline=message.text.strip())
    name = data.get("name", '')
    description = data.get("description", '')
    deadline = data.get("deadline", '')
    id = str(message.from_user.id)

    add_task(name, description, deadline, id)
    await message.answer('Task added')
    await state.clear() 

@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        data = await state.update_data(deadline=str(date.date()))

        name = data.get("name", "")
        description = data.get("description", "")
        deadline = data.get("deadline", "")
        user_id = str(callback_query.from_user.id)

        add_task(name, description, deadline, user_id)

        await callback_query.message.answer(
            f"✅ Задача додана!\n\n"
            f"📌 <b>{name}</b>\n"
            f"📝 {description}\n"
            f"⏰ Deadline: {deadline}"
        )
        await state.clear()

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    