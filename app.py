import telebot
from telebot import types
import os
import time
from flask import Flask, request

import DIYdb
import datebirth

secrettok = os.environ['my_secrettoken']

TOKEN = secrettok

bot = telebot.TeleBot(TOKEN)

application = Flask(__name__)

def buttonMK():
	markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
	item1=types.KeyboardButton("Здивуйте мене")
	item2=types.KeyboardButton("Розкладіть Аркан")
	item3=types.KeyboardButton("Поради баби Тари")

	markup.add(item1, item2)
	markup.add(item3)

	return markup

markup = buttonMK()

@bot.message_handler(commands=["getlog"])
def openflog(message):
    if message.chat.id == 521217070 or message.chat.id == 575699090:
        file = open("log.txt", "rb")
        bot.send_document(message.chat.id, file)
        file.close()

@bot.message_handler(commands=["usercount"])
def usercount(message):
    if message.chat.id == 521217070 or message.chat.id == 575699090:
        bot.send_message(message.chat.id, str(len(DIYdb.get_data("users")["users"])), reply_markup = markup)


@bot.message_handler(commands=["wakeup"])
def wakeupcll(message):
    if message.chat.id == 521217070 or message.chat.id == 575699090:
        DIYdb.getime(str(message.chat.id)+" - Wakeup - ")
        for i in DIYdb.get_data("users")["users"]:
            try:
                bot.send_message(i,"Баба Тара вже достатньо відпочила і може знову робити передбачення!!!!!!☺️☺️", reply_markup = markup)
            except telebot.apihelper.ApiTelegramException:
                pass


@bot.message_handler(commands=["start"])
def start(message, res = False):
	DIYdb.getime(str(message.chat.id)+" - Start - ")
	if DIYdb.write_json(message.chat.id, "users"):
		with open('srcfiles/1greeting.txt', 'r+', encoding='utf-8-sig') as file:
			greeting = file.read()
			bot.send_message(message.chat.id,greeting, reply_markup=markup)
	else:
		bot.send_message(message.chat.id,'З поверненням!!!☺️', reply_markup=markup)


@bot.message_handler(commands =["help"])
def help(message):
    DIYdb.getime(str(message.chat.id)+" - Help - ")
    bot.send_message(message.chat.id, "Я драйвова баба Тара, яка вміє дати хорошу пораду(сподіваюсь хорошу😅), розкласти ваш аркан за датою народження та просто сказати щось приємне!😊\nЯ не криптовалютчиця і не програмістка, а пенсії не вистачає аби побачити світ😒, тому, якшо вам подобається те що я роблю, то можете винагородити і копієчкою(хе-хе-хе)\n\n\t5375414130848707")

@bot.message_handler(commands =["sleep"])
def sleep(message):
    if message.chat.id == 521217070 or message.chat.id == 575699090:
        DIYdb.getime(str(message.chat.id)+" - Sleep - ")
        dataf = DIYdb.get_data("users")
        for i in dataf["users"]:
            try:
                bot.send_message(i,"Баба Тара втомилась від усіх справ і хоче трошки поспати😴😴(не турбувати)\nБаба Тара сповістить вас коли набереться сил(((")
            except telebot.apihelper.ApiTelegramException:
                pass

        DIYdb.cljson()

@bot.message_handler(content_types = ["document", "audio", "sticker", "photo", "video", "voice", "location", "contact", "video_note"])
def impropercontent(message):
    DIYdb.getime(str(message.chat.id)+" - "+ "Sent smth" +" - ")
    bot.send_message(message.chat.id, 'Я не розумію те що ви надіслали😅', reply_markup = markup)


@bot.message_handler(content_types = ["text"])
def send_text(message):

    if message.text == "Здивуйте мене":
        DIYdb.getime(str(message.chat.id)+" - "+ "Surprise me" +" - ")
        if DIYdb.write_json(message.chat.id, "predicted"):
            bot.send_message(message.chat.id,'Ви прекрасніііі!!!!🥰', reply_markup = markup)
        else:
            bot.send_message(message.chat.id,'Я вам вже казала що ви прекрасні? - Я скажу знову, ви прекрасні!!!!🥰',  reply_markup = markup)

    elif message.text == "Поради баби Тари":
        DIYdb.getime(str(message.chat.id)+" - "+ "Baba Tara advise" +" - ")
        bot.send_message(message.chat.id, DIYdb.advis("1advise.txt"), reply_markup = markup)

    elif message.text == "Розкладіть Аркан":
        DIYdb.getime(str(message.chat.id)+" - "+ "Arkan button" +" - ") 
        bot.send_message(message.chat.id,'Вкажіть свою дату народження:', reply_markup = types.ForceReply(selective=False, input_field_placeholder="dd.mm.yyyy"))
    else:
        dattm = datebirth.check_date(message.text)
        if dattm != None:
            if dattm == "date1":
                stic = open('srcfiles/wrongdate.webp', 'rb')
                bot.send_sticker(message.chat.id, stic)
                bot.send_message(message.chat.id, "Дату вказано неправильно! Введіть її знову:", reply_markup = types.ForceReply(selective=False, input_field_placeholder="dd.mm.yyyy"))
            else:

                DIYdb.getime(str(message.chat.id)+" - "+ "Arkan" +" - ")
                bot.send_message(message.chat.id, "Підбираю карти....")
                time.sleep(1)
                for x in datebirth.arkane(dattm):

                    img = open("srcfiles/"+str(x)+'.jpg', 'rb')
                    bot.send_photo(message.chat.id, img)
                    img.close()

                    bot.send_message(message.chat.id, datebirth.choice(x))
                    time.sleep(1.5)

                bot.send_message(message.chat.id,'Фух, наче все, якшо щось забула, то вибачайте😅😅\nСтарість - це далеко не радість😢', reply_markup = markup)

        else:
            if message.chat.id == 521217070 or message.chat.id == 575699090:
                try:
                    admmess = message.text.split("!! ")
                    if admmess[0] == "admin":
                        DIYdb.getime(str(message.chat.id)+" - Admin msg - ")
                        adminmes(admmess[1])
                    elif admmess[0] == "adminadv":
                        DIYdb.getime(str(message.chat.id)+" - Admin advise - ")
                        DIYdb.addtotxtfile(admmess[1], "1advise.txt")
                        bot.send_message(message.chat.id, 'Пораду додано!', reply_markup = markup)
                    else:
                        DIYdb.getime(str(message.chat.id)+" - "+ "Debil check" +" - ")
                        bot.send_message(message.chat.id, 'Я не розумію вас😅', reply_markup = markup)
                    
                except AttributeError:
                    DIYdb.getime(str(message.chat.id)+" - "+ "Debil check" +" - ")
                    bot.send_message(message.chat.id, 'Я не розумію вас😅', reply_markup = markup)
            else:          
                DIYdb.getime(str(message.chat.id)+" - "+ "Debil check" +" - ")
                bot.send_message(message.chat.id, 'Я не розумію вас😅', reply_markup = markup)

def adminmes(admessage):
    dataf = DIYdb.get_data("users")
    for i in dataf["users"]:
        try:
            bot.send_message(i, admessage, reply_markup = markup)
        except telebot.apihelper.ApiTelegramException:
            pass


@application.route("/"+ TOKEN, methods = ['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "Babka vstala!", 200

@application.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url = 'https://majestictgbot.herokuapp.com/' + TOKEN)
	return "Babka vstala!", 200