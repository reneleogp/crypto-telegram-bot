import os
import telebot
import api_calls
from millify import millify

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

trash_info = {
    "color", "png32", "png64", "webp32", "webp64", "totalSupply", "pairs",
    "markets", "exchanges"
}

# Get help
@bot.message_handler(commands=['help'])
def info(message):
    f = open('help.txt', 'r')
    bot.send_message(message.chat.id, f.read())
    f.close()

# Start message
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello! Welcome to Crypto Info Bot, use /help to learn how to use the bot. Enjoy!"
    )

# Single coin detailed information request
def coin_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "info":
        return False
    else:
        return True


@bot.message_handler(func=coin_request)
def send_coin_info(message):
    coin = message.text.split()[1].upper()
    data = api_calls.single(coin)
    if 'error' in data:
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""

        for val in data:
            if val in "rate":
                response += ("Price: " + format_value(data[val]) + "\n")
            elif val not in trash_info:
                response += (val.capitalize() + ": " +
                             format_value(data[val]) + "\n")

        bot.send_message(message.chat.id, response)

# Coins list information request
def list_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "list":
        return False
    else:
        return True


@bot.message_handler(func=list_request)
def send_list_info(message):
    limit = int(message.text.split()[1])
    data = api_calls.list(min(limit, 20))
    if 'error' in data:
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""
        for coin in data:
            for val in coin:
                if val in 'code':
                    response += ("Name Code: ")
                if val in 'rate':
                    response += ("Price: ")
                if val in 'volume':
                    response += ("24H Volume: ")
                if val in 'cap':
                    response += ("Market Cap: ")
                response += (format_value(coin[val]) + "\n")
            response += "\n"

        bot.send_message(message.chat.id, response)

# Market overview request
def overview_request(message):
    request = message.text.split()
    if len(request) < 1 or request[0].lower() not in "overview":
        return False
    else:
        return True


@bot.message_handler(func=overview_request)
def send_overview(message):
    data = api_calls.overview()
    if 'error' in data:
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = "Market overview.\n"
        for val in data:
            if val in 'btcDominance':
                response += ("BTC Dominance: " +
                             str(millify((data[val] * 100), precision=2) + "%\n"))
            if val in 'volume':
                response += ("24H Volume: " + format_value(data[val])+"\n")
            if val in 'cap':
                response += ("Market Cap: " + format_value(data[val])+"\n")
            if val in 'liquidity':
                response += ("2% liquidity : " +
                             str(millify((data[val] * 100), precision=2) + "%\n"))    

        bot.send_message(message.chat.id, response)


# Exchanges list information request
def list_ex_request(message):
    request = message.text.split()
    if len(request) < 3 or request[0].lower() not in "exchanges" or request[1].lower() not in "list":
        return False
    else:
        return True


@bot.message_handler(func=list_ex_request)
def send_list_ex_info(message):
    limit = int(message.text.split()[2])
    data = api_calls.list_exchanges(min(limit, 15))
    if 'error' in data:
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""
        for exchange in data:
            for val in exchange:
                if val in 'markets':
                    response += val.capitalize() + format_value(exchange[val], True)
                else:
                    response += (format_value(coin[val]) + "\n")
            response += "\n"

        bot.send_message(message.chat.id, response)


# Format value function
def format_value(val, money):
    response = ""
    if money:
        response = "$"
    if type(val) == int or type(val) == float:
        if val < 1:
            response += str(format(val, '.6f'))
        else:
            response += str(millify(val, precision=2))
    else:
        response += str(val)
    return response + "\n"


bot.polling()
