# Technology calculator
Technological calculator for VVEK

## Стек использованных технологий
* Python
* tkinter

## Установка проекта на локальный компьютер из репозитория
* Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:<username>/technology_calculator.git
```
```
cd technology_calculator
```
* Установить и активировать виртуальное окружение:

Команда для Linux и macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Команда для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
* Установить зависимости pip install -r requirements.txt
```
pip install -r requirements.txt
```
* В корневой папке создать файл .env:
```
touch .env
```
* В файле .env добавить переменные из файла .env.example
* Запустить проект:

Команда для Linux и macOS:
```
python3 manage.py runserver
```
Команда для Windows:
```
python manage.py runserver
```

## Автор
* [Андрей Петров](https://github.com/AndreiPetrov94)