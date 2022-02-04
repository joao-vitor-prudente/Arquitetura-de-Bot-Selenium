from SuperClass_Bot import Bot
from Class_ModuloDeInteracao import ModuloDeInteracao

"""
Essa classe é seu script principal e será o seu bot em si.
"""


class MainBot(Bot):
    def __init__(self):
        """ CONSTRUTOR.
        """
        super().__init__()
        self.erro = None

    def __enter__(self):
        """ SET UP DO DRIVER E DA PASTA DOWNLOADS QUE SERÁ EXECUTADO QUANDO A CLASSE FOR CHAMADA NUM CONTEXT MANAGER.
        Func: return self.main(): função principal do bot.
        """
        self.set_up()

    def main(self):
        """ SCRIPT PRINCIPAL DE INTERAÇÃO DO BOT COM O SITE.
        """
        ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_1', acao='click', switch_to_window='True')
        ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_2', acao='send_keys', arg='Hello world!', switch_to_window='True')
        ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_3', acao='execute_script', arg='arguments[0].scrollIntoView();', switch_to_window='True')
        # o de cima é apenas um exemplo, o modulo de interacao ja faz a rolagem ate o elemento para todas as ações,
        # portanto esse comando seria trivial.
        texto_do_elemento = ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_4', acao='text', switch_to_window='True')
        print(texto_do_elemento)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ PROCEDIMENTO DE SAIDA QUE SERÁ EXECUTADO QUANDO O CONTEXT MANAGER FOR ENCERRADO OU HOUVER ALGUM ERRO.
        Str: param exc_type: tipo da excessão.
        Str: param exc_value: valor da excessão.
        Str: param exc_traceback: traceback da excessão.
        """
        self.clean_up()

        if exc_type is None:
            self.log = 'Interação executada com sucesso'
        else:
            self.log = f'Houve um erro na execução do programa:'
        print(self.log)


if __name__ == '__main__':
    with MainBot() as mb:
        MainBot.main(mb)
        pass
