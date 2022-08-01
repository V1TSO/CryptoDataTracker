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
languages = ["ar","de","en","es","fr","he","it","nl","no","pt","ru","sv","ud","zh"]

@bot.message_handler(commands=['info'])
def info(message):
    if len(message.text.strip().split()) == 2:
        coin = message.text.strip(' ').split()[1]
        print(f"The user requested info about {coin}:")
        print()
        if coin in coins:
            info = coin_client.get_coin_by_id(id=coin,localization='false', tickers='true', market_data='true', community_data='false', developer_data='false', sparkline='false')
            if info:
                current_homepage = info['links']['homepage'][0]
                current_blockchain = info['links']['blockchain_site'][0]
                current_forum = info['links']['official_forum_url'][0]
                current_subreddit = info['links']['subreddit_url']
                current_genesis = info['genesis_date']
                current_mc_rank = info['market_cap_rank']
                current_ath = info['market_data']['ath']['usd']
                current_ath = "${:,.2f}".format(current_ath)
                current_ath_change = round(info['market_data']['ath_change_percentage']['usd'], 2)
                current_ath_date = info['market_data']['ath_date']['usd'][:10]
                current_atl = info['market_data']['atl']['usd']
                current_atl = "${:,.2f}".format(current_atl)
                current_atl_change = round(info['market_data']['atl_change_percentage']['usd'], 2)
                current_atl_date = info['market_data']['atl_date']['usd'][:10]
                current_price = info['market_data']['current_price']['usd']
                current_price = "${:,.2f}".format(current_price)
                current_mcap = info['market_data']['market_cap']['usd']
                current_mcap = "${:,.2f}".format(current_mcap)
                current_24h = info['market_data']['high_24h']['usd']
                current_24h = "${:,.2f}".format(current_24h)
                current_24l = info['market_data']['low_24h']['usd']
                current_24l = "${:,.2f}".format(current_24l)
                current_totalsupply = info['market_data']['total_supply']
                current_totalsupply = "{:,.2f}".format(current_totalsupply)
                current_circsupply = info['market_data']['circulating_supply']
                current_circsupply = "{:,.2f}".format(current_circsupply)
                current_maxsupply = info['market_data']['max_supply']
                current_maxsupply = "{:,.2f}".format(current_maxsupply)
                bot.reply_to(message, f"Homepage: {current_homepage}\n\nBlockchain: {current_blockchain}\n\nForum: {current_forum}\n\nSubreddit: {current_subreddit}\n\nGenesis: {current_genesis}\n\nMarket cap rank: {current_mc_rank}\n\nAll time high: {current_ath}\n\nAll time high change: {current_ath_change}%\n\nAll time high date: {current_ath_date}\n\nAll time low: {current_atl}\n\nAll time low change: {current_atl_change}%\n\nAll time low date: {current_atl_date}\n\nPrice: {current_price}\n\n24h High: {current_24h}\n\n24 Low: {current_24l}\n\nMarket cap: {current_mcap}\n\nCirculating supply: {current_circsupply}\n\nTotal supply: {current_totalsupply}\n\nMax supply: {current_maxsupply}")

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
        if coin in coins and language in languages:
            top_headlines = newsapi.get_everything(q=coin, language=language, sort_by='relevancy', page_size=10)
            if top_headlines['totalResults'] > 3  and top_headlines['articles']:
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
                    if i == 2:
                        bot.reply_to(message, text="This function is still in alpha development, currently it only works well with top Market Cap coins.")
                        print("This function is still in alpha development, currently it only works well with top Market Cap coins.")
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
            bot.reply_to(message, text=f'Error, {coin} was not found or language is not supported, if the coin has two words use "-" instead of space and if the language is not supported use /language')
            print(f'Error, {coin} was not found, if the coin has two words use "-" instead of space and if the language is not supported use /language')
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