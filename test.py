import telebot
from telebot import types # для указание типов

import csv
import datetime
from datetime import datetime
import os
import pandas as pd
import time

bot = telebot.TeleBot('6581012402:AAEoFDiSXeAJ1Es1heqqEESd-gLgpnTt4EM')

#путь к репозиторию на гитхабе к файлу с вопросами
_url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions.csv'

#путь к файлу с вопросами
path_to_quetions='D:/nur_bot/who_are_you_without_your_bot/Questions.csv'

#путь к ответам на вопросы (статистике)
path_to_statistic='D:/nur_bot/who_are_you_without_your_bot/data.csv'

#path to file with info about passed user
path_to_passed_user='D:/nur_bot/who_are_you_without_your_bot/user_is_passed.csv'

df = pd.read_csv(_url)
passed_df=pd.read_csv(path_to_passed_user)

#массив с вопросами и ответами из файла
questions = {
    "question": df.question,
    "answer": [df.answer1, df.answer2, df.answer3, df.answer4],
    "count": len(df.question),
    "index_answer": 0,
    "name_of_file": 0
}

#mass whth info about passed user
passed_user={
    "user_id": passed_df.user_id,
    "is_passed": passed_df.is_passed
}

#id Дениса
den_id=123704982

#время начала опроса
last_time=datetime.now()

@bot.message_handler(commands=["start"])
def start(message):
    first_msg="Привет!"
    bot.send_message(message.chat.id, first_msg, reply_markup=None)
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton("OK"))
    second_msg="Тебе придется ответить на следующие вопросы 😁"
    bot.send_message(message.chat.id, second_msg, reply_markup=markup)


@bot.message_handler(content_types=['text'])

def message(message):
    if (message.text=="OK"):
        global last_time
        last_time=datetime.now()
        str=check_passed(message.chat.id)
        if (str=={'is_passed'}):
            bot.send_message(message.chat.id, text="Вы уже прошли этот опрос",reply_markup=None)
        else:
            questions["index_answer"]=0
            post=get_question_message(questions["index_answer"])
            bot.send_message(message.chat.id, post["text"],reply_markup=post["keyboard"])

    #root rights
    elif (message.text=="root" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=root_keyboard()
        bot.send_message(message.chat.id, text="ROOT: Вы вошли с правами root",reply_markup=markup)
    #выход их рут прав
    elif(message.text=="Exit" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("OK"))
        bot.send_message(message.chat.id, text="Теперь вы обычный пользователь", reply_markup=markup)
    #change questions
    elif (message.text=="Change file with questions" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn=types.KeyboardButton("Questions.csv")
        btn1=types.KeyboardButton("Questions1.csv")
        btn2=types.KeyboardButton("Questions2.csv")
        btn3=types.KeyboardButton("Questions3.csv")
        btn4=types.KeyboardButton("Exit")
        markup.add(btn,btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id, text="ROOT: Выберите файл с вопросами", reply_markup=markup)

    elif (message.text=="Questions.csv" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=root_keyboard()
        url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions.csv'
        update_questions(url)
        questions["name_of_file"]=0
        bot.send_message(message.chat.id, text="ROOT: Теперь используются вопросы из файла Questions.csv", reply_markup=markup)
    elif (message.text=="Questions1.csv" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=root_keyboard()
        url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions1.csv'
        update_questions(url)
        questions["name_of_file"]=1
        bot.send_message(message.chat.id, text="ROOT: Теперь используются вопросы из файла Questions1.csv", reply_markup=markup)
    elif (message.text=="Questions2.csv" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=root_keyboard()
        questions["name_of_file"]=2
        url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions2.csv'
        update_questions(url)
        bot.send_message(message.chat.id, text="ROOT: Теперь используются вопросы из файла Questions2.csv", reply_markup=markup)
    elif (message.text=="Questions3.csv" and (message.chat.id==644440906 or message.chat.id==den_id)):
        markup=root_keyboard()
        url='https://raw.githubusercontent.com/Bre199ad11/Quiz/main/Questions3.csv'
        update_questions(url)
        questions["name_of_file"]=3
        bot.send_message(message.chat.id, text="ROOT: Теперь используются вопросы из файла Questions3.csv", reply_markup=markup)
    #end change questions
    #clear user_is_passed.csv
    elif (message.text=="Clear user_is_passed.csv and data.csv" and (message.chat.id==644440906 or message.chat.id==den_id)):
        cldf=passed_df
        cldf= cldf[0:0] 
        cldf.to_csv(path_to_passed_user, index = False)
        statistics={'data': [1],
                'user_id': [1],
                'username': [1],
                'question': [1],
                'number_of_question': [1],
                'answer': [1],
                'answer_index': 1,
                'seria_index': 1}
        cldf=pd.DataFrame(statistics)
        cldf= cldf[0:0] 
        cldf.to_csv(path_to_statistic, index = False)
        update_passed_user()
        bot.send_message(message.chat.id, text="ROOT: Файл user_is_passed.csv и data.csv были успешно очищены. Теперь пользователи могут проходить тестирование повторно.",
                          reply_markup=None)

    #end root rights


    else:
        send_msg="Извините, я вас не понимаю 😔"
        bot.send_message(message.chat.id, send_msg, reply_markup=None)

def get_question_message(index_answer):
    keyboard=types.InlineKeyboardMarkup()
    for num,answer in enumerate(questions["answer"][index_answer]):
         keyboard.row(types.InlineKeyboardButton(f"{chr(num + 97)}) {answer}", callback_data=f"?ans&{num}"))
    text=f"Вопрос №{index_answer + 1}\n{questions['question'][index_answer]}\n"
    return{
        "text": text,
           "keyboard": keyboard,
    }

def check_passed(user_id):
    text=""
    update_passed_user();
    for num, user_from_file in enumerate(passed_user["user_id"]):
        if (user_from_file==user_id):
            text="is_passed"
            break;
        else:
            text="not_passed"
    return{
        text
    }


@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    data_now=datetime.now()
    hour=abs(data_now.hour-last_time.hour)
    diff=data_now.minute-last_time.minute
    if (hour>=1): 
        diff+=60
    if (diff<10):
        if (questions["index_answer"]==questions["count"]):
            bot.edit_message_text(text='Спасибо за прохождение викторины 🙂', chat_id=query.message.chat.id, message_id=query.message.id,
		    				 reply_markup=None)
            questions["index_answer"]=0
            passed_write_to_file(query.message.chat.id)
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(telebot.types.InlineKeyboardButton("Следующий вопрос", callback_data="?next"))
            user_answer=questions["answer"][questions["index_answer"]][int(query.data.split("&")[1])]
            number_user_answer=int(query.data.split("&")[1])
            statistics_write(query.message.chat.id, user_answer, questions["index_answer"], number_user_answer, query.message.chat.username)
            questions["index_answer"]+=1
            bot.edit_message_text(text='Ответ записан ✅', chat_id=query.message.chat.id, message_id=query.message.id,
                            reply_markup=keyboard)
    else:
        bot.edit_message_text(text='Превышено ожидание ответа.', chat_id=query.message.chat.id, message_id=query.message.id,
			    			 reply_markup=None)


@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    data_now=datetime.now()
    hour=abs(data_now.hour-last_time.hour)
    diff=data_now.minute-last_time.minute
    if (hour>=1): 
        diff+=60
    if (diff<10):
        if (questions["index_answer"]!=questions["count"]):
            post=get_question_message(questions["index_answer"])
            bot.edit_message_text(post["text"], query.message.chat.id, query.message.id, reply_markup=post["keyboard"])
        else:
            bot.edit_message_text(text='Спасибо за прохождение викторины 🙂', chat_id=query.message.chat.id, message_id=query.message.id,
			    			 reply_markup=None)
            questions["index_answer"]=0
            passed_write_to_file(query.message.chat.id)
    else:
        bot.edit_message_text(text='Превышено ожидание ответа.', chat_id=query.message.chat.id, message_id=query.message.id,
			    			 reply_markup=None)

#обновление файла user_is_passed.csv
def passed_write_to_file(user_id):
    mass={
        "user_id": [user_id],
        "is_passed": "is_passed"
    }
    df = pd.DataFrame(mass)
    #df.to_csv('D:/nur_bot/who_are_you_without_your_bot/user_is_passed.csv', index = False) 
    old_df = pd.read_csv(path_to_passed_user)
    result=pd.concat([old_df,df])
    result.to_csv(path_to_passed_user, index = False) 

#запись статистики ответов
def statistics_write(user_id, answer, index_answer, number_answer, username):

    data = datetime.today().strftime("%Y-%m-%d-%H-%M")
    statistics={'data': [data],
                'user_id': [user_id],
                'username': [username],
                'question': [questions["question"][index_answer]],
                'number_of_question': [index_answer],
                'answer': [answer],
                'answer_index': number_answer,
                'seria_index': questions["name_of_file"]}
    
    df = pd.DataFrame(statistics)

    print(df)

    #df.to_csv('D:/nur_bot/who_are_you_without_your_bot/data.csv', index = False) 
    old_df = pd.read_csv(path_to_statistic)

    result=pd.concat([old_df,df])
    result.to_csv(path_to_statistic, index = False) 

#обновление user_is_passed.csv
def update_passed_user():
    passed_df=pd.read_csv(path_to_passed_user)
    passed_user["user_id"]=passed_df.user_id
    passed_user["is_passed"]=passed_df.is_passed



#обновление вопросов
def update_questions(url):
    table = pd.read_csv(url)
    questions["question"]=table.question
    questions["answer"]=[table.answer1, table.answer2, table.answer3, table.answer4]
    questions["count"]=len(table.question)
    questions["index_answer"]=0

#клавиатура суперпользователя (админа)
def root_keyboard():
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Change file with questions"))
    markup.add(types.KeyboardButton("Clear user_is_passed.csv and data.csv"))
    markup.add(types.KeyboardButton("Exit"))
    return markup



bot.polling(non_stop=True)