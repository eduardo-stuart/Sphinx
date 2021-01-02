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

from rpyc import Service
from rpyc.utils.server import ThreadedServer
from Sphinx import Sphinx

class SphinxServer(Service):
    sphynx = Sphinx()
    MAX_TENTATIVAS = 10
    tentativa_atual = 0
    fim_jogo = False

    def __init__(self):
        # Sempre que um objeto for criado, vamos iniciar um jogo
        self.exposed_novo_jogo()

    def exposed_novo_jogo(self):
        print('Cliente solicitou: um novo jogo')
        self.sphynx.novo_jogo()
        self.tentativa_atual = 0

    def exposed_get_descricao(self):
        print('Cliente solicitou: descricao do jogo')
        return self.sphynx.get_descricao()

    def exposed_quantas_tentativas_restam(self):
        print('Cliente solicitou: quantas tentativas restam')
        return self.MAX_TENTATIVAS - self.tentativa_atual

    def exposed_get_total_letras(self):
        print('Cliente solicitou: total de letras da frase')
        return self.sphynx.get_total_letras()

    def exposed_get_total_letras_descobertas(self):
        print('Cliente solicitou: total de letras descobertas')
        return self.sphynx.get_total_letras_descobertas()

    def exposed_get_letras_descobertas(self):
        print('Cliente solicitou: letras que já foram descobertas')
        return self.sphynx.get_letras_descobertas()

    def exposed_get_total_letras_nao_descobertas(self):
        print('Cliente solicitou: quantas letras ainda não foram descobertas')
        return self.sphynx.get_total_letras_nao_descobertas()

    def exposed_get_letras_nao_descobertas(self):
        print('Cliente solicitou: conjunto de letras ainda não descobertas')
        return self.sphynx.get_letras_nao_descobertas()

    def exposed_get_conjunto_de_letras_da_frase(self):
        print('Cliente solicitou: conjunto de letras que formam uma frase')
        return self.sphynx.letras_da_frase

    def exposed_get_total_palpites(self):
        print('Cliente solicitou: quantidade de palpites já feitos')
        return self.sphynx.get_total_palpites()

    def exposed_get_frase_ate_momento(self):
        print('Cliente solicitou: como está a frase até o momento')
        return u'\xa0'.join(self.sphynx.get_frase_ate_momento())

    def exposed_get_jogo_encerrado(self):
        print('Cliente solicitou: jogo encerrado?')
        return self.sphynx.jogo_encerrado()

    def exposed_palpite(self, letra):
        print(f'Cliente solicitou: dar um palpite com a letra {letra}')
        return self.sphynx.palpite(letra)

    def exposed_get_frase_display(self):
        print('Cliente solicitou: a frase final, como deverá ser exibida ao usuário')
        return self.sphynx.frase_escolhida_display



if __name__=='__main__':
    print("""
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
        """)
    PORT = 18871
    sphynx_server = SphinxServer()
    try:
        server = ThreadedServer(sphynx_server, port=PORT)
    except:
        print(f'Erro ao tentar iniciar o servidor. Já existe uma instância usando a porta {PORT}?')
    else:
        print('Seja bem-vindo ao jogo Sphynx')
        print('O servidor está em operação')
        print(f'Para se conectar, o cliente deverá usar a porta {server.port}')
        server.start()

