"""
Gerenciador de diálogos do jogo — reutilizável para qualquer cena.
"""
import pygame
from settings import FONTE_NOME, ALTURA, LARGURA


class GerenciadorDialogo:
    """Gerencia a exibição de diálogos em estilo RPG.
    
    Uso:
        dialogo = GerenciadorDialogo([
            "PeLezin: Oi professor!",
            "Prof. Joaildo: Olá, PeLezin!",
        ])
        
        # Em processar_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            dialogo.proximo()
            
        # Em desenhar:
        if dialogo.ativo:
            dialogo.desenhar(tela)
    """
    
    def __init__(self, linhas):
        """Inicializa o gerenciador com uma lista de linhas de diálogo."""
        self.linhas = linhas
        self.indice_atual = 0
        self.ativo = False
        self._fonte_dialogo = pygame.font.SysFont(FONTE_NOME, 20)
        self._fonte_dica = pygame.font.SysFont(FONTE_NOME, 14)
    
    def iniciar(self):
        """Inicia o diálogo."""
        self.ativo = True
        self.indice_atual = 0
    
    def proximo(self):
        """Avança para a próxima linha de diálogo."""
        self.indice_atual += 1
        if self.indice_atual >= len(self.linhas):
            self.ativo = False
            return False  # Diálogo acabou
        return True  # Ainda há mais linhas
    
    def acabou(self):
        """Retorna True se o diálogo acabou."""
        return not self.ativo
    
    def desenhar(self, tela):
        """Desenha a caixa de diálogo na parte inferior da tela."""
        largura_d = LARGURA - 80
        altura_d = 130
        x_dialogo = 40
        y_dialogo = ALTURA - altura_d - 30
        
        # Fundo da caixa de diálogo
        pygame.draw.rect(tela, (20, 20, 30), (x_dialogo, y_dialogo, largura_d, altura_d), border_radius=14)
        pygame.draw.rect(tela, (255, 255, 255), (x_dialogo, y_dialogo, largura_d, altura_d), width=3, border_radius=14)
        
        # Linha atual de diálogo
        linha_atual = self.linhas[self.indice_atual]
        txt_linha = self._fonte_dialogo.render(linha_atual, True, (255, 255, 255))
        tela.blit(txt_linha, (x_dialogo + 25, y_dialogo + 25))
        
        # Dica de como continuar
        txt_dica = self._fonte_dica.render("Clique ou aperte uma tecla para continuar...", True, (180, 180, 180))
        tela.blit(txt_dica, (x_dialogo + 25, y_dialogo + altura_d - 40))
