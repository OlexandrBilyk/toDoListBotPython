from aiogram.fsm.state import State, StatesGroup

class AddTask(StatesGroup):
    name = State()
    description = State()
    deadline = State()  
    time = State()    
    
class DelTask(StatesGroup):
    id = State()

class SearchTask(StatesGroup):
    name = State()