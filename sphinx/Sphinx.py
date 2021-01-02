"""
########################################################################
###########################   Sphinx  ##################################
########################################################################
## Trabalho para a disciplina Sistemas Distribuídos                   ##
## Professor: Fábio Contarini Carneiro                                ##
## Aluno: Eduardo Stuart Napier Moura (eduardostuart.ti@gmail.com)    ##
## Matrícula: 20161101936                                             ##
## Universidade Veiga de Almeida - Período: 2018.2                    ##
########################################################################
########################################################################
"""

import random
import unicodedata

ARQUIVO_PROVERBIOS = 'proverbios.txt'


class Sphinx:

    lista_proverbios = None
    descricao = 'Tente acertar a frase!'
    frase_escolhida_display = None  # Frase para ser exibida na tela, com acentos gráficos e etc
    frase_escolhida = None  # Usada pelo mecanismo do jogo, com letras em maiúsculas e dispensando acentos gráficos
    frase_ate_momento = []  # Armazena o estado da frase até então (ou seja, quais letras já ou não foram encontradas)
    letras_da_frase = set()  # Conjunto com as letras que compõem a frase
    letras_descobertas = set()
    letras_nao_descobertas = set()
    letras_palpites = set()

    def novo_jogo(self):
        if not self.lista_proverbios:
            self.lista_proverbios = open(ARQUIVO_PROVERBIOS,
                                         encoding='UTF-8',
                                         mode='r').readlines()
            if self.lista_proverbios[0][0] == '#':
                self.descricao = self.lista_proverbios[0][1:]
                self.lista_proverbios.pop(0)
        self.frase_escolhida_display = random.choice(self.lista_proverbios).strip()
        # Vamos remover todos os caracteres que não forem letras/números e também os acentos gráficos
        self.frase_escolhida = self.__remover_acentos(self.frase_escolhida_display).upper()
        frase_tmp = ''.join(ch for ch in self.frase_escolhida if ch.isalpha())
        # Quais as letras que integram a frase?
        self.letras_da_frase = set() # Caso já tenha sido escolhida uma frase, vamos zerá-la
        for letra in frase_tmp:
            self.letras_da_frase.add(letra)
        # Zerando os status do jogo
        self.letras_descobertas = set()
        self.letras_nao_descobertas = self.letras_da_frase.copy()
        self.letras_palpites = set()
        self.frase_ate_momento = ['_' if ch != ' ' else ' ' for ch in self.frase_escolhida]

    def __init__(self):
        self.novo_jogo()

    # Getters
    def get_total_letras(self):
        return len(self.letras_da_frase)

    def get_total_letras_descobertas(self):
        return len(self.letras_descobertas)

    def get_letras_descobertas(self):
        return self.letras_descobertas

    def get_total_letras_nao_descobertas(self):
        return len(self.letras_nao_descobertas)

    def get_letras_nao_descobertas(self):
        return self.letras_nao_descobertas

    def get_conjunto_letras(self):
        return self.letras_da_frase

    def get_total_palpites(self):
        return len(self.letras_palpites)

    def get_frase_ate_momento(self):
        return self.frase_ate_momento

    def get_descricao(self):
        return self.descricao

    def jogo_encerrado(self):
        return self.get_total_letras_nao_descobertas() == 0

    # Métodos do jogo
    def palpite(self, letra):
        letra = self.__remover_acentos(letra).upper()
        if letra in self.letras_palpites:
            return -1
        self.letras_palpites.add(letra)
        total_acertos = 0
        if letra in self.frase_escolhida:
            total_acertos = self.frase_escolhida.count(letra)
            self.letras_descobertas.add(letra)
            self.letras_nao_descobertas.remove(letra)
            for idx, ch in enumerate(self.frase_escolhida):
                if ch == letra:
                    self.frase_ate_momento[idx] = self.frase_escolhida_display[idx]
        return total_acertos

    def palpite_frase(self, frase):
        # vamos tirar qualquer acento que o usuário pode ter fornecido e colocar todas as letras em maiúsculas
        frase = self.__remover_acentos(frase).upper()
        # O enigma é igual à frase fornecida?
        if frase == self.frase_escolhida.upper():
            # Acertou!
            self.letras_nao_descobertas.clear() # Isso atulizará o getter da propriedade que indica se o jogo terminou
            return self.frase_escolhida_display
        else:
            # Ainda não encontrou... Retorne -1
            return -1




    # Métodos de apoio
    def __remover_acentos(self, frase):
        return ''.join(ch for ch in unicodedata.normalize('NFD', frase)
                       if unicodedata.category(ch) != 'Mn')

if __name__=='__main__':
    # Este código somente será executado se esse arquivo for chamado solo
    # Como efetivamente iremos usá-lo apenas como um módulo, o código a seguir
    # tem como objetivo testar os métodos e se a lógica do jogo está funcionando
    sphynx = Sphinx();
    print(sphynx.get_descricao())
    print('Frase até o momento...')
    print(' '.join(sphynx.frase_ate_momento))
    while True:
        letra = input('Forneca uma letra (use 1 para adivinhar a frase ou 0 para encerrar)\n')
        if letra == '0':
            break
        if letra == '1':
            frase = input('Qual o seu palpite para a frase?\n')
            resultado = sphynx.palpite_frase(frase)
            if resultado == -1:
                print('Errou. Continue tentando...')
                continue
            else:
                print(f'Parabéns! Você acertou a frase!\n{resultado}')
                break
        acertos = sphynx.palpite(letra[0])
        print(f'A letra {letra[0]} apareceu {acertos} vezes. A frase agora está assim:\n')
        res = ' '.join(sphynx.frase_ate_momento)
        print(res)
        print(f'\n')
        if sphynx.jogo_encerrado():
            print('Parabéns! Você acertou a frase!')
            break