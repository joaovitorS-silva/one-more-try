import pygame
from settings import PRETO, BRANCO, CINZA

_fonte = None


def _get_fonte():
    """Inicializa a fonte apenas quando o pygame já estiver rodando."""
    global _fonte
    if _fonte is None:
        _fonte = pygame.font.SysFont("arial", 32, bold=True)
    return _fonte


class Botao: 
    def __init__(self, texto, x, y, largura, altura):
        self.texto  = texto
        self.rect   = pygame.Rect(x, y, largura, altura)
        self.hover  = False

    def desenhar(self, tela):
        cor = CINZA if self.hover else BRANCO
        pygame.draw.rect(tela, cor, self.rect, border_radius=20)

        fonte      = _get_fonte()
        texto_surf = fonte.render(self.texto, True, PRETO)
        tela.blit(texto_surf, texto_surf.get_rect(center=self.rect.center))

    def verificar_hover(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )