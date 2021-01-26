import configparser
import os 

class configuracoes:
    def carregarDados(self):
        self.diretorio = os.path.abspath("./lib/config.ini") #Diretório de configurações default - Credenciais
        self.config = configparser.ConfigParser()
        self.config.read(self.diretorio)
        return self.config

    def credenciais(self, config):
        return config["credenciais"]

        

#teste = configuracoes()
#credenciais = teste.carregarDados()
#print(teste.credenciais(credenciais)["senha"])