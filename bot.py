import time,codecs
from random import randrange
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver
from PIL import Image
from botMicrosoft import BotMicrosoft

class Bot(object):

    def __init__(self, config):
        self.config = config
        self.nome = self.config['BOT']['nome']
        self.bot = ChatBot(self.nome)
        self.bot.set_trainer(ListTrainer)
        # Caminho para onde esta o arquivo do driver para o selenium
        self.chrome = self.config['BOT']['path_driver'] + '\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" + self.config['BOT']['path_driver'] + "\profileGoogle\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        # Instanciando o Bot Microsoft
        self.microsoft = BotMicrosoft()

    def inicia(self,nome_contato):
        #Acessa o Whatsapp e procura os campos na página
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        self.caixa_de_pesquisa = self.driver.find_element_by_class_name('jN-F5')
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print(nome_contato)
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)

    # Começa a conversa
    def saudacao(self,frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    # Pega o texto que o usuário enviou
    def escuta(self):
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto

    # Salva a imagem na pasta imagens para ela ser analizada
    def CapturarImagem(self):
        post = self.driver.find_elements_by_class_name('_3v3PK')
        ultimo = len(post) - 1
        self.escreveNaTela("Analisando imagem...")
        idImagem = randrange(9999)
        for element in post[ultimo].find_elements_by_tag_name('img'):
            print("Tetando pegar o SRC")
            try:
                nomeImagem = "screenshot{}".format(idImagem)
                element.screenshot("imagens/{}.png".format(nomeImagem))
                im = Image.open("imagens/{}.png".format(nomeImagem))
                rgb_im = im.convert('RGB')
                rgb_im.save('imagens/convertidas/{}.jpg'.format(nomeImagem))
                self.escreveNaTela("Análise concluida")
                #Chama a função para indentificar as caracteristicas no rosto
                for response in self.microsoft.indentificarFaceImagem('imagens\\convertidas\\{}.jpg'.format(nomeImagem), self.config['MICROSOFT']['key'], self.config['MICROSOFT']['location']):
                    self.escreveNaTela(response)
            except:
                self.escreveNaTela("Não foi possível análisar a imagem, tente novamente mais tarde")

    # Para ensinar o bot uma nova frase
    def aprenderConversa(self, texto):
        if texto.find('?') != -1:
            ultimo_texto = texto
            texto = texto.replace(':', '')
            texto = texto.lower()
            texto = texto.replace('?', '?*')
            texto = texto.split('*')
            novo = []
            for elemento in texto:
                elemento = elemento.strip()
                novo.append(elemento.replace('?', ''))
            with codecs.open('treino/treinar.txt', 'a', 'utf-8') as arq:
                arq.write('\n')
                arq.write(novo[0])
                arq.write('\n')
                arq.write(novo[1])
                arq.close()
            self.bot.train(novo)
            self.caixa_de_mensagem.send_keys('*{}*: Aprendi = {}'.format(self.nome,texto))
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
            self.botao_enviar.click()
        else:
            self.caixa_de_mensagem.send_keys("*{}*: '{}' não está no formato certo pergunta?resposta".format(self.nome,texto))
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
            self.botao_enviar.click()
        return ultimo_texto

    # Utilizando a biblioteca chatterbot ele trás uma resposta para o usuário
    def responde(self,texto):
        response = self.bot.get_response(texto)
        if float(response.confidence) > 0.5:
            response = str(response)
        else:
            response = "Não entendi, me ensine: '{}'".format(texto)
        self.escreveNaTela(response)

    # Ensina o bot com o arquivo de treino
    def treina(self,nome_arquivo):
        treino = codecs.open('treino/'+nome_arquivo, "r", encoding="utf-8")
        conversas = []
        print("Treinou")
        for fala in treino:
            conversas.append(fala)
        print(conversas)
        self.bot.train(conversas)

    # Envia uma mensagem para o usuário
    def escreveNaTela(self, response):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
        self.caixa_de_mensagem.send_keys('*{}*: {}'.format(self.nome,response))
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()
