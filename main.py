import os
from click import command 
import telebot
from pycoingecko import CoinGeckoAPI
from coins import coins

coin_client = CoinGeckoAPI()
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot("5587433203:AAEvScGpJH8VuCzwB0jaD6peNTru-P67X6k")


@bot.message_handler(commands=['info'])
def info(message):
    if len(message.text.strip().split()) == 2:
        coin = message.text.strip(' ').split()[1]
        if coin in coins:
            info = coin_client.get_coin_by_id(id=coin,localization='false', tickers='true', market_data='true', community_data='false', developer_data='false', sparkline='false')
            if info:
                current_price = info['market_data']['current_price']['usd']
                bot.reply_to(message, text=f'Price: {current_price}')
        else:
            bot.reply_to(message, text=f'Error, {coin} was not found')
    else:
        bot.reply_to(message, text='Error, please use /info <coin>')



if __name__ == '__main__':
    bot.polling()