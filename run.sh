#!/bin/bash
clear
echo "Запуск виртуального окружения..."
source myvenv/bin/activate
echo "Выберете на каком порту хотите запустить сервер:"
echo "1 - 8000"
echo "2 - 5000"
echo "3 - 9000"
read s
if [[ $s == 1 ]]
then
    echo "Запуск локального сервера. Порт 8000"
    echo
    python3 manage.py runserver 8000
elif [[ $s == 2 ]]
then
    echo "Запуск локального сервера. Порт 5000"
    echo
    python3 manage.py runserver 5000
elif [[ $s == 3 ]]
then
    echo "Запуск локального сервера. Порт 9000"
    echo
    python3 manage.py runserver 9000
else
    echo 'Ввод только 1-3! Давайте как все сначала'
fi


