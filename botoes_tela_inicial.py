import pygame

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (220, 220, 220)

fonte = None  

class Botao:
    def __init__(self, texto, x, y, largura, altura):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.hover = False

    def desenhar(self, tela):
        global fonte
        if fonte is None:
            fonte = pygame.font.SysFont("arial", 32, bold=True)

        cor = CINZA if self.hover else BRANCO
        pygame.draw.rect(tela, cor, self.rect, border_radius=20)
        texto_surf = fonte.render(self.texto, True, PRETO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def verificar_hover(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

