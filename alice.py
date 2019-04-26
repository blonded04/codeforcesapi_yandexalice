# ─╔══╦══╦══╦╗─╔╗╔══╦══╦═══╗
# ─╚╗╔╣╔═╣╔╗║╚═╝║║╔═╣╔╗║╔═╗║
# ──║║║╚═╣║║║╔╗─║║╚═╣║║║╚═╝║
# ╔╗║║╚═╗║║║║║╚╗║║╔═╣║║║╔╗╔╝
# ║╚╝╚╦═╝║╚╝║║─║║║║─║╚╝║║║║
# ╚═══╩══╩══╩╝─╚╝╚╝─╚══╩╝╚╝
# ╔══╦╗─╔══╦══╦═══╗╔══╗╔╗╔╗
# ║╔╗║║─╚╗╔╣╔═╣╔══╝║╔╗║║║║║
# ║╚╝║║──║║║║─║╚══╗║╚╝╚╣╚╝║
# ║╔╗║║──║║║║─║╔══╝║╔═╗╠═╗║
# ║║║║╚═╦╝╚╣╚═╣╚══╗║╚═╝║╔╝║
# ╚╝╚╩══╩══╩══╩═══╝╚═══╝╚═╝
# ╔══╦══╦════╦╗─╔╦═══╦════╗
# ║╔═╣╔╗╠═╗╔═╣╚═╝║╔══╩═╗╔═╝
# ║╚═╣╚╝║─║║─║╔╗─║╚══╗─║║
# ║╔═╣╔╗║─║║─║║╚╗║╔══╝─║║
# ║║─║║║║─║║─║║─║║╚══╗─║║
# ╚╝─╚╝╚╝─╚╝─╚╝─╚╩═══╝─╚╝

from flask import Flask, \
    request  # Нужно для запуска сервера, чтобы отвечать на запросы
import logging  # Нужно для логирования
import json  # JSON используется для обработки JSON запросов
from config import KEY, \
    SECRET  # В файле config.py находятся KEY и SECRET от API codeforces
from codeforces import \
    CodeForcesAPI  # В файле codeforces.py находится класс CodeAPI с методами

cf = CodeForcesAPI(KEY, SECRET)  # Связываемся с API CodeForces

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/post', methods=['POST'])  # При попытке отправить метод POST по
# адресу /post будет вызваны следующие функции, генирирующие JSON файл
def main():
    logging.info('Request: %r', request.json)

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json
    # преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog, которая
    # доделает JSON файл, добавляя в него варианты для диалога
    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    # Вовращаем JSON файл, нужный для Алисы
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Если пользователь новый, Алиса его поприветствует

        res['response']['text'] = '''
        Привет! Я умею работать с codeforces api!
        '''
        return

    # Для каждой из комманд связываем ее с запросом к CodeForces API
    if req['request']['original_utterance'].lower().split()[:3] == [
        'расскажи',
        'про',
        'запись'
    ]:
        # Получаем ответ
        response = cf.viewBlog(
            req['request']['original_utterance'].lower().split()[3])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif req['request']['original_utterance'].lower().split()[:4] == [
        'расскажи',
        'про',
        'комментарии',
        'записи'
    ]:
        # Получаем ответ
        response = cf.viewComments(
            req['request']['original_utterance'].lower().split()[4])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif req['request']['original_utterance'].lower().split()[:4] == [
        'расскажи',
        'про',
        'ближайшие',
        'соревнования'
    ]:
        # Получаем ответ
        response = cf.viewContests()
        result = "Ближайшие 25 соревнований: \n"
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif req['request']['original_utterance'].lower().split()[:4] == [
        'расскажи',
        'про',
        'изменение',
        'рейтинга'
    ]:
        # Получаем ответ
        response = cf.viewRatingChange(
            req['request']['original_utterance'].lower().split()[-1],
            req['request']['original_utterance'].lower().split()[4])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif req['request']['original_utterance'].lower().split()[:4] == [
        'расскажи',
        'про',
        'темы',
        'задачи'
    ]:
        # Получаем ответ
        response = cf.viewProblem(
            req['request']['original_utterance'].lower().split()[4])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif 'задач по теме' in req['request']['original_utterance']:
        # Получаем ответ
        response = cf.viewProblems(
            req['request']['original_utterance'].lower().split()[-1],
            req['request']['original_utterance'].lower().split()[2])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif 'Расскажи про записи пользователя' in req['request'][
        'original_utterance']:
        # Получаем ответ
        response = cf.viewPosts(
            req['request']['original_utterance'].lower().split()[-1])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif 'Расскажи о пользователе' in req['request'][
        'original_utterance']:
        # Получаем ответ
        response = cf.viewUser(
            req['request']['original_utterance'].lower().split()[-1])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    elif 'Расскажи об изменении рейтинга пользователя' in req['request'][
        'original_utterance']:
        # Получаем ответ
        response = cf.viewRating(
            req['request']['original_utterance'].lower().split()[-1])
        result = ""
        for answer in response:
            for string in answer:
                result += string + '\n'
            result += '\n'
        # Алиса отвечает пользователю
        res['response']['text'] = result
    else:
        # Если ни одна из комманд не подходит под маску, просим пользоваться
        # коммандами
        res['response']['text'] = 'Пользуйтесь коммандами, я вас не понимаю!'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
