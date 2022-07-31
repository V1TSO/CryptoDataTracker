from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='5753feb0897a4ff5a322ccd4289acede')

top_headlines = newsapi.get_everything(q=coin, language=language, sort_by='popularity', page_size=10)

for i in range(0,5):
    print()
    print(f"Title: {top_headlines['articles'][i]['title']}")
    print(f"Description: {top_headlines['articles'][i]['description']}")
    print(f"URL: {top_headlines['articles'][i]['url']}")
    print(f"Published in: {top_headlines['articles'][i]['publishedAt'][:10]}")
    print()