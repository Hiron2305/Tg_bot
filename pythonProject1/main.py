import telebot
import random
import settings

bot = telebot.TeleBot(settings.API_KEY)
main_list = []
edit_word = []

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Команды: "/rnd" - рандомная фраза из списка, "/list" - управление список фраз ')
@bot.message_handler(commands=["rnd"])
def rnd(message):
    if len(main_list) > 0:
        bot.send_message(message.chat.id, random.choice(main_list))
    else:
        bot.send_message(message.chat.id, "Список фраз пуст")

@bot.message_handler(commands=["list"])
def edit(message):
    bot.send_message(message.chat.id, "'/add' - добавить фразу в список,'/show' - показать список всех фраз, '/delete' - удалить фразу из списка, '/edit' - отредактировать фразу из списка")

@bot.message_handler(commands=["add"])
def cmd_add(message):
    send = bot.send_message(message.chat.id, 'Введи фразу для добавления в список, а после введи следующую команду.')
    bot.register_next_step_handler(send, adding)
def adding(message):
    main_list.append(message.text)
    bot.send_message(message.chat.id, "Вы добавили фразу: " + message.text)

@bot.message_handler(commands=["show"])
def showing(message):
    a = ", ".join(main_list)
    bot.send_message(message.chat.id, 'Список фраз: ' + a)

@bot.message_handler(commands=["delete"])
def dell(message):
    send_del = bot.send_message(message.chat.id,'Введи фразу для удаления ее из списка, а после введи следующую команду.')
    bot.register_next_step_handler(send_del,deleting)

def deleting(message):
    if len(main_list) > 0:
        main_list.remove(message.text)
        bot.send_message(message.chat.id,"Вы удалили фразу: " + message.text)
    else:
        bot.send_message(message.chat.id, "Список пуст")

@bot.message_handler(commands=["edit"])
def edit(message):
    send_edit = bot.send_message(message.chat.id, "Напишите фразу, которую хотите заменить.")
    bot.register_next_step_handler(send_edit, editing_first)

def editing_first(message):
    edit_word.append(message.text)
    if edit_word[0] not in main_list:
        bot.send_message(message.chat.id,"Фразы нет в списке.")
    else:
        send_edit_first = bot.send_message(message.chat.id, "Напишите фразу, на которую хотите заменить.")
        bot.register_next_step_handler(send_edit_first, editing)

def editing(message):
    index_edit = main_list.index(edit_word[0])
    main_list[index_edit] = message.text
    y = ", ".join(main_list)
    bot.send_message(message.chat.id,"Теперь ваш список фраз выглядит так: " + y)

bot.polling(none_stop=True, interval=0)