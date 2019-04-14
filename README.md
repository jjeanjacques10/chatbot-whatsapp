# Chatbot para WhatsApp

O bot tem como objetivo auxiliar em algumas atividades básicas do cotidiano, ser um assistente pessoal, como por exemplo:

* Mostrar o clima 
* Fazer pesquisas no Wikipédia 
* Trazer as notícias de tecnologia 
* Trazer vídeos do YouTube
* Analizar fotos enviadas

## Para utilizar 

#### Número para conversar com o bot: +55 11 94887-2832
- Para falar com o Bot  /texto
- Para pesquisar notícias de tecnologia /news ou :news termo de tecnologia
- Para pesquisa na wikipédia /wiki texto
- Para o Bot aprender algo /aprenda pergunta?resposta
- Para pesquisar o clima escreva /clima
- Para pesquisar vídeos no youtube /youtube ou /youtube termo pesquisa


## Para programar 

### Você vai precisar de:

* Python 3.x
* Os drivers do selenium se encontram na pasta driver

### Bibliotecas instaladas

* Selenium - https://www.seleniumhq.org/projects/webdriver/
* Chatterbot - https://chatterbot.readthedocs.io/en/stable/
* Wikipedia - https://pypi.org/project/wikipedia/
* Api Video Google - https://developers.google.com/youtube/v3/docs/videos/list?hl=pt-br
* cognitive_face - https://github.com/Microsoft/Cognitive-Face-Python

### As variáveis estão no arquivo Config.json

```sh
{
  "BOT": {
    "nome": "Nome do robô",
    "treino": "Arquivo para treino",
    "path_driver": "driver",
    "usuario": "Nome do usuário com quem quer conversar"
  },
  "KEY":{
    "youtube": "Chave para usar a API do youtube"
  },
  "MICROSOFT": {
    "key": "Chave para usar a API da Microsoft",
    "location": "location da API da Microsoft, consulte a documentação deles"
  }
}
```
Exemplo:
```sh
{
  "BOT": {
    "nome": "Bot",
    "treino": "treinar.txt",
    "path_driver": "driver",
    "usuario": "Jean"
  },
  "KEY":{
    "youtube": "EGeaSyBWTr6gXzZxJUEyva2Rh7IdSmv-jX8IWvw"
  },
  "MICROSOFT": {
    "key": "992ac345681dcb9c818720358e8d6b80",
    "location": "westus"
  }
}
```

#### Artigo no Medium explicando como foi feito: https://medium.com/@jjean.jacques10/assistente-pessoal-para-whatsapp-8c86f6373058
