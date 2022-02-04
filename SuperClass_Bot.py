import json
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


"""
Essa classe contém todas as funções de entrada e saida do bot. 
"""


class Bot:
    """ ATRIBUTOS:
    Str: attr user: usuario windows.
    Str: attr log: mensagem de saida do programa.
    WebDriverObject: attr driver: driver controlador do chrome.
    Dict: attr parametros: dicionario com as configuracoes e informacoes importantes do sistema.
    Str: attr link: link do site retirado da planilha.
    """
    def __init__(self):
        """ CONSTRUTOR.
        """
        self.user = Path.home().name
        self.driver = None
        self.parametros = {}
        self.log = ''
        self.link = 'https://www.santander.com.br/'  # TODO: BOTE O LINK DO SITE AQUI

    def set_up(self):
        """ CONFIGURA O DRIVER.
        """
        caps = DesiredCapabilities().CHROME
        caps['pageLoadStrategy'] = 'normal'
        # caps['pageLoadStrategy'] = 'eager'

        chrome_options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')

        self.driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)

        self.driver.get(self.link)

    def clean_up(self):
        """ ENCERA O DRIVER.
        """
        self.driver.close()

    def set_up_ambiente(self):
        """ PADRONIZA O AMBIENTE DE TRABALHO DOS BOTS NOS DIRETORIOS DO COMPUTADOR (PASTA DOWNLOADS).
        APENAS NECESSARIO CASO HAJA DOWNLOAD DE ARQUIVOS.
        """
        # lista os arquivos da pasta downloads
        caminho_downloads = Path(rf'C:\Users\{self.user}\Downloads')
        if caminho_downloads / Path('temp') in caminho_downloads.iterdir() or \
                caminho_downloads / Path('downloads') in caminho_downloads.iterdir():
            self.log = f'Apague ou mova qualquer pasta chamada temp ou downloads da sua pasta downloads.'
            return

        # cria as pastas temp e certidoes
        arquivos = list(caminho_downloads.iterdir())
        (caminho_downloads / Path('temp')).mkdir()
        (caminho_downloads / Path('downloads')).mkdir()

        # move todos os arquivos para a pasta temp
        for arquivo in arquivos:
            shutil.move(arquivo, arquivo.parent / Path('temp') / arquivo.name)

    def clean_up_ambiente(self):
        """ DESPADRONIZA O AMBIENTE DE TRABALHO DOS BOTS NOS DIRETORIOS DO COMPUTADOR (PASTA DOWNLOADS).
        APENAS NECESSARIO CASO HAJA DOWNLOAD DE ARQUIVOS.
        """
        # esvaziar pasta temp
        for arquivo in Path(fr'C:\Users\{self.user}\Downloads\temp').iterdir():
            shutil.move(arquivo, arquivo.parent.parent / arquivo.name)

        # apagar pasta temp
        Path(fr'C:\Users\{self.user}\Downloads\temp').rmdir()
