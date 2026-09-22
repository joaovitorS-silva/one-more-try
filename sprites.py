"""Imagens opcionais: sem arquivo, preserva os retângulos do protótipo."""
from pathlib import Path
import pygame


class GerenciadorSprites:
    def __init__(self, pasta=None):
        self.pasta = Path(pasta) if pasta else Path(__file__).parent / 'assets' / 'sprites'
        self.cache = {}

    def desenhar(self, tela, nome, rect, cor):
        chave = (nome, rect.size)
        if chave not in self.cache:
            arquivo = self.pasta / (nome + '.png')
            imagem = None
            if arquivo.is_file():
                try:
                    imagem = pygame.transform.scale(pygame.image.load(str(arquivo)).convert_alpha(), rect.size)
                except (pygame.error, OSError):
                    pass
            self.cache[chave] = imagem
        imagem = self.cache[chave]
        if imagem is None:
            pygame.draw.rect(tela, cor, rect, border_radius=5)
        else:
            tela.blit(imagem, rect)


sprites = GerenciadorSprites()
