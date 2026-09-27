import pygame
from jogo.settings import ALTURA
from jogo.ui.botoes_tela_inicial import Botao
from jogo.ui.interface import texto


class TelaInicial:
    """Menu desenhado com formas e fontes, sem imagens externas."""
    def __init__(self, game):
        self.game = game
        self.ajuda = False
        self.botoes = [Botao(t, 70, 300 + i * 72, 280, 55)
                       for i, t in enumerate(('Jogar', 'Como jogar', 'Sair'))]

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.game.nova_partida()
                return
            for i, botao in enumerate(self.botoes):
                if botao.clicado(evento):
                    if i == 0:
                        self.game.nova_partida()
                    elif i == 1:
                        self.ajuda = not self.ajuda
                    else:
                        self.game.sair()
                    return

    def atualizar(self):
        for botao in self.botoes:
            botao.verificar_hover(pygame.mouse.get_pos())

    def desenhar(self, tela):
        tela.fill((17, 25, 43))
        for y in range(0, ALTURA, 30):
            pygame.draw.line(tela, (24, 35, 54), (0, y), (800, y))
        pygame.draw.circle(tela, (38, 66, 83), (650, 160), 150, 2)
        pygame.draw.circle(tela, (68, 187, 173), (650, 160), 95, 3)
        pygame.draw.line(tela, (242, 196, 110), (650, 160), (650, 100), 5)
        pygame.draw.line(tela, (242, 196, 110), (650, 160), (695, 190), 5)
        texto(tela, 'IFRN • UMA AVENTURA SOBRE RECOMEÇAR', 70, 65, 17, (90, 212, 193))
        texto(tela, 'ONE MORE', 65, 110, 58)
        texto(tela, 'TRY', 65, 173, 66, (242, 196, 110))
        texto(tela, 'Uma prova. Um dia. Outra chance.', 70, 257, 21)
        for botao in self.botoes:
            botao.desenhar(tela)
        if self.ajuda:
            linhas = ['WASD: mover • E: interagir', 'ENTER: avançar diálogos', '1–4 ou mouse: responder', 'H: comprar dica • ESC: pausar', 'Meta: 50 pontos. Com −30, o dia reinicia.', '9 questões • até 90 s de prova']
        else:
            linhas = ['Acompanhe PeLezin até a escola.', 'Acerte a prova e volte para celebrar.', 'Se der errado... tente mais uma vez.', 'Partida aproximada: 2 minutos']
        for i, linha in enumerate(linhas):
            texto(tela, linha, 390, 315 + i * 34, 17, largura=370)
        texto(tela, 'PROJETO ANUAL • PROGRAMAÇÃO ORIENTADA A OBJETOS', 70, 555, 15, (145, 162, 185))


