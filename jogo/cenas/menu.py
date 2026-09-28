import pygame
from jogo.ui.botoes_tela_inicial import Botao
from jogo.ui.interface import texto


class TelaInicial:
    def __init__(self, game):
        self.game = game
        self.botoes = [Botao(t, 70, 300 + i * 72, 280, 55)
                       for i, t in enumerate(('Jogar', 'Sair'))]

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.game.nova_partida()
                return
            for i, botao in enumerate(self.botoes):
                if botao.clicado(evento):
                    if i == 0:
                        self.game.nova_partida()
                    else:
                        self.game.sair()
                    return

    def atualizar(self):
        for botao in self.botoes:
            botao.verificar_hover(pygame.mouse.get_pos())

    def desenhar(self, tela):
        tela.fill((17, 25, 43))
        texto(tela, 'ONE MORE', 65, 110, 58)
        texto(tela, 'TRY', 65, 173, 66, (242, 196, 110))
        for botao in self.botoes:
            botao.desenhar(tela)


