#from distutils.cmd import Command
#from email import message
#from re import I
#import random
#from datetime import date
from calendar import TUESDAY
import telebot
from telebot import types
import datetime
from bs4 import BeautifulSoup
import requests
import re
import mechanize

import http.cookiejar

API_KEY =  ''
bot = telebot.TeleBot(API_KEY)

url = "https://rozklad.ztu.edu.ua/schedule/group/ПЛ-6"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

"""
with open ("Розклад групи ПЛ-6.html", "r", encoding='utf-8') as f:       
    doc = BeautifulSoup(f, "html.parser")
#In case the web page wont be available
"""

table = doc.find_all("table")
print(table)
table_monday1 = doc.find_all(day = "Понеділок 1")
table_tuesday1 = doc.find_all(day = "Вівторок 1")
table_wednesday1 = doc.find_all(day = "Середа 1")
table_thursday1 = doc.find_all(day = "Четвер 1")
table_friday1 = doc.find_all(day = "П'ятниця 1")

table_monday2 = doc.find_all(day = "Понеділок 2")
table_tuesday2 = doc.find_all(day = "Вівторок 2")
table_wednesday2 = doc.find_all(day = "Середа 2")
table_thursday2 = doc.find_all(day = "Четвер 2")
table_friday2 = doc.find_all(day = "П'ятниця 2")

datenow = datetime.datetime.now()
datethen = datetime.datetime(2024,1,1)

weekdate = (datenow-datethen).days
weeknum = (weekdate//7) + 1





@bot.message_handler(commands=["start"])
def start(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
    
    schedule_all_button = types.KeyboardButton("📅Розклад")
    schedule_today_button = types.KeyboardButton("📅Розклад на сьогодні")

    menu.add(schedule_all_button, schedule_today_button)
       
    bot.send_message(message.chat.id, "Привіт, {0.first_name}".format(message.from_user), reply_markup = menu)



@bot.message_handler(content_types = ['text'])
def bot_menu(message):
    
    

    def sched_func():    
        time_text = []
            
        for ii in req_day:
            x = ii.get("hour")
            time_text.append(x)
                        
        time_indx = -1
        
        for i in list(range(0, len(req_day))):
                            
            parse_text = []
            choise = req_day[i].get_text()
            
            if len(choise) == 1:
                time_indx += 1
                bot.send_message(message.chat.id, time_text[time_indx] + "\n" + "-------------------------", reply_markup = menu)

            elif len(choise) > 1:
                for line in choise.split('\n'):
                    parse_text.append(line) 
                    
                del parse_text[0:3] 
                del parse_text[-2:]
                del parse_text[-2]

                print(parse_text)

                subj_name = parse_text[0]
                subj_classroom = parse_text[1] + "\n" + "      " + parse_text[2].strip()
                subj_teacher = parse_text[3]  
                
                subj_total = "📕" + subj_name + "\n" + "\n" + "🏚️" + subj_classroom + "\n" + "\n" + "👩🏻‍🏫" + subj_teacher    
                
                time_indx += 1
                bot.send_message(message.chat.id, "🕓" + time_text[time_indx] + "\n" + "\n" + subj_total, reply_markup = menu)
                    


    monday_button = types.KeyboardButton("📅Понеділок")
    tuesday_button = types.KeyboardButton("📅Вівторок")
    wednesday_button = types.KeyboardButton("📅Середа")
    thursday_button = types.KeyboardButton("📅Четвер")
    friday_button = types.KeyboardButton("📅П'ятниця")
    back_button = types.KeyboardButton("🔙Назад")



    if message.text == "📅Розклад на сьогодні":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
        schedule_all_button = types.KeyboardButton("📅Розклад")
        schedule_today_button = types.KeyboardButton("📅Розклад на сьогодні")

        menu.add(schedule_all_button, schedule_today_button)
        
        if weeknum % 2 != 0:
            if datenow.strftime("%w") == "1":
                req_day = table_monday1
                sched_func()
            
            elif datenow.strftime("%w") == "2":
                req_day = table_tuesday1

                sched_func()
            
            elif datenow.strftime("%w") == "3":
                req_day = table_wednesday1
                sched_func()
            
            elif datenow.strftime("%w") == "4":
                req_day = table_thursday1
                sched_func()
            
            elif datenow.strftime("%w") == "5":
                req_day = table_friday1
                sched_func()
            
            elif datenow.strftime("%w") == "6" or "0":
                bot.send_message(message.chat.id, "Сьогодні вихідний", reply_markup = menu)
    

        elif weeknum % 2 == 0:
            if datenow.strftime("%w") == "1":
                req_day = table_monday2
                sched_func()
            
            elif datenow.strftime("%w") == "2":
                req_day = table_tuesday2
                sched_func()
            
            elif datenow.strftime("%w") == "3":
                req_day = table_wednesday2
                sched_func()
            
            elif datenow.strftime("%w") == "4":
                req_day = table_thursday2
                sched_func()
            
            elif datenow.strftime("%w") == "5":
                req_day = table_friday2
                sched_func()
            
            elif datenow.strftime("%w") == "6" or "0":
                bot.send_message(message.chat.id, "Сьогодні вихідний", reply_markup = menu)



        
        
        
        
        
        
    elif message.text == "📅Розклад":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
        schedule_first_button = types.KeyboardButton("📅Розклад на перший тиждень")
        scheduleb_second_button = types.KeyboardButton("📅Розклад на другий тиждень")

        menu.add(schedule_first_button, scheduleb_second_button)
    
        bot.send_message(message.chat.id, "Оберіть розклад", reply_markup = menu)

    

    elif message.text == "📅Розклад на перший тиждень":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        
        bot.send_message(message.chat.id, "Оберіть день тиждня", reply_markup = menu)

    
    elif message.text == "🔙Назад":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
        schedule_all_button = types.KeyboardButton("📅Розклад")
        schedule_today_button = types.KeyboardButton("📅Розклад на сьогодні")

        menu.add(schedule_all_button, schedule_today_button)

        bot.send_message(message.chat.id, "🔙", reply_markup = menu) 


    
    elif message.text == "📅Понеділок":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
 
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_monday1
        
        sched_func()

    elif message.text == "📅Вівторок":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
  
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)        
        req_day = table_tuesday1
        
        sched_func()

    elif message.text == "📅Середа":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
 
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_wednesday1
        
        sched_func()

    elif message.text == "📅Четвер":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
   
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_thursday1
        
        sched_func()


    elif message.text == "📅П'ятниця":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_friday1
        
        sched_func()

    
    



    elif message.text == "📅Розклад на другий тиждень":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        
        bot.send_message(message.chat.id, "Оберіть день тиждня", reply_markup = menu)


    elif message.text == "📆Понеділок":     
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_monday2
        
        sched_func()
            
        
    elif message.text == "📆Вівторок":    
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
    
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_tuesday2
        
        sched_func()
        
    elif message.text == "📆Середа":    
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
     
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_wednesday2
        
        sched_func()
        

    elif message.text == "📆Четвер":  
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
     
        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_thursday2
        
        sched_func()


    elif message.text == "📆П'ятниця":
        menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

        menu.add(monday_button, tuesday_button, wednesday_button,thursday_button,friday_button, back_button)
        req_day = table_friday2
        
        sched_func()





bot.polling(non_stop=True)