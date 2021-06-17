# Можно фильтровать неактивных пользователей, создавая опросы, и помещая их в закреп. Люди, которые заходят в беседу, видят этот
    # Опрос, и голосуют в нем. Остальных пользователей можно кикнуть с помощью этого скрипта

import vk_api # Импорит библиотеки для работы с VK API. Для установки - "pip install vk_api"
from tokens import token # Создайте файл в данной директории "tokens.py" и создайте string переменную со значением токена вашего аккаунта

class KickUsers:

    peer_id = 2000000291 # Chat_ID беседы, в которой производить массовый кик не проголосовавших участников
    owner_id = 168227736 # ID Владельца опроса
    poll_id = 559844889 # ID Опроса, стоит после "owner_id"_ ...
    count = 1000 # Количество проголосовавших человек, которых нужно получить (1000 - максимум. Если количество превышает 1000, в запросе нужно будет ...
                    # ... использовать параметр offset, отвечающий за смещение)

    answer_id = 1667020798 # ID Варианта ответа, получить его можно с помощью метода здесь: https://vk.com/dev/polls.getById
    # (!!!) Если вариантов ответа > 1, требуется модернизация скрипта (!!!)

    def auth(self,): # Метод авторизации
        self.vk_session = vk_api.VkApi(token=token, api_version='5.126')
        self.vk = self.vk_session.get_api()

    def get_users(self,): # Метод получения всех пользователей беседы
        users = self.vk.messages.getConversationMembers(peer_id=self.peer_id)
        members = users['items']
        users = []
        for i in members:
            users.append(i['member_id'])
        return users
    
    def get_voted_users(self,): # Получения проголосовавших в опросе пользователей
        vote, = self.vk.polls.getVoters(owner_id=self.owner_id, poll_id=self.poll_id, answer_ids=self.answer_id, count=self.count)
        voted_users = vote['users']['items']
        return voted_users

if __name__ == "__main__":
    bot = KickUsers()
    bot.auth()
    users = bot.get_users()
    voted_users = bot.get_voted_users()

    chat_id = bot.peer_id - 2000000000

    for user in users:
        if user not in voted_users: # Если пользователя нет в списке проголосовавших
            try:
                bot.vk.messages.removeChatUser(chat_id=chat_id, user_id=user) # Производится кик
            except: # Ошибка возникает только, если пользователь - админ
                bot.vk.messages.send(peer_id=bot.peer_id, message=f'Не удалось кикнуть [id{user}|Этого пользователя]', random_id=0) # Сообщение об ошибке

    bot.vk.messages.send(peer_id=bot.peer_id, message=f'Я закончил.', random_id=0)