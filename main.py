import os
from click import command 
import telebot
from pycoingecko import CoinGeckoAPI
from coins import coins
from newsapi import NewsApiClient
import time


newsapi = NewsApiClient(api_key='5753feb0897a4ff5a322ccd4289acede')
coin_client = CoinGeckoAPI()
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot("5587433203:AAEvScGpJH8VuCzwB0jaD6peNTru-P67X6k")


@bot.message_handler(commands=['info'])
def info(message):
    if len(message.text.strip().split()) == 2:
        coin = message.text.strip(' ').split()[1]
        print(f"The user requested info about {coin}:")
        print()
        if coin in coins:
            info = coin_client.get_coin_by_id(id=coin,localization='false', tickers='true', market_data='true', community_data='false', developer_data='false', sparkline='false')
            if info:
                current_price = info['market_data']['current_price']['usd']
                bot.reply_to(message, text=f'Price: {current_price}')
                print(f'Price: {current_price}')
                print()
                print('------------------------------------------------------')
                print()
        else:
            bot.reply_to(message, text=f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            print(f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            print()
            print('------------------------------------------------------')
            print()
    else:
        bot.reply_to(message, text='Error, please use /info <coin>')
        print('Error, please use /info <coin>')
        print(f"Number of args: {len(message.text.strip().split())}")
        print()
        print('------------------------------------------------------')
        print()
@bot.message_handler(commands=['news'])
def news(message):
    if len(message.text.strip().split()) == 3:
        coin = message.text.strip(' ').split()[1]
        language = message.text.strip(' ').split()[2]
        print(f"The user requested news about {coin}:")
        print()
        if coin in coins:
            top_headlines = newsapi.get_everything(q=coin, language=language, sort_by='popularity', page_size=10)
            if top_headlines['totalResults'] > 0  and top_headlines['articles']:
                for i in range(0,3):
                    bot.reply_to(message, text=f"[{i+1}]\n\nTitle: {top_headlines['articles'][i]['title']}\n\nDescription: {top_headlines['articles'][i]['description']}\n\nURL: {top_headlines['articles'][i]['url']}\n\nPublished: {top_headlines['articles'][i]['publishedAt'][:10]}\n\n")
                    print()
                    print(f"Title: {top_headlines['articles'][i]['title']}")
                    print(f"Description: {top_headlines['articles'][i]['description']}")
                    print(f"URL: {top_headlines['articles'][i]['url']}")
                    print(f"Published in: {top_headlines['articles'][i]['publishedAt'][:10]}")
                    print()
                    print('------------------------------------------------------')
                    print()
            else:
                bot.reply_to(message, text=f'Error, {coin} has no articles')
                print(f'Error, {coin} has no articles')
                print()
                print('------------------------------------------------------')
                print()
        else:
            bot.reply_to(message, text=f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            print(f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            print()
            print('------------------------------------------------------')
            print()
    else:
        bot.reply_to(message, text='Error, please use /news <coin> <language>, for languages available use /languages')
        print('Error, please use /news <coin>')
        print(f"Number of args: {len(message.text.strip().split())}")
        print()
        print

@bot.message_handler(commands=['language'])
def language(message):
    bot.reply_to(message, text='Possible language options: ar-de-en-es-fr-he-it-nl-no-pt-ru-sv-ud-zh.')
    print('Possible language options: ar-de-en-es-fr-he-it-nl-no-pt-ru-sv-ud-zh.')
    print()
    print('------------------------------------------------------')
    print()
    


if __name__ == '__main__':
    print('Initializing bot...')
    time.sleep(2)
    print('Bot is running...')
    time.sleep(2)
    print('waiting for commands...')
    time.sleep(2)
    print('available commands: /info <coin>')
    print('Press Ctrl+C to stop')
    print('Logs:')
    print()
    print('------------------------------------------------------')
    print()
    bot.polling()