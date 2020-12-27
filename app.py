import telebot
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
telegram_token = config['Telegram']['TOKEN']

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = config['Telegram']['WELCOME_MESSAGE']
    with open('images/welcome_image.png', 'rb') as photo:
        welcome_msg = bot.send_photo(
            message.chat.id, photo, welcome_text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
