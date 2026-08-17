"""
Objetos de cenário reutilizáveis: móveis decorativos, a porta interativa
(clicável, usada para trocar de cena) e o banco onde o jogador pode sentar.
"""
import pygame


class ObjetoCenario:
    """Objeto decorativo simples — sem interação (ainda). Ex.: cama, fliperama,
    placa de ônibus. Só ocupa espaço na tela e mostra um rótulo em cima."""

    def __init__(self, rotulo, cor, x, y, largura, altura):
        self.rotulo = rotulo
        self.cor = cor
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela, fonte):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)
        pygame.draw.rect(tela, (255, 255, 255), self.rect, width=2, border_radius=6)

        if self.rotulo:
            txt = fonte.render(self.rotulo, True, (255, 255, 255))
            tela.blit(txt, txt.get_rect(midbottom=(self.rect.centerx, self.rect.top - 4)))


class Porta(ObjetoCenario):
    """Porta clicável — o jogador clica em cima dela pra mudar de cena.
    Não bloqueia o personagem fisicamente, ele pode andar por cima normalmente."""

    def __init__(self, x, y, largura=55, altura=140, rotulo="Porta"):
        super().__init__(rotulo, (90, 60, 30), x, y, largura, altura)

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class Banco(ObjetoCenario):
    """Banco clicável — o jogador clica pra "sentar" (dispara um diálogo curto
    de descanso, sem precisar de sprite de animação por enquanto)."""

    def __init__(self, x, y, largura=140, altura=50, rotulo="Banco"):
        super().__init__(rotulo, (120, 90, 60), x, y, largura, altura)

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class Chao:
    """Chão/piso visual da cena — uma linha horizontal que marca onde o
    personagem "caminha". Sem colisão física por enquanto, apenas visual."""

    def __init__(self, y, largura, altura=8, cor=(100, 80, 60)):
        """
        Args:
            y: posição Y do chão
            largura: largura total (geralmente a largura da tela)
            altura: espessura do chão em pixels
            cor: cor RGB do chão
        """
        self.rect = pygame.Rect(0, y, largura, altura)
        self.cor = cor

    def desenhar(self, tela):
        """Desenha o chão na tela."""
        pygame.draw.rect(tela, self.cor, self.rect)
        # Borda superior para dar efeito de profundidade
        pygame.draw.line(tela, (150, 120, 90), (0, self.rect.top), (self.rect.width, self.rect.top), width=2)