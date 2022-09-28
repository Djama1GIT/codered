# https://t.me/codered_demotivator_bot
import telebot
import os
import wget

from PIL import Image, ImageDraw, ImageFont
from yandeximagesparser.ImageParser import YandexImage

token = "YOUR_TOKEN_BOT"
bot = telebot.TeleBot(token)


def find(msg):
    parser = YandexImage()
    bot_err = False
    try:
        wget.download(parser.search(msg.split()[0], sizes=parser.size.medium)[0].url, out='inside.png')
    except:
        bot_err = True

    demotivator = Image.open('demotivator.jpg')
    go_away = Image.open('go_away.jpg')
    if not bot_err:
        i1 = Image.open('inside.png')
        i2 = None
        if i1.width / i1.height > 1.53:
            width_center = i1.width // 2
            right_width = int(i1.height * 1.53)
            left = width_center - right_width // 2
            up = 0
            right = width_center + right_width // 2
            down = i1.height
            i2 = i1.crop((left, up, right, down)).resize((800, 530))
        elif i1.width / i1.height < 1.53:
            height_center = i1.height // 2
            right_height = int(i1.width / 1.53)
            left = 0
            up = height_center - right_height // 2
            right = i1.width
            down = height_center + right_height // 2
            i2 = i1.crop((left, up, right, down)).resize((800, 530))
        else:
            i2 = i1.resize((800, 530))
        i2.save('inside.png')
        demotivator.paste(i2, (100, 68))
        demotivator_text = ImageDraw.Draw(demotivator)
        msg = msg.encode('cp1251')
        demotivator_text.text(
            (500, 670),
            msg.decode('cp1251'),
            anchor='ms',
            font=ImageFont.truetype(os.path.abspath('Impact.ttf'), 40),
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
    find(message.text.lower())
    with open('out.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.polling()
