# ╔══╦══╦══╗╔═══╦══╦══╦═══╦══╦═══╦══╗
# ║╔═╣╔╗║╔╗╚╣╔══╣╔═╣╔╗║╔═╗║╔═╣╔══╣╔═╝
# ║║─║║║║║╚╗║╚══╣╚═╣║║║╚═╝║║─║╚══╣╚═╗
# ║║─║║║║║─║║╔══╣╔═╣║║║╔╗╔╣║─║╔══╩═╗║
# ║╚═╣╚╝║╚═╝║╚══╣║─║╚╝║║║║║╚═╣╚══╦═╝║
# ╚══╩══╩═══╩═══╩╝─╚══╩╝╚╝╚══╩═══╩══╝
# ╔══╦═══╦══╗╔══╦══╦═══╗
# ║╔╗║╔═╗╠╗╔╝║╔═╣╔╗║╔═╗║
# ║╚╝║╚═╝║║║─║╚═╣║║║╚═╝║
# ║╔╗║╔══╝║║─║╔═╣║║║╔╗╔╝
# ║║║║║──╔╝╚╗║║─║╚╝║║║║
# ╚╝╚╩╝──╚══╝╚╝─╚══╩╝╚╝
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

import requests  # requests используется для получения запросов


class CodeForcesAPI:
    '''
    Этот класс описывает методы из Codeforces API
    '''

    def __init__(self, key, secret):  # На данный момент ключ и токен не
        # нужны, будут добавлены в следующих версиях для работы с приватными
        # данными пользователя
        self.key = key
        self.secret = secret

    '''
    Следующие методы описывают методы API, связанные с записями в блоге CodeForces
    '''

    def viewBlog(self, blog_id):  # Позволяет получать информацию о блоге по
        # id блога
        url = "http://codeforces.com/api/blogEntry.view?blogEntryId={}".format(
            blog_id)

        response = requests.get(url)
        json = response.json()

        if json['status'] != 'OK':
            result = [("Некорректный номер записи в блоге")]
        else:
            result = [(json['result']['authorHandle'] + ' пишет:',
                       'Рейтинг: ' + json['result']['content'],
                       json['result']['title'])]  # Возвращает имя автора блога,
            # заголовок блога, и текст блога

        return result

    def viewComments(self, blog_id):  # Позволяет получать информацию о
        # комментариях поста блога по id блога
        url = "http://codeforces.com/api/blogEntry.comments?blogEntryId={}".format(
            blog_id)

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result.append(("Некорректный номер записи в блоге"))
        else:
            comments = json['result']
            for comment in comments:
                result.append((comment['commentatorHandle'] + ' пишет:',
                               'Рейтинг: ' + str(comment['rating']),
                               comment['text']))
                # Возвращает имя автора комментария, рейтинг комментария,
                # и текст комментария

        return result

    '''
    Следующие методы описывают методы API, связанные с соревнованиями CodeForces
    '''

    def viewContests(self):  # Позволяет получать информацию о
        # последних 25 соревнованиях
        url = "http://codeforces.com/api/contest.list?gym=false"

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result.append(("Какие-то непредвиденные проблемы на сервере"))
        else:
            contests = json['result']
            for i in range(25):
                contest = contests[i]
                result.append(
                    (contest['name'],
                     contest['relativeTimeSeconds']))  # Возвращает для
                # каждого из 25 соревнований его название и время до начала
                # раунда

        return result[::-1]

    def viewRatingChange(self, name, contest_id):  # Позволяет получать
        # изменение рейтинга пользователя по его хендлу и id соревнования
        url = "http://codeforces.com/api/contest.ratingChanges?contestId={}".format(
            contest_id)

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result.append(("Некорректный номер соревнования"))
        else:
            ratings = json['result']
            for rating in ratings:
                if rating['handle'] == name:
                    result.append((rating['handle'],
                                   str(rating['oldRating']) + ' -> ' +
                                   str(rating['newRating'])))  # Кортеж с
                    # хендлом пользователя, старым рейтингом и рейтингом,
                    # полученным после соревнования
                    break
            if len(result) == 0:
                result.append(("Некорректное имя пользователя"))

        return result

    '''
    Следующие методы описывают методы API, связанные с задачами CodeForces
    '''

    def viewProblem(self, problem_name):  # Позволяет узнавать темы задач по
        # их имени
        url = " http://codeforces.com/api/problemset.problems"

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result.append(("Проблемы на сервере"))
        else:
            problems = json['result']
            for problem in problems:
                if problem['name'] == problem_name:
                    answer = ""
                    for tag in problem['tags']:
                        answer += tag + ';'
                    result.append((problem['name'], answer))  # Возвращает
                    # название задачи и набор тем
            if len(result) == 0:
                result.append(("Некорректное имя задачи"))

        return result

    def viewProblems(self, problem_tag, counter):  # Позволяет узнавать
        # имена задач по теме
        url = "http://codeforces.com/api/problemset.problems?tags={}".format(
            problem_tag)

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result.append(("Некорректный тег для задач"))
        else:
            problems = json['result']
            for i in range(min(counter, 25, len(problems))):
                problem = problems[i]
                answer = ""
                for tag in problem['tags']:
                    answer += tag + ';'
                result.append((problem['name'], answer))  # Возвращает список
                # имен задач и их темы

        return result

    '''
    Следующие методы описывают методы API, связанные с пользователями CodeForces
    '''

    def viewPosts(self, user_handle):  # Позволяет узнавать посты
        # пользователя по его хендлу
        url = "http://codeforces.com/api/user.blogEntries?handle={}".format(
            user_handle)

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result = [("Некорректное имя пользователя")]
        else:
            posts = json['result']
            for post in posts:
                result.append(
                    (post['authorHandle'] + ' пишет пост ' + post['title'],
                     'id поста: ' + str(post['id'])))  # Возвращает список
                # содержащий
                # автора поста, название поста и id поста

        return result

    def viewUser(self, user_handle):  # Позволяет узнавать информацию о
        # пользователе по его хендлу
        url = "https://codeforces.com/api/user.info?handles={}".format(
            user_handle)

        response = requests.get(url)
        json = response.json()

        if json['status'] != 'OK':
            result = [("Некорректное имя пользователя")]
        else:
            result = [(json['result'][0]['handle'], json['result'][0]['rank'],
                       str(json['result'][0]['rating']))]  # Возвращает хендл
            # пользователя, рейтинг и его ранг

        return result

    def viewRating(self, user_handle):  # Позволяет узнавать изменения
        # рейтинга пользователя по его хендлу
        url = "http://codeforces.com/api/user.rating?handle={}".format(
            user_handle)

        response = requests.get(url)
        json = response.json()
        result = []

        if json['status'] != 'OK':
            result = [("Некорректное имя пользователя")]
        else:
            results = json['result']
            for result in results:
                result.append((result['handle'], result['contestName'],
                               str(result['oldRating']) + ' -> ' +
                               str(result['newRating'])))  # Возвращает список
                # хендлов пользователя, названия соревнования, рейтинга до
                # соревнования и рейнтинга после соревнования

        return result
