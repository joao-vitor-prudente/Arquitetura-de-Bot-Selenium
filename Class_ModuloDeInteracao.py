import pandas as pd
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import openpyxl


"""
Essa classe contém todo o modulo que vai auxiliar a interação com elementos web. 
"""


class ModuloDeInteracao:
    """ ATRIBUTOS:
    WebDriverObject: attr driver: driver controlador do chrome.
    Dict: attr xpaths: dicionario relacionando xpath de cada elemento e sua etiqueta.
    Dict: attr frames: dicionario relacionando xpath de cada frame e suaetiqueta.
    Str: attr endereco: etiqueta do elemento.
    Str: attr acao: acao a ser executada (click, send_keys, execute_script).
    Str: attr arg: argumento passado na acao.
    Bool: attr switch_to_window: define se é ou nao necessario mudar de janela.
    Int: attr time_out: tempo ate que a funcao resulte numa excessao.
    Bool: attr endereco_com_indice: define se existe um indice_endereco no xpath, marcado por {i}, ou nao
    Int: attr indice_endereco: numero do indice_endereco.
    """
    def __init__(
            self, driver, endereco_elemento: str, acao: str, arg: str = '', switch_to_window: bool = False,
            time_out: int = 20, endereco_com_indice: bool = False, indice_endereco: int = 0
    ):
        """ CONSTRUTOR
        WebDriverObject: param driver: driver controlador do chrome.
        Str: param endereco_elemento: etiqueta do elemento.
        Str: param acao: acao a ser executada (click, send_keys, execute_script, text).
        Str: param arg: argumento passado na acao.
        Bool: param switch_to_window: define se é ou nao necessario mudar de janela.
        Int: param time_out: tempo ate que a funcao resulte numa excessao.
        Bool: param endereco_com_indice: define se existe um indice_endereco no xpath, marcado por {i}, ou nao
        Int: param indice_endereco: numero do indice_endereco.
        """
        self.driver = driver
        self.xpaths = {}
        self.frames = {}
        self.endereco = endereco_elemento
        self.acao = acao
        self.arg = arg
        self.switch_to_window = switch_to_window
        self.time_out = time_out
        self.endereco_com_indice = endereco_com_indice
        self.indice_endereco = indice_endereco
        self.text = ''

        # framework
        self.ler_xpaths()
        self.procurar_elemento()
        self.executar_interacao()

    def ler_xpaths(self):
        """ LE A PLANILHA DE PARAMETROS E GERA UM DICIONARIO COM OS PARAMETROS E COM OS XPATHS
        """
        # le a planilha
        planilha_xpaths = pd.read_excel('Relacao Xpaths.xlsx', sheet_name='Relacao Xpaths')

        # transforma os dataframes em dicionarios
        self.xpaths = dict(zip(list(planilha_xpaths['LABEL']), list(planilha_xpaths['XPATH'])))

        # cria uma uma matriz onde cada linha sao os dados de uma coluna de frames
        lista_frames = [list(planilha_xpaths[coluna]) for coluna in planilha_xpaths.keys()
                        if coluna != 'LABEL' and coluna != 'XPATH']

        # rotaciona essa matriz para que cada linha seja os dados de uma linha de frames
        lista_frames = list(zip(*lista_frames))
        lista_frames = [list(i) for i in lista_frames]

        self.frames = dict(zip(list(planilha_xpaths['LABEL']), lista_frames))
        for key, value in self.frames.items():
            while '.' in value:
                self.frames[key].remove('.')

    def procurar_elemento(self):
        """ ACESSA OS FRAMES NECESSARIOS E REALIZA AS CHECAGENS NECESSARIAS.
        """
        # acessar os frames necessarios
        self.driver.switch_to.default_content()
        for frame in self.frames[self.endereco]:
            WebDriverWait(self.driver, self.time_out).until(EC.presence_of_element_located((By.XPATH, frame)))
            self.driver.execute_script('arguments[0].scrollIntoView();', self.driver.find_element(By.XPATH, frame))
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, frame))

        # endereco com indice - funcionalidade para escolher o elemento dinamicamente necessario para escolher lote e comprovante
        if self.endereco_com_indice:
            self.endereco = self.xpaths[self.endereco].replace('{i}', str(self.indice_endereco))
        else:
            self.endereco = self.xpaths[self.endereco]

        WebDriverWait(self.driver, self.time_out).until(EC.presence_of_element_located((By.XPATH, self.endereco)))

    def executar_interacao(self):
        """ EXECUTA A ACAO REQUISITADA.
        """
        elemento = self.driver.find_element(By.XPATH, self.endereco)
        if self.acao == 'click':
            try:
                WebDriverWait(self.driver, self.time_out).until(EC.element_to_be_clickable)
                elemento.click()
            except ElementNotInteractableException:
                self.driver.execute_script('arguments[0].click();', elemento)
        elif self.acao == 'send_keys':
            elemento.send_keys(self.arg)
        elif self.acao == 'execute_script':
            self.driver.execute_script(self.arg, elemento)
        elif self.acao == 'text':
            self.text = elemento.text
