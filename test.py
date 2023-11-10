import telebot
from telebot import types # для указание типов

import csv
import datetime
import os
import pandas as pd
import time

bot = telebot.TeleBot('6581012402:AAEoFDiSXeAJ1Es1heqqEESd-gLgpnTt4EM')

#путь к репозиторию на гитхабе к файлу с вопросами
url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions.csv'

#путь к файлу с вопросами
#path_to_quetions='D:/nur_bot/who_are_you_without_your_bot/Questions.csv'

#путь к ответам на вопросы (статистике)
path_to_statistic='D:/nur_bot/who_are_you_without_your_bot/data.csv'


df = pd.read_csv(url)

#массив с вопросами и ответами из файла
questions = {
    "question": df.question,
    "answer": [df.answer1, df.answer2, df.answer3, df.answer4],
    "count": len(df.question),
    "index_answer": 0
}


@bot.message_handler(commands=["start"])
def start(message):
    first_msg="Привет!"
    bot.send_message(message.chat.id, first_msg, reply_markup=None)
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton("OK"))
    second_msg="Тебе придется ответить на следующие вопросы 😁"
    bot.send_message(message.chat.id, second_msg, reply_markup=markup)


@bot.message_handler(content_types=['text'])

def ok(message):
    if (message.text=="OK"):
        questions["index_answer"]=0
        post=get_question_message(questions["index_answer"])
        bot.send_message(message.chat.id, post["text"],reply_markup=post["keyboard"])


def get_question_message(index_answer):
    keyboard=types.InlineKeyboardMarkup()
    for num,answer in enumerate(questions["answer"][index_answer]):
         keyboard.row(types.InlineKeyboardButton(f"{chr(num + 97)}) {answer}", callback_data=f"?ans&{num}"))
    text=f"Вопрос №{index_answer + 1}\n{questions['question'][index_answer]}\n"
    return{
        "text": text,
           "keyboard": keyboard,
    }



@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    if (questions["index_answer"]==questions["count"]):
        bot.edit_message_text(text='Спасибо за прохождение викторины 🙂', chat_id=query.message.chat.id, message_id=query.message.id,
						 reply_markup=None)
        questions["index_answer"]=0
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton("Следующий вопрос", callback_data="?next"))
        user_answer=questions["answer"][questions["index_answer"]][int(query.data.split("&")[1])]
        number_user_answer=int(query.data.split("&")[1])
        statistics_write(query.message.chat.id, user_answer, questions["index_answer"], number_user_answer, query.message.chat.username)
        questions["index_answer"]+=1
        bot.edit_message_text(text='Ответ записан ✅', chat_id=query.message.chat.id, message_id=query.message.id,
						 reply_markup=keyboard)
        


@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    if (questions["index_answer"]!=questions["count"]):
        post=get_question_message(questions["index_answer"])
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id, reply_markup=post["keyboard"])
    else:
        bot.edit_message_text(text='Спасибо за прохождение викторины 🙂', chat_id=query.message.chat.id, message_id=query.message.id,
						 reply_markup=None)
        questions["index_answer"]=0



def statistics_write(user_id, answer, index_answer, number_answer, username):
    data = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    statistics={'data': [data],
                'user_id': [user_id],
                'username': [username],
                'question': [questions["question"][index_answer]],
                'number_of_question': [index_answer],
                'answer': [answer],
                'answer_index': number_answer}
    
    df = pd.DataFrame(statistics)

    print(df)

    #df.to_csv('D:/nur_bot/who_are_you_without_your_bot/data.csv', index = False) 
    old_df = pd.read_csv(path_to_statistic)

    result=pd.concat([old_df,df])
    result.to_csv(path_to_statistic, index = False) 

    """with open('data.csv', 'a', newline="", encoding='UTF-8') as fil:
        wr = csv.writer(fil, delimiter=',')
        wr.writerow([statistics["user_id"], statistics["question"], statistics["number_of_question"], statistics["answer"]])"""


bot.polling(non_stop=True)