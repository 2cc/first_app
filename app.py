import telebot
from telebot import types
import json
import random
import resources.demo_config as config
import csv


token = config.TOKEN
welcome_text = config.WELCOME_TEXT
images_folder = config.IMAGES_FOLDER
photos_folder = config.PHOTOS_FOLDER
persons_list = config.PERSONS_LIST
answers_file = config.ANSWERS_FILE

bot = telebot.TeleBot(token)


def send_question(message):
    persons = get_json_from_file(f'{persons_list}.json')
    person = random.choice(persons)
    photo_src = get_photo_src(person['id'])
    answer_options = get_answer_options(person['name'], person['gender'])
    markup = get_markup(answer_options)
    with open(photo_src, 'rb') as photo:
        question_msg = bot.send_photo(message.chat.id, photo, reply_markup=markup)
    bot.register_next_step_handler(question_msg, check_answer, person)


def get_json_from_file(file_name):
    with open(file_name, 'r',  encoding="utf8") as f:
        main_data = json.load(f)
        return main_data


def get_photo_src(person_id):
    photo_src = f'{photos_folder}/{person_id}.jpg'
    return photo_src


def get_answer_options(person_name, person_gender):
    answer_options = [person_name]
    persons = get_json_from_file(f'{persons_list}.json')
    random_persons_by_gender = [
        person for person in persons if person['gender'] == person_gender]
    while len(answer_options) < 4:
        random_person = random.choice(random_persons_by_gender)
        if random_person['name'] not in answer_options:
            answer_options.append(random_person['name'])
    random.shuffle(answer_options)
    return answer_options


def get_markup(answer_options):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(*(types.KeyboardButton(answer_option) for answer_option in answer_options))
    return markup


def check_answer(message, person):
    if message.text == person['name']:
        answer_msg = bot.send_message(
            message.chat.id, u'\U00002705' + ' Верно!')
    else:
        answer_msg = bot.send_message(
            message.chat.id, u'\U0000274C' + ' Ошибка!')
    write_answer_to_csv(message.from_user.id, person['name'], message.text)
    send_question(message)


def write_answer_to_csv(user_id, question, answer):
    with open(f'{answers_file}.csv', 'a') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow([user_id, question, answer])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Го!'))
    with open(f'{images_folder}/welcome_image.png', 'rb') as photo:
        welcome_msg = bot.send_photo(message.chat.id, photo, welcome_text, reply_markup=markup)
    bot.register_next_step_handler(welcome_msg, send_question)


bot.polling()
