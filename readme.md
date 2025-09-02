# 🚀 Telegram Bot Guide

Этот проект — телеграм-бот на Python с использованием библиотеки **aiogram**.  
Ниже приведён пошаговый гайд, как запустить бота у себя.

---

## 🔧 Установка и запуск

### 1. Склонируйте репозиторий
```bash
git clone https://github.com/OlexandrBilyk/toDoListBotPython.git
```

### 2. Создайте виртуальное окружение

### Windows:

```python
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS:
```python
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости
```python
pip install -r requirements.txt
```

### 4. Создайте файл окружения .env

### В корне проекта создайте файл .env и пропишите туда токен бота (получить можно у @BotFather
):
```env
BOT_TOKEN=ваш_токен
```
### 5. Создайте файл data.json

### В корне проекта создайте файл data.json с содержимым:

```python
[]
```

### 6. Запустите бота
```python
python bot.py
```