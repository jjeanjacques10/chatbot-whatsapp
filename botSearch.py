import requests, json, time
import wikipedia
from bot import Bot

class BotSearch(Bot):

    def escreveNaTela(self, response):
        self.caixa_de_mensagem.send_keys('*{}*:{}'.format(self.nome,response))
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()

    def PesquisarWikipedia(self, keyword):
        try:
            wikipedia.set_lang("pt")  # Defina antes
            pesquisa = wikipedia.summary(keyword, sentences=5)
            wikiaprenda = [keyword, str(pesquisa)]
            self.bot.train(wikiaprenda)
        except:
            pesquisa = 'Termo não encontrado, tente outro'
        self.caixa_de_mensagem.send_keys('*{}*:{}'.format(self.nome,pesquisa))
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()

    def PesquisarNoticias(self, keyword):
        try:
            if(keyword == None):
                req = requests.get('https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
                noticias = json.loads(req.text)
            else:
                req = requests.get('https://newsapi.org/v2/top-headlines?q={}&country=br&category=technology&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f'.format(keyword))
                noticias = json.loads(req.text)
            if(noticias["totalResults"] != 0):
                for news in noticias['articles']:
                    titulo = news['title']
                    link = news['url']
                    new = '*'+ self.nome +'*: ' + titulo + ' ' + link + '\n'

                    self.caixa_de_mensagem.send_keys(new)
                    time.sleep(1)
            else:
                self.escreveNaTela("*{}*: Não encontrei nada, tem certeza que o termo tem relação com tecnologia?".format(self.nome))
        except:
            pesquisa = "Termo {} não encontrado, tente outro".format(keyword)
            self.caixa_de_mensagem.send_keys('*' + self.nome + '*:' + pesquisa)
            self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
            self.botao_enviar.click()

    def PesquisaClima(self):
        try:
            weather = requests.get('http://apiadvisor.climatempo.com.br/api/v1/weather/locale/3477/current?token=42e95b3445df96d67215946ab6ce301c')
            json_weather1 = weather.json()
            weatherText = "\n======Clima em {}/{} ======\n".format(json_weather1["name"], json_weather1["state"])
            weatherText += "*Condição* = {}\n".format(json_weather1["data"]["condition"])
            weatherText += "*Temperature* = {}ºC\n".format(json_weather1["data"]["temperature"])
            weatherText += "*Umidade* = {}%\n".format(json_weather1["data"]["humidity"])
            weatherText += "*Espero ter ajudado*"
        except:
            weatherText = 'Houve um problema, tente mais tarde'
        self.escreveNaTela(weatherText)

    def PesquisaYoutube(self, keyword):
        try:
            if (keyword == None):
                videos = "Insira um termo para pesquisa"
            else:
                videos = requests.get(
                    'https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&q={}&type=video&order=relevance&chart=mostPopular&locale=br&maxResults=5&regionCode=br&key={}'.format(
                        keyword,self.config['KEY']['youtube']))
                json_videos = videos.json()
                videos = "*Vídeos*\n"
                for i in range(len(json_videos["items"])):
                    try:
                        nome = json_videos["items"][i]["snippet"]["title"]
                        link = json_videos["items"][i]["id"]["videoId"]
                        videos += "{} - https://www.youtube.com/watch?v={}\n".format(nome, link)
                    except:
                        videos += "{}\n".format(nome)
                self.caixa_de_mensagem.send_keys(videos)
                time.sleep(1)
        except:
            videos = 'Houve um problema, tente mais tarde'
            self.escreveNaTela(videos)

