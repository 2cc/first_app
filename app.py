import telebot
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
telegram_token = config['Telegram']['TOKEN']

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()