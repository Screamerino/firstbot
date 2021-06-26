import telebot
import os
from transfer import run_style_transfer

bot = telebot.TeleBot("947809948:AAEvV6HmYNsQx-fIE1QE1kXBVVVMUiFR2fs",
					parse_mode=None)

users = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, как твои дела?")

@bot.message_handler(commands=['begin'])	
def echo_all(message):
    users[message.chat.id] = {'started': True, 'content': False, 'style': False}
    bot.send_message(message.chat.id, 'So send me content image')


@bot.message_handler(content_types=['photo'])
def process_images(message):
    if message.chat.id in users:
        if not users[message.chat.id]['content']:
            users[message.chat.id]['content'] = message.photo[-1].file_id
            bot.send_message(message.chat.id, 'Send me style image')
        elif not users[message.chat.id]['style']:
            users[message.chat.id]['style'] = message.photo[-1].file_id
            bot.send_message(message.chat.id, 'Transfer started, wait ~1 min')
            call_transfer(message.chat.id)
            with open(str(message.chat.id) + '_styled.jpg', 'rb') as f:
                bot.send_photo(message.chat.id, f)
            remove_data(message.chat.id)
        #        heroku3.from_key(herokuapi).apps()[0].dynos()[0].restart()

def remove_data(user):
    for i in ['_content.jpg', '_style.jpg', '_styled.jpg']:
        os.remove(str(user) + i)
    del users[user]


def call_transfer(user):
        download(user)
        run_style_transfer(str(user) + '_content.jpg', str(user) + '_style.jpg', str(user) + '_styled.jpg')

def download(user):
	content_id = bot.get_file(users[user]['content'])
	with open(str(user) + '_content.jpg', 'wb') as f:
		f.write(bot.download_file(content_id.file_path))
	style_id = bot.get_file(users[user]['style'])
	with open(str(user) + '_style.jpg', 'wb') as f:
		f.write(bot.download_file(style_id.file_path))

bot.polling()