import pygame
from jogo.sistemas.sprites import sprites


class ObjetoCenario:

    def __init__(self, rotulo, cor, x, y, largura, altura):
        self.rotulo = rotulo
        self.cor = cor
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela, fonte):
        sprites.desenhar(tela, self.rotulo.lower().replace(" ", "_"), self.rect, self.cor)
        pygame.draw.rect(tela, (255, 255, 255), self.rect, width=2, border_radius=6)

        if self.rotulo:
            txt = fonte.render(self.rotulo, True, (255, 255, 255))
            tela.blit(txt, txt.get_rect(midbottom=(self.rect.centerx, self.rect.top - 4)))


class Porta(ObjetoCenario):

    def __init__(self, x, y, largura=55, altura=140, rotulo="Porta"):
        super().__init__(rotulo, (90, 60, 30), x, y, largura, altura)

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class Banco(ObjetoCenario):

    def __init__(self, x, y, largura=140, altura=50, rotulo="Banco"):
        super().__init__(rotulo, (120, 90, 60), x, y, largura, altura)

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class Chao:

    def __init__(self, y, largura, altura=8, cor=(100, 80, 60)):
        self.rect = pygame.Rect(0, y, largura, altura)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        # Borda superior para dar efeito de profundidade
        pygame.draw.line(tela, (150, 120, 90), (0, self.rect.top), (self.rect.width, self.rect.top), width=2)
