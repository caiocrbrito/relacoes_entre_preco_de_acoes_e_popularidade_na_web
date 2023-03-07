import pandas as pd
import snscrape.modules.twitter as sntwitter
from pytrends.request import TrendReq
from pyyoutube import Api
from chaves import chave_api


class ScrapingDados:

    def __init__(self, ativo, inicio=None, final=None):
        
        self.ativo = ativo
        self.inicio = inicio
        self.final = final

    def twitter(self):
        
        tweets = []

        query = f'#{self.ativo} until:{self.final} since:{self.inicio}'

        for tweet in sntwitter.TwitterSearchScraper(query).get_items():

            tweets.append([tweet.date, 
                            tweet.user.username, 
                            tweet.user.displayname, 
                            tweet.user.verified,                  
                            tweet.replyCount,
                            tweet.retweetCount,
                            tweet.likeCount, 
                            tweet.lang,
                            tweet.content,
                            self.ativo])

        df = pd.DataFrame(tweets, 
                        columns=['data',
                                'usuario',
                                'nome_usuario',
                                'verificado',
                                'replicado',
                                'retweets',
                                'curtidas',
                                'lingua',
                                'conteudo',
                                'conteudo_renderizado',
                                'ativo'])
        return df

    def trends(self):

        pytrends = TrendReq(hl='pt-BR', 
                            tz=360)

        pytrends.build_payload([self.ativo], 
                                cat=0, 
                                timeframe=f'{self.inicio} {self.final}')

        data = pytrends.interest_over_time() 
        data = data.reset_index()
        data.columns = ['date', 'qtd', 'ticker']
    
        return data
    
    def youtube(self):
        
        api = Api(api_key=chave_api)

        r = api.search_by_keywords(q=self.ativo, 
                           search_type=["channel",
                                        "video", 
                                        "playlist"], 
                           count=50000,
                           published_after=f"{self.inicio}T00:00:00Z",
                           published_before=f"{self.final}T23:59:59Z")
        dict_yt = r.to_dict()

        lista_yt = []
      
        for i in range(len(dict_yt['items'])):
            
            lista_yt.append([dict_yt['items'][i]['snippet']['publishedAt'],
                            dict_yt['items'][i]['snippet']['channelId'],
                            dict_yt['items'][i]['snippet']['title'],
                            dict_yt['items'][i]['snippet']['description'],
                            dict_yt['items'][i]['snippet']['channelTitle'],
                            dict_yt['items'][i]['id']['videoId'],
                            self.ativo])

        df_yt = pd.DataFrame(lista_yt, 
                     columns=['data_publicacao',
                              'canal_id',
                              'titulo',
                              'descricao',
                              'titulo_canal',
                              'video_id',
                              'ativo'])
        return df_yt
        


# df = ScrapingDados(ativo='LUNC', inicio='2022-10-10', final='2022-10-11')
# print(df.twitter())
print('Hello')
# trends = ScrapingDados(ativo='LUNC', inicio='2022-10-10', final='2022-10-11')
# print(trends.trends())
df = ScrapingDados(ativo='LUNC', inicio='2022-10-10', final='2022-10-11')
print(df.youtube())
