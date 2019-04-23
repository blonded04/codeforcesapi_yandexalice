from flask import Flask, \
    request  # Нужно для запуска сервера, чтобы отвечать на запросы
import logging  # Нужно для логирования
import json  # JSON используется для обработки JSON запросов
from config import KEY, \
    SECRET  # В файле config.py находятся KEY и SECRET от API codeforces
from codeforces import \
    CodeAPI  # В файле codeforces.py находится класс CodeAPI с описанными
# методами


