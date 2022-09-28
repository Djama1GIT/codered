# https://t.me/codered_demotivator_bot
import telebot
import os
import wget

from PIL import Image, ImageDraw, ImageFont
from yandeximagesparser.ImageParser import YandexImage

token = "token"
bot = telebot.TeleBot(token)


def find(msg):
    parser = YandexImage()
    bot_err = False
    try:
        wget.download(parser.search(msg, sizes=parser.size.medium)[0].url, out='inside.png')
    except:
        bot_err = True

    demotivator = Image.open('demotivator.jpg')
    go_away = Image.open('go_away.jpg')
    if not bot_err:
        i1 = Image.open('inside.png')
        demotivator = demotivator.resize((int(1000*(i1.size[0]/800)), int(800*(i1.size[1]/530))))
        demotivator.paste(i1, (int(100*(i1.size[0]/800)), int(68*(i1.size[1]/530))))
        demotivator_text = ImageDraw.Draw(demotivator)
        msg = msg.encode('cp1251')
        demotivator_text.text(
            (int(500*(i1.size[0]/800)), int(700*(i1.size[1]/530))),
            msg.decode('cp1251'),
            anchor='ms',
            font=ImageFont.truetype(os.path.abspath('Impact.ttf'), int(40*(i1.size[0]/800))),
            fill='white'
        )
        demotivator.save('out.png')
        os.remove('inside.png')
    else:
        go_away.save('out.png')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Для создания демотиватора просто напиши что-нибудь')


@bot.message_handler(content_types=['text'])
def answer(message):
    find(message.text.upper())
    with open('out.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.polling()
