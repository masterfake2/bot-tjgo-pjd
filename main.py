from selenium import webdriver
import logging
import os
import sys
import load 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

class Configuracoes:
    logging.basicConfig(filename="application.log", level=logging.INFO)
    config = load.configuracoes().carregarDados()

class Navegador(Configuracoes):
    # * -------------------------------------------------------
    linux_path = '/home/jamal/Downloads/geckodriver-v0.29.0-linux64/geckodriver' # * Caminho para usar no Linux (Ubuntu)
    windows_path = os.path.abspath("./lib/") # * Caminho para usar no windows
    # * -------------------------------------------------------
    def __init__(self) -> None:
        # ? Inicia a aplicação 
        logging.info('[DEBUG] Iniciando a aplicação')
        # ? Verifica o sistema em que o script está rodando 
        sistema = sys.platform
        if 'linux' in sistema:
            self.path = self.linux_path
        elif 'windows' in sistema:
            self.path = self.windows_path
        else:
            exit(1)
        logging.info(f'[DEBUG] s.o -> {sistema}') # * Gera log com o sistema encontrado 
        logging.info(f'[DEBUG] caminho encontrado -> {self.path}')

    def criarBrowser(self) -> None:
        # ? Retorna um inteiro representando sucesso na instanciação do browser 
        try:
            # ? Tenta criar chamar os métodos responsáveis pela criação do browser
            # ! Uso obrigatório do firefox (facilidade de outros sistemas operacionais)
            self.firefox = webdriver.Firefox(executable_path=self.path)
            return self.firefox # * Sucesso
        except Exception as e:
            self.firefox.quit()
            logging.critical(f'[ERRO NO PROCESSO DE CRIAÇÃO DO BROWSER] {e} ')
            return -1 # ! Erro 

class Tribunal(Configuracoes):
    tribunal = "TJGO"
    tribunal_url = "https://pjd.tjgo.jus.br/"

    def __init__(self, nav) -> None:
        self.nav = nav

    def entrarTribubal(self):
        self.nav.get(self.tribunal_url)

    def preencheDados(self):
        # TODO: loginbox & Senha
        self.nav.find_element_by_id("loginbox").send_keys(Configuracoes.config.credenciais()["usuario"])
        self.nav.find_element_by_id("Senha").send_keys("teste")
        self.nav.find_element_by_id("teclashiftN").click()

        #*driver = webdriver.Firefox(executable_path='/home/jamal/Downloads/geckodriver-v0.29.0-linux64/geckodriver', service_log_path=os.devnull)
        #*driver.get("http://www.python.org")
                
class GoogleSheet(Configuracoes):
    def __init__(self) -> None:
        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage(os.path.abspath("./lib/") + '/credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', scopes)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

# * msg = Navegador()
# * nav = msg.criarBrowser()

# * tj = Tribunal(nav)
# * tj.entrarTribubal()
# * tj.preencheDados()

teste = GoogleSheet()