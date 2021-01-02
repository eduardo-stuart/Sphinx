from tkinter import messagebox
import tkinter as tk
from tkinter import *
import argparse

import rpyc

##########################################
# Constantes usadas para gerar a interface
PADY = 20
PADX = 20
TAMANHO_BOTAO = 20
TAMANHO_DESCRICAO = 16
TAMANHO_FRASE = 22


###############################################
# Cores usadas para compor a interface
# A peleta vai do tom mais escuro ao mais claro
COR_1 = '#d06969'
COR_2 = '#d08369'
COR_3 = '#d09869'
COR_4 = '#db9e6b'
COR_5 = '#e7a46b'

# CONSTANTES USADAS PARA A LÓGICA DO JOGO
MAXIMO_ERROS = 5

class SphinxGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.frames = {}
        frame = PaginaPrincipal(container, self)
        self.frames[PaginaPrincipal] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        self.exibir_frame(PaginaPrincipal)

    def exibir_frame(self, tela):
        frame = self.frames[tela]
        frame.tkraise()


class PaginaPrincipal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=COR_5)

        # Frase Superior
        frame_superior = Frame(self, height=65, width=680)
        frame_superior.pack()

        bg_img_topo = PhotoImage(file='./bg.png')
        bg_label = Label(frame_superior, image=bg_img_topo)
        bg_label.imagem_usada = bg_img_topo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Servidor que está rodando o jogo
        self.servidor = servidor.root

        # Strings que são usadas na interface
        # Seu conteúdo é fornecido pelo servidor
        self.descricao = StringVar()
        self.frase = StringVar()
        self.feedback = StringVar()
        frame_descricao = tk.Frame(self,
                                   width=550,
                                   bg=COR_3,
                                   bd=1,
                                   relief=tk.SUNKEN)
        frame_descricao.pack(pady=PADY, padx=PADX)

        descricao_label = tk.Label(frame_descricao, textvariable=self.descricao,
                                   font=('', TAMANHO_DESCRICAO), wraplength=450, bg=COR_3)
        descricao_label.pack(pady=5, padx=5)
        tk.Label(self, textvariable=self.feedback, bg=COR_5, font=('', 16)).pack(pady=10, padx=10)
        frase_label = tk.Label(self, textvariable=self.frase,
                               font=('', TAMANHO_FRASE), wraplength=450, bg=COR_5)
        frase_label.pack(pady=PADY, padx=PADX)

        frame_status = tk.Frame(self,
                                bg=COR_3,
                                width=500,
                                height=100,
                                pady=5,
                                padx=5)
        frame_status.pack(pady=5, padx=5)

        # Iremos indicar quantas tentativas já foram feitas e quantas ainda restam
        self.erros = StringVar()
        self.tentativas = StringVar()
        self.vidas = StringVar()

        Label(frame_status, text='Número de Erros: ',
              font=('', 10), bg=COR_3).grid(row=0, column=0)
        Label(frame_status, textvariable=self.erros,
              font=('', 14), bg=COR_3).grid(row=0, column=1)

        Label(frame_status, text='Vidas Restantes: ',
              font=('', 10), bg=COR_3).grid(row=0, column=2)
        Label(frame_status, textvariable=self.vidas,
              font=('', 14), bg=COR_3).grid(row=0, column=3)

        Label(frame_status, text='Número Total de Palpites: ',
              font=('', 10), bg=COR_3).grid(row=0, column=4)
        Label(frame_status, textvariable=self.tentativas,
              font=('', 14), bg=COR_3).grid(row=0, column=5)

        frame_letras = tk.Frame(self,
                                bg=COR_2,
                                width=600,
                                height=150,
                                pady=PADY,
                                padx=PADX,
                                bd=2,
                                relief=tk.GROOVE)
        frame_letras.pack(pady=PADY, padx=PADX)

        # Fileira de botões com as letras correspondentes
        self.botoes = []
        letras = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        col_l, lin_l = 0, 0
        for idx, letra in enumerate(letras):
            if idx == 10:
                col_l, lin_l = 1, 1
            elif idx == 19:
                col_l, lin_l = 2, 2
            else:
                col_l += 1

            btn = tk.Button(frame_letras,
                            text=letra,
                            bg=COR_5,
                            width=3,
                            height=1,
                            font=('', TAMANHO_BOTAO))
            btn.grid(row=lin_l, column=col_l)
            btn.bind('<Button-1>', self.um_palpite)
            self.botoes.append(btn)

        # Frase inferior
        frame_inferior = Frame(self, height=35, width=680)
        frame_inferior.pack()

        bg_img_bot = PhotoImage(file='./bg2.png')
        bg_label_bot = Label(frame_inferior, image=bg_img_bot)
        bg_label_bot.imagem_usada = bg_img_bot
        bg_label_bot.place(x=0, y=0, relwidth=1, relheight=1)

        self.iniciar_novo_jogo()

    def desativar_todos_botoes(self):
        for btn in self.botoes:
            btn.config(state=tk.DISABLED, bg='black')

    def ativar_todos_botoes(self):
        for btn in self.botoes:
            btn.config(state=tk.NORMAL, bg=COR_5)

    def um_palpite(self, event):
        btn = event.widget
        if btn['state'] != tk.DISABLED:
            btn.config(state=tk.DISABLED, bg='black')
            letra = btn['text']
            acertos = self.servidor.palpite(letra)
            # Se não acertou nenhum, vamos diminuir o total de erros permitidos
            if acertos == 0:
                self.total_erros += 1
                self.erros.set(self.total_erros)
                vidas = MAXIMO_ERROS - self.total_erros
                self.vidas.set(vidas)
                if vidas == 0:
                    # Game Over...
                    self.desativar_todos_botoes()
                    self.frase.set(self.servidor.get_frase_display())
                    messagebox.showinfo('Game Over...',
                                        'Que pena, você não acertou a frase...\n\nClique OK para iniciar uma nova partida!')
                    self.iniciar_novo_jogo()
                    return
            self.feedback.set(f'A letra {letra} apareceu {acertos} vezes.')
            if self.servidor.get_jogo_encerrado():
                self.desativar_todos_botoes()
                self.frase.set(self.servidor.get_frase_display())
                messagebox.showinfo('Parabéns!', 'Você venceu!\n\nAperte OK para iniciar uma nova partida!')
                self.iniciar_novo_jogo()
            else:
                tentativas_feitas = self.servidor.get_total_palpites()
                self.frase.set(self.servidor.get_frase_ate_momento())
                self.tentativas.set(tentativas_feitas)

    def iniciar_novo_jogo(self):
        self.servidor.novo_jogo()
        self.descricao.set(self.servidor.get_descricao().strip())
        self.frase.set(self.servidor.get_frase_ate_momento().strip())

        self.total_erros = 0
        self.erros.set(self.total_erros)

        self.tentativas.set(self.servidor.get_total_palpites())
        self.vidas.set(MAXIMO_ERROS - self.total_erros)
        self.ativar_todos_botoes()

        self.feedback.set('')





if __name__=='__main__':

    parser = argparse.ArgumentParser(
        description='Sphinx: Cliente',
        epilog='Use -ip para indicar o IP da máquina destino, e -port para indicar a porta usada pelo servidor'
    )
    parser.add_argument('-port', help='Indica a porta do servidor que iremos usar', default=18871)
    parser.add_argument('-ip', help='Indica o IP do servidor que iremos usar', default='localhost')
    args = vars(parser.parse_args())

    try:
        servidor = rpyc.connect(args['ip'], args['port'])
    except:
        print('Não foi possível se conectar ao servidor. Certifique-se que o mesmo está em execução')
        exit(18871)

    print('Estamos conectados ao servidor.')

    # Vamos gerar a interface gráfica e exibí-la para o usuário
    sphinx = SphinxGUI()

    sphinx.title('Sphinx: O Jogo da Adivinhação')

    # Mensagem de boas-vindas
    messagebox.showinfo('Sphinx - Trabalho de Sistemas Distribuídos',
"""Seja bem-vindo ao Sphinx, um divertido jogo de adivinhação.

As regras são simples:
Você é capaz de acertar a frase que foi escolhida pelo computador?

Tente acertar, escolhendo uma das letras disponíveis.

Sphinx: Trabalho para a Disciplina Sistemas Distribuídos
Professor: Fábio Contarini Carneiro

Aluno: Eduardo Stuart Napier Moura (eduardostuart.ti@gmail.com)
Matrícula: 20161101936

Universidade Veiga de Almeida

2018.2

Pressione OK para iniciar uma partida e boa sorte!""")
    sphinx.mainloop()