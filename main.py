import os
import telebot
import api_calls
import json
from millify import millify

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

trash_info = {
    "color", "png32", "png64", "webp32", "webp64", "totalSupply", "png128",
    "webp128", "uscompliant"
}
not_money = {
    "pairs", "markets", "exchanges", "name", "symbol", "code", "visitors",
    "centralized", "circulatingSupply", "maxSupply"
}


# Get help
@bot.message_handler(commands=['help'])
def info(message):
    f = open('help.txt', 'r')
    bot.send_message(message.chat.id, f.read())
    f.close()

    # Database
    f = open("database.json", "r")
    data = json.load(f)
    f.close()

    data["help"] += 1
    f = open("database.json", "w")
    json.dump(data, f)
    f.close()


# Start message
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello! Welcome to Crypto Info Bot, use /help to learn how to use the bot. Enjoy!"
    )
    # Database
    f = open("database.json", "r")
    data = json.load(f)
    f.close()

    data["users"] += 1
    f = open("database.json", "w")
    json.dump(data, f)
    f.close()


# Market overview request
def overview_request(message):
    request = message.text.split()
    if len(request) < 1 or request[0].lower() != "overview":
        return False
    else:
        return True


@bot.message_handler(func=overview_request)
def send_overview(message):
    data = api_calls.overview()
    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = "Market overview.\n"
        for val in data:
            money = True
            if val in 'volume':
                name = "24H Volume"
            elif val in 'cap':
                name = "Market Cap"
            elif val in 'liquidity':
                name = ("2% liquidity")

            if val in 'btcDominance':
                response += (
                    "BTC Dominance: " +
                    str(millify((data[val] * 100), precision=2) + "%\n"))
            elif val not in trash_info:
                response += format_line(name, data[val], money)

        bot.send_message(message.chat.id, response)


# Single coin detailed information request
def coin_request(message):

    request = message.text.split()
    if len(request) >= 2 and (request[0].lower() == "price"
                              or request[0].lower() == "info"):
        return True
    else:
        return False


@bot.message_handler(func=coin_request)
def send_coin_info(message):
    coin = message.text.split()[1].upper()
    if message.text.split()[0].lower() in "info":
        data = api_calls.single(coin, True)
    else:
        data = api_calls.single(coin, False)

    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""
        for val in data:
            name = val.capitalize()
            money = True
            if val in "rate":
                name = "Price"
            if val in not_money:
                money = False

            if val not in trash_info:
                response += format_line(name, data[val], money)

        bot.send_message(message.chat.id, response)


# Coins list information request
def list_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() != "list":
        return False
    else:
        limit = request[1]
        if limit.isnumeric():
            return True
        else:
            return False


@bot.message_handler(func=list_request)
def send_list_info(message):
    limit = int(message.text.split()[1])
    data = api_calls.list(min(limit, 20))
    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""
        for coin in data:
            for val in coin:
                name = val.capitalize()
                money = True
                if val in "rate":
                    name = "Price"
                if val in 'code':
                    name = "Name Code"
                if val in 'volume':
                    name = "24H Volume"
                if val in 'cap':
                    name = "Market Cap"
                if val in not_money:
                    money = False

                if val not in trash_info:
                    response += format_line(name, coin[val], money)
            response += "\n"

        bot.send_message(message.chat.id, response)


# Exchanges list information request
def list_ex_request(message):
    request = message.text.split()
    if len(request) < 3 or request[0].lower() != "list" or (
            request[1].lower() != "exchanges"
            and request[1].lower() != "exchange"):
        return False

    else:
        limit = request[2]
        if limit.isnumeric():
            return True
        else:
            return False


@bot.message_handler(func=list_ex_request)
def send_list_ex_info(message):
    limit = int(message.text.split()[2])
    data = api_calls.list_exchanges(min(limit, 15))
    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = ""
        for exchange in data:
            for val in exchange:
                name = val.capitalize()
                money = True

                if val in 'code':
                    name = "Name Code"
                if val in 'volume':
                    name = "24H Volume"
                if val in "visitors":
                    name = "Daily Visitors"

                if val in not_money:
                    money = False

                if val not in trash_info:
                    response += format_line(name, exchange[val], money)
            response += "\n"

        bot.send_message(message.chat.id, response)


# Single exanchange detailed information request
def exchange_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() != "exchange":
        return False
    else:
        return True


@bot.message_handler(func=exchange_request)
def send_ex_info(message):
    exchange = message.text.split()[1].lower()
    data = api_calls.single_exchange(exchange)
    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:

        response = ""
        for val in data:
            name = val.capitalize()
            money = True
            if val in 'code':
                name = "Name Code"
            if val in 'volume':
                name = "24H Volume"
            if val in "visitors":
                name = "Daily Visitors"

            if val.lower() in not_money:
                money = False

            if val.lower() not in trash_info:
                response += format_line(name, data[val], money)

        bot.send_message(message.chat.id, response)


# Get real time price depending on amount
def calculator_request(message):
    request = message.text.split()
    if len(request) < 3 or request[0].lower() != "calculate":
        return False
    else:
        amount = request[2]
        try:
            float(amount)
            return True
        except ValueError:
            return False


@bot.message_handler(func=calculator_request)
def send_value_calculated(message):
    coin = message.text.split()[1].upper()
    amount = float(message.text.split()[2])
    data = api_calls.single(coin, False)
    if "error" in data or data['rate'] == None:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:

        r = ""
        r += format_line("Amount", amount, False)[:-1]+ " " + coin.upper() + "\n"
        r += format_line("Price", data['rate'], True)
        r += format_line("Value", data['rate'] * amount, True)
        bot.send_message(message.chat.id, r)


# Format line function
def format_line(name, val, money):
    if type(val) == int or type(val) == float:
        if val < 1:
            val = format(val, '.6f')
        else:
            val = millify(val, precision=2)

    return "{0}: {1}{2}\n".format(name, "$" if money else "", val)


bot.polling()
