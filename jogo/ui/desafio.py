import pygame
from jogo.ui.interface import texto


class Desafio:
    def __init__(self, titulo, pergunta, opcoes, correta, explicacao, ao_acertar):
        self.titulo = titulo
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.correta = correta
        self.explicacao = explicacao
        self.ao_acertar = ao_acertar
        self.ativo = True
        self.concluido = False
        self.feedback = 'Sem penalidade: experimente e aprenda.'

    def processar(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_RETURN:
            self.ativo = False
        elif not self.concluido and pygame.K_1 <= evento.key <= pygame.K_4:
            escolha = evento.key - pygame.K_1
            if escolha == self.correta:
                self.concluido = True
                self.feedback = self.explicacao
                self.ao_acertar()
            else:
                self.feedback = 'Ainda não. ' + self.explicacao + ' Tente outra vez.'

    def desenhar(self, tela):
        pygame.draw.rect(tela, (20, 31, 49), (45, 110, 710, 420), border_radius=18)
        texto(tela, self.titulo, 70, 130, 28)
        texto(tela, self.pergunta, 70, 180, 21, largura=650)
        for i, opcao in enumerate(self.opcoes):
            texto(tela, f'{i + 1}. {opcao}', 80, 245 + i * 38, 21)
        texto(tela, self.feedback, 70, 410, 18, (245, 207, 120), 650)
        texto(tela, '1–4: responder • ENTER: voltar à exploração', 70, 490, 18)
