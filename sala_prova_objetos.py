"""
Objetos específicos da sala de prova — mesa do professor, cadeiras dos alunos,
campos de visão, etc.
"""
import pygame
import math


class MesaProfessor:
    """Mesa onde o professor fica durante o exame."""
    
    def __init__(self, x, y, largura=180, altura=100):
        self.rect = pygame.Rect(x, y, largura, altura)
    
    def desenhar(self, tela, fonte):
        """Desenha a mesa com rótulo."""
        pygame.draw.rect(tela, (70, 50, 30), self.rect, border_radius=8)
        pygame.draw.rect(tela, (100, 100, 255), self.rect, width=3, border_radius=8)
        
        txt = fonte.render("Mesa do Professor", True, (100, 100, 255))
        tela.blit(txt, txt.get_rect(center=self.rect.center))


class CadeiraAluno:
    """Cadeira individual de aluno — apenas visual."""
    
    def __init__(self, x, y, largura=50, altura=50):
        self.rect = pygame.Rect(x, y, largura, altura)
    
    def desenhar(self, tela):
        """Desenha a cadeira (retângulo amarelo)."""
        pygame.draw.rect(tela, (255, 255, 0), self.rect, width=3, border_radius=4)


class CampoVisaoProfessor:
    """Campo de visão do professor — visualização de onde ele consegue ver."""
    
    def __init__(self, professor_rect, raio=150):
        """
        Args:
            professor_rect: pygame.Rect do professor
            raio: raio do campo de visão em pixels
        """
        self.professor_rect = professor_rect
        self.raio = raio
    
    def desenhar(self, tela, cor=(255, 100, 100, 50)):
        """Desenha o campo de visão como um círculo semi-transparente."""
        # Criar superfície temporária com transparência
        surf = pygame.Surface((tela.get_width(), tela.get_height()), pygame.SRCALPHA)
        
        # Desenhar círculo semi-transparente
        centro = (
            self.professor_rect.centerx,
            self.professor_rect.centery
        )
        pygame.draw.circle(surf, cor, centro, self.raio)
        
        # Desenhar borda do círculo
        pygame.draw.circle(surf, (255, 100, 100, 150), centro, self.raio, width=2)
        
        tela.blit(surf, (0, 0))
    
    def pode_ver(self, alvo_rect):
        """Verifica se algo está dentro do campo de visão."""
        distancia = math.sqrt(
            (self.professor_rect.centerx - alvo_rect.centerx) ** 2 +
            (self.professor_rect.centery - alvo_rect.centery) ** 2
        )
        return distancia <= self.raio


class BarraVidaProfessor:
    """Barra visual de vida do professor — aparece no topo da tela."""
    
    def __init__(self, x, y, largura=400, altura=30):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
    
    def desenhar(self, tela, fonte, vida_atual, vida_maxima):
        """Desenha a barra de vida."""
        # Fundo (barra vazia)
        pygame.draw.rect(tela, (100, 100, 100), (self.x, self.y, self.largura, self.altura))
        pygame.draw.rect(tela, (200, 200, 200), (self.x, self.y, self.largura, self.altura), width=2)
        
        # Barra de vida (proporcional)
        percentual = vida_atual / vida_maxima if vida_maxima > 0 else 0
        largura_vida = self.largura * percentual
        
        # Cor varia com a vida (verde → amarelo → vermelho)
        if percentual > 0.5:
            cor = (0, 255, 0)  # Verde
        elif percentual > 0.25:
            cor = (255, 255, 0)  # Amarelo
        else:
            cor = (255, 0, 0)  # Vermelho
        
        pygame.draw.rect(tela, cor, (self.x, self.y, largura_vida, self.altura))
        
        # Texto de vida
        txt = fonte.render(f"Vida do Professor: {int(vida_atual)}/{vida_maxima}", True, (255, 255, 255))
        tela.blit(txt, (self.x + 10, self.y + 5))
