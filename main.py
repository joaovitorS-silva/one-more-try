import pygame
import sys

from settings import LARGURA, ALTURA, FPS, TITULO, PRETO
from botoes_tela_inicial import Botao
# from cena import TelaJogo
from cena import TelaQuarto

class TelaInicial:
    """Tela de menu principal — Jogar, Opções, Sair."""

    def __init__(self, game):
        self.game = game
        bx = LARGURA // 2 - 150
        self.botoes = [
            Botao("Jogar",  bx, 120, 300, 60),
            Botao("Opções", bx, 200, 300, 60),
            Botao("Sair",   bx, 280, 300, 60),
        ]
        self.acoes = {
            "Jogar":  self._jogar,
            "Opções": self._opcoes,
            "Sair":   self.game.sair,
        }

    def _jogar(self):
        print("Iniciando jogo...")
        # TODO: self.game.trocar_cena(TelaJogo(self.game))
        self.game.trocar_cena(TelaQuarto(self.game))
        
    def _opcoes(self):
        print("Abrindo opções...")
        # TODO: self.game.trocar_cena(TelaOpcoes(self.game))


    def processar_eventos(self, eventos):
        for evento in eventos:
            for botao in self.botoes:
                if botao.clicado(evento):
                    self.acoes[botao.texto]()

    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.verificar_hover(pos_mouse)

    def desenhar(self, tela):
        tela.fill(PRETO)
        for botao in self.botoes:
            botao.desenhar(tela)


class Game:
    """Gerenciador principal do jogo — controla o loop e as cenas."""

    def __init__(self):
        pygame.init()
        self.tela       = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock      = pygame.time.Clock()
        self.rodando    = True
        self.cena_atual = None
        pygame.display.set_caption(TITULO)

    def trocar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def executar(self):
        self.trocar_cena(TelaInicial(self))

        while self.rodando:
            eventos = pygame.event.get()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.sair()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.sair()

            self.cena_atual.processar_eventos(eventos)
            self.cena_atual.atualizar()

            self.tela.fill(PRETO)
            self.cena_atual.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(FPS)

    def sair(self):
        self.rodando = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().executar()
