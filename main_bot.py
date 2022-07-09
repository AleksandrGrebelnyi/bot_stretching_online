import telebot
from flask import Flask, request
import os
import messages
from datetime import datetime

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
MY_ID = os.environ.get('MY_ID')
time_now = datetime.now()
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')  # paste token using os
user_answers = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.mes.get('GREETINGS'))
    bot.send_message(message.chat.id, messages.mes.get('FIO'))
    bot.register_next_step_handler(message, fio_step)


def fio_step(message):
    user_answers['<b>Дата</b>'] = time_now.strftime('%Y-%m-%d')
    user_answers['<b>Имя</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('PHONE'))
    bot.register_next_step_handler(message, phone_step)


def phone_step(message):
    user_answers['<b>Контакты</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('AGE'))
    bot.register_next_step_handler(message, age_step)


def age_step(message):
    user_answers['<b>Возраст</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('AD'))
    bot.register_next_step_handler(message, ad_step)


def ad_step(message):
    user_answers['<b>Откуда узнали</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('HOW_MANY_TRAININGS'))
    bot.register_next_step_handler(message, how_many_trainings_step)


def how_many_trainings_step(message):
    user_answers['<b>Сколько тренировок в неделю</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('AT_WHAT_TIME'))
    bot.register_next_step_handler(message, at_what_time_step)


def at_what_time_step(message):
    user_answers['<b>Удобное время для тренировок</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('PURPOSE'))
    bot.register_next_step_handler(message, underbelly_step)


def underbelly_step(message):
    user_answers['<b>Цель от тренировок</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('INTERESTS'))
    bot.register_next_step_handler(message, interestts_step)


def interestts_step(message):
    user_answers['<b>Какие направления интересны</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('HEALTH'))
    bot.register_next_step_handler(message, health_step)


def health_step(message):
    user_answers['<b>Противопоказания</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('UESTIONS'))
    bot.register_next_step_handler(message, questions_step)


def questions_step(message):
    user_answers['<b>Вопросы клиента</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('ARE_YOU_READY'))
    bot.register_next_step_handler(message, final_step)


@bot.message_handler(type=['text'])
def final_step(message):
    user_answers['<b>Вы готовы быть с нами</b>'] = message.text
    bot.send_message(message.chat.id, messages.mes.get('FINAL'))
    bot.send_message(MY_ID, f'{list(user_answers.keys())[0]} => {user_answers.get("<b>Дата</b>")}\n'
                            f'{list(user_answers.keys())[1]} => {user_answers.get("<b>Имя</b>")}\n'
                            f'{list(user_answers.keys())[2]} => {user_answers.get("<b>Контакты</b>")}\n'
                            f'{list(user_answers.keys())[3]} => {user_answers.get("<b>Возраст</b>")}\n'
                            f'{list(user_answers.keys())[4]} => {user_answers.get("<b>Откуда узнали</b>")}\n'
                            f'{list(user_answers.keys())[5]} => {user_answers.get("<b>Сколько тренировок в неделю</b>")}\n'
                            f'{list(user_answers.keys())[6]} => {user_answers.get("<b>Удобное время для тренировок</b>")}\n'
                            f'{list(user_answers.keys())[7]} => {user_answers.get("<b>Цель от тренировок</b>")}\n'
                            f'{list(user_answers.keys())[8]} => {user_answers.get("<b>Какие направления интересны</b>")}\n'
                            f'{list(user_answers.keys())[9]} => {user_answers.get("<b>Противопоказания</b>")}\n'
                            f'{list(user_answers.keys())[10]} => {user_answers.get("<b>Вопросы клиента</b>")}\n'
                            f'{list(user_answers.keys())[11]} => {user_answers.get("<b>Вы готовы быть с нами</b>")}\n')
    print(user_answers.items())


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://telega2bot.herokuapp.com/' + TOKEN)
    return 'Python Telegram Bot', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))