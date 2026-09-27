import pygame
from jogo.settings import LARGURA, ALTURA, FPS, TITULO
from jogo.cenas.cena import TelaQuarto
from jogo.cenas.menu import TelaInicial
from jogo.ui.interface import texto


class Game:
    """Mantém a troca direta de cenas da base original."""
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.pausado = False
        self.dt = 0
        self.tentativa = 1
        self.nota = 0
        self.cena_atual = TelaInicial(self)

    def trocar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def nova_partida(self):
        self.tentativa = 1
        self.nota = 0
        self.pausado = False
        self.trocar_cena(TelaQuarto(self))

    def executar(self):
        while self.rodando:
            self.dt = min(self.clock.tick(FPS) / 1000, 0.05)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.sair()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    if not isinstance(self.cena_atual, TelaInicial):
                        self.pausado = not self.pausado
                    eventos = []
                    break
            if not self.rodando:
                break
            if self.pausado:
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                        self.pausado = False
                        self.trocar_cena(TelaInicial(self))
                        eventos = []
                        break
            else:
                cena = self.cena_atual
                cena.processar_eventos(eventos)
                if cena is self.cena_atual:
                    cena.atualizar()
            self.cena_atual.desenhar(self.tela)
            if self.pausado:
                overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                overlay.fill((10, 15, 25, 225))
                self.tela.blit(overlay, (0, 0))
                texto(self.tela, 'PAUSA', 320, 240, 42)
                texto(self.tela, 'ESC: continuar • M: menu principal', 220, 315)
            pygame.display.flip()
        pygame.quit()

    def sair(self):
        self.rodando = False


