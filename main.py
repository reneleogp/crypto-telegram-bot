import os
import telebot
import requests

TEL_API_KEY = os.environ['API_KEY']
WEB_API_KEY = os.environ['LiveCoinWatch_API_KEY']

query = {
     'currency': 'USD'  
}
my_headers = {
   'content-type': 'application/json',
    
}

response = requests.get("https://api.livecoinwatch.com/status" ,headers=my_headers)

print(response.status_code)

# session = requests.Session()
# bearer = 'Bearer {' + WEB_API_KEY + '}'
# session.headers.update({'x-api-key': bearer})
# session.headers.update({'content-type': 'application/json'})

# query = {
#     'currency': 'USD',
#     'sort': 'rank',
#     'order': 'ascending',
#     'offset': 0,
#     'limit': 2,
#     'meta': 'false'
# }
# response = session.get("https://api.livecoinwatch.com/coins/list",
#                        params=query)

                      



bot = telebot.TeleBot(TEL_API_KEY)


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey, hows it going?")


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")


# @bot.message_handler(commands=['list'])
# def list(message):

bot.polling()
