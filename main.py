import re, json
from botSearch import BotSearch

while True:
    # Buscando arquivos de configuração
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Instanciando o bot
    bot = BotSearch(config)
    # Passando o arquivo para treino
    bot.treina(config['BOT']['treino'])
    # Selecionando a pessoa que ele vai pesquisar no WhatsApp
    bot.inicia(config['BOT']['usuario'])
    # Dizendo o primeiro 'Oi'
    bot.saudacao(
        ['*{}*: Oi, sou o {}! Estou disponível para ajuda-los'.format(config['BOT']['nome'], config['BOT']['nome']),
         'Para falar com o {}  */texto*'.format(config['BOT']['nome']),
         'Para pesquisar notícias de tecnologia */news* ou *:news termo de tecnologia*',
         'Para pesquisa na wikipédia */wiki texto*',
         'Para o {} aprender algo */aprenda pergunta?resposta*'.format(config['BOT']['nome']),
         'Para pesquisar o clima escreva */clima*',
         'Para pesquisar vídeos no youtube */youtube* ou */youtube termo pesquisa*'])
    # bot.saudacao(['*{}*: Oi, sou o SIBot! Estou disponível para ajuda-los'.format(nomebot)])
    ultimo_texto = ''

    try:

        while True:
            #Iniciando o processo de captar mensagens do whatsaap
            try:
                # Capturando textos digitados
                texto = bot.escuta()
            except:
                # Capturando imagens para análise
                bot.CapturarImagem()

            if texto != ultimo_texto and re.match(r'^/', texto):
                ultimo_texto = texto
                texto = texto.replace('/', '')
                texto = texto.lower()

                if (re.match(r'^ aprenda', texto) or  re.match(r'^aprenda', texto)):
                    texto = texto.replace('aprenda', '')
                    ultimo_texto = bot.aprenderConversa(texto)
                elif (texto == 'news' or texto == ' news' or re.match(r'^news', texto) or  re.match(r'^ news', texto)):
                    if(texto == 'news'):
                        bot.PesquisarNoticias(None)
                    else:
                        texto = texto.replace('news', '')
                        bot.PesquisarNoticias(texto)
                elif (re.match(r'^ wiki', texto) or re.match(r'^wiki', texto)):
                    keyword = texto.replace('wiki', '')
                    bot.PesquisarWikipedia(keyword)
                elif(texto == "clima" or re.match(r'^ clima', texto) or re.match(r'^clima', texto)):
                    bot.PesquisaClima()
                elif (texto == "youtube" or re.match(r'^ youtube', texto) or re.match(r'^youtube', texto)):
                    keyword = texto.replace('youtube', '')
                    bot.PesquisaYoutube(keyword)
                else:
                    bot.responde(texto)
    except:
        # Caso ocorra um problema o programa será reiniciado
        print("O programa será reiniciado")
        bot.driver.close()
        bot.driver.quit()
