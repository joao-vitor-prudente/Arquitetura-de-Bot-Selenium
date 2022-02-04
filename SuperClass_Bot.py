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

        self.driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)

        self.driver.get(self.link)

    def clean_up(self):
        """ ENCERA O DRIVER.
        """
        self.driver.close()
