import sqlite3
import telebot
from newsapi import NewsApiClient
import requests

conn = sqlite3.connect("pybotdb.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS categories
                  (categorii text,
                   user_id INTEGER,
                   FOREIGN KEY (user_id) REFERENCES users (id))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS keywords
                  (keyw text)
               """)

conn.commit()


bot = telebot.TeleBot("Token")
@bot.message_handler(commands=['start'])
def send_welcome(message):
	user_id = message.from_user.id
	first_name = message.from_user.first_name
	bot.reply_to(message, "Приветствую вас на новостном канале, "+ first_name + "!\nИспользуйте команды:\n"
																				"/news - для просмотра топ новостей\n")
	print(user_id,first_name)
	cursor.execute("""INSERT INTO users (id) VALUES (?)""", (user_id,))
	conn.commit()
# @bot.message_handler(commands=['showmycategories'])
# def show_category(message):
# 	user_id = message.from_user.id
# 	first_name = message.from_user.first_name
# 	bot.reply_to(message, "Приветствую вас на новостном канале, "+ first_name + "!\nИспользуйте команды:\n"
# 																				"/news - для просмотра топ новостей\n")
# 	print(user_id,first_name)
# 	cursor.execute("""INSERT INTO users (id) VALUES (?)""", (user_id,))
# 	conn.commit()
@bot.message_handler(commands=['news'])
def echo_news(message):

	query_params = {
		"source": "bbc-news",
		"sortBy": "top",
		"apiKey": "newsapiKey"
	}
	main_url = " https://newsapi.org/v1/articles"

	res = requests.get(main_url, params=query_params)
	open_bbc_page = res.json()

	article = open_bbc_page["articles"]

	results = []

	for ar in article:
		results.append(ar["title"])
		bot.reply_to(message, results)
	for i in range(len(results)):
		print(i + 1, results[i])
	bot.reply_to(message, results)
bot.polling()
conn.close()