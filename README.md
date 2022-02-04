# 1. INTRODUÇÃO
Este é um modelo de bot para automação web utilizando selenium com foco em resiliência a mudanças no site que está sendo automatizado, legibilidade e segurança.<br />
# 2. ARQUIVOS
O projeto é composto por quatro arquivos:<br />
SuperClass_Bot.py: contém a classe com as funções de inicialização e fechamento do driver controlador do navegador.<br />
Class_ModuloDeInteração.py: contém o modulo que modifica o selenium.<br />
Class_MainBot.py: contém o modelo da estrutura do seu bot.<br />
RelacaoXpaths.xlsx: é uma planilha contendo o nome dado a cada elemento com que o bot interagirá, os seus respectivos xpaths e o caminho de iframes que leva a ele desde o conteudo
principal da pagina.<br />
# 3. BOT
Contém 3 metodos:
__init__: é o construtor da classe.<br />
set_up: contém as configurações de inicialização do driver, bem como o tipo do driver (o padrão é o chrome) e o link do site no momento inicial.
clean_up: encerra o driver
# 4. MODULO DE INTERAÇÃO
O arquivo Class_ModuloDeInteracao.py contem uma unica classe ModuloDeInteracao, a qual pode apenas ser chamada.<br />
## 4.1. Parâmetros
WebDriverObject: param driver: driver controlador do chrome.<br />
Str: param endereco_elemento: etiqueta do elemento.<br />
Str: param acao: acao a ser executada (click, send_keys, execute_script, text).<br />
Observação 1: a ação text gera um retorno.<br />
Observação 2: a ação execute_script nesse modulo só suporta um argumento.<br />
Str: param arg: argumento passado na acao send_keys e execute_script.<br />
Bool: param switch_to_window: define se é ou nao necessario mudar de janela.<br />
Int: param time_out: tempo ate que a funcao resulte numa excessao do tipo TimeoutException.<br />
Bool: param endereco_com_indice: define se existe um indice_endereco no xpath, marcado por {i}, ou nao.<br />
Int: param indice_endereco: numero do indice_endereco.<br />
## 4.2. Endereços com Indices
Quando se quer fazer um loop interagindo com todos os endereços xpath que diferem em algum índice na sua estrutura, escreve-se o primeiro elemento da lista na planilha e troca-se
o numero que será o indice por um {i}.<br />
Exemplo:<br />
Tem-se os elementos div/spam[1]/a, div/spam[2]/a, div/spam[3]/a...<br />
Escreve-se na planilha div/spam[{i}]/a e usa-se o codigo, por exemplo:<br />
```python
while True:
  ModuloDeInteracao(driver=driver, endereco_elemento=endereco, acao=acao, endereco_com_indice=True, indice_endereco=1)
```
## 4.3. Funcionalidade
Para cada ação, o modulo:
1. Percorre todo o caminho de iframes ate chegar no que contém o elemento.
2. Espera até que o elemento esteja presente.
3. Rola até que o elemento esteja visível na página.
No caso da ação click, ele também espera o elemento ser clicavel e, em caso de erro, tenta clicar ele executando o javascript.
Exemplos:
```python
ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_1', acao='click', switch_to_window='True')
ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_2', acao='send_keys', arg='Hello world!', switch_to_window='True')
ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_3', acao='execute_script', arg='arguments[0].scrollIntoView();', switch_to_window='True')
texto_do_elemento = ModuloDeInteracao(driver=self.driver, endereco_elemento='endereco_elemento_4', acao='text', switch_to_window='True')
```
# 5. RELAÇÃO XPATHS
Essa é uma planilha com uma aba de mesmo nome.<br />
A primeira coluna (LABEL) é uma etiqueta arbitrária para ser referenciada no parâmetro endereco_elemento.<br />
A segunda coluna (XPATH) é o endereco xpath relativo àquela etiqueta.<br />
Da terceira coluna em diante (FRAMES) cada coluna da esquerda para a direita é dado o xpath do iframe mais externo ate o frame que contem o elemento.<br />
Observação: Podem existir quantas colunas chamadas FRAMES forem necessarias, basta escrever FRAMES na primeira linha da coluna depois da última.<br />
Observação: Cada celula vazia numa coluna chamada FRAMES deve ser preenchida com um ponto.<br />
# 6. MAIN BOT
Essa é a classe em que se desenvolverá o bot em si.<br />
Ela inicialmente possui 4 métodos:<br />
__init__: é o construtor da classe, nele se pode editar os parâmetros que serão passados nela e seus atributos.<br />
__enter__, __exit__: a classe é chamada em uma estrutura de contexto (with), então a primeira contém os metodos que serão chamados na inicialização do bot e a segunda contem os
metodos que serão chamados no encerramento dele.<br />
main: contém a rotina de interações que será executada pelo bot.<br />
# 7. DEPENDENCIAS
## 7.1. Selenium
Instalação:<br />
No terminal: pip install selenium<br />
Instalar chrome driver ou outro drver a sua escolha:<br />
Link chrome driver: (https://chromedriver.chromium.org/downloads).<br />
extrair chromedriver na pasta C:\Windows.<br />
## 7.2. Pandas
No terminal: pip install pandas
