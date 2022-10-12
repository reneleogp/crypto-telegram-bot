import os
import telebot
import time
import functions
import json
from millify import millify

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

trash_info = {
    "color", "png32", "png64", "webp32", "webp64", "totalSupply", "png128",
    "webp128", "uscompliant", "categories", "delta", "links"
}
not_money = {
    "pairs", "markets", "exchanges", "name", "symbol", "code", "visitors",
    "centralized", "circulatingSupply", "maxSupply", "rank"
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
    data = functions.overview()
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
                response += functions.format_line(name, data[val], money)

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
        data = functions.single(coin, True)
    else:
        data = functions.single(coin, False)

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
                response += functions.format_line(name, data[val], money)

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
    data = functions.list(min(limit, 20))
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
                    response += functions.format_line(name, coin[val], money)
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
    data = functions.list_exchanges(min(limit, 15))
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
                    response += functions.format_line(name, exchange[val],
                                                      money)
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
    data = functions.single_exchange(exchange)
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
                response += functions.format_line(name, data[val], money)

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
    data = functions.single(coin, False)
    if "error" in data or data['rate'] == None:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        r = ""
        r += functions.format_line("Amount", amount,
                                   False)[:-1] + " " + coin.upper() + "\n"
        r += functions.format_line("Price", data['rate'], True)
        r += functions.format_line("Value", data['rate'] * amount, True)
        bot.send_message(message.chat.id, r)


# Get change over time:
def get_change_request(message):
    request = message.text.split()
    if len(request) >= 2 and (request[0].lower() == "change"
                              or request[0].lower() == "changes"):
        return True
    else:
        return False


@bot.message_handler(func=get_change_request)
def send_change(message):
    code = message.text.split()[1].upper()
    data = functions.single(code, True)

    if 'error' in data:
        print(data)
        bot.send_message(message.chat.id, "No data!?")
    else:
        response = "Name: " + data['name'] + "\n"
        x1 = data['rate']
        response += functions.format_line("Price", x1, True)
        changes = {}

        t = int(time.time())
        t *= 1000

        functions.get_change(changes, "1 Year", code)
        functions.get_change(changes, "90 Days", code)
        functions.get_change(changes, "30 Days", code)
        functions.get_change(changes, "7 Days", code)
        functions.get_change(changes, "24 Hours", code)
        functions.get_change(changes, "1 Hour", code)

        for i in changes:
            x2 = changes[i]
            if x1 == None or x2 == None:
                pct = None
            else:
                try:
                    pct = ((x1 - x2) / abs(x2)) * 100
                except ZeroDivisionError:
                    pct = None

            if pct != None:
                pct = round(pct, 2)

            response += str(i) + ": " + str(pct) + "%\n"

        bot.send_message(message.chat.id, response)


bot.polling()
