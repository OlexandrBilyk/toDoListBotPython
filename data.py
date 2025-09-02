import json
from nanoid import generate


def write_data(user_id, key, send_data):
    with open('data.json', 'r') as fh:
        data = json.load(fh)
    if user_id in data:
        data[user_id][key] = send_data
        
        with open('data.json', 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=4)

def register_user(user_id):
    with open('data.json', 'r') as fh:
        data = json.load(fh)

    if user_id not in data:
        data[user_id] = {
            'tasks': [],
        }
            
    with open('data.json', 'w') as fh:      
        json.dump(data, fh, ensure_ascii=False, indent=4)
        
def get_tasks(user_id):
    with open('data.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    if user_id in data:
        return data[user_id]['tasks']
    else:
        return []

def add_task(name, description, deadline, user_id):
    tasks = get_tasks(user_id)
    new_task = {
        '_id': generate(size=5),
        'name': name,
        'description': description,
        'deadline': deadline,
    }
    tasks.append(new_task)
    write_data(user_id, 'tasks', tasks)

def get_task_by_name(user_id, name):
    tasks = get_tasks(user_id)
    if tasks:
        task = [task for task in tasks if name in task['name']]
        if task:
            return task
        else: 
            return None
        
def get_task_by_id(user_id, id):
    tasks = get_tasks(user_id)
    if tasks:
        for t in tasks:
            if t['_id'] == id:
                return t
        
def del_task_by_id(user_id, id):
    tasks = get_tasks(user_id)
    if tasks and id:
        new_tasks = [t for t in tasks if t['_id'] != id]

        write_data(user_id, 'tasks', new_tasks)