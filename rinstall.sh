#!/bin/bash
clear
echo "установка виртуального окружения..."
python3 -m venv myvenv

echo "запуск виртуального окружения..."
source myvenv/bin/activate

echo "Установка ПО..."
pip3 install -r requirements.txt

python3 manage.py migrate
rm db.sqlite3
