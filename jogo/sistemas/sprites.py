from pathlib import Path
import pygame


class GerenciadorSprites:
    def __init__(self, pasta=None):
        self.pasta = Path(pasta) if pasta else Path(__file__).resolve().parents[2] / 'assets' / 'sprites'
        self.cache = {}
        self.quadros_personagem = None
        self.cache_personagem = {}
        self.cache_fundos = {}

    def carregar_fundo(self, nome, tamanho):
        chave = (nome, tamanho)
        if chave not in self.cache_fundos:
            try:
                arquivo = self.pasta / (nome + '.png')
                imagem = pygame.image.load(str(arquivo)).convert()
                self.cache_fundos[chave] = pygame.transform.smoothscale(imagem, tamanho)
            except (pygame.error, OSError):
                self.cache_fundos[chave] = None
        return self.cache_fundos[chave]

    def carregar_personagem(self):
        if self.quadros_personagem is not None:
            return self.quadros_personagem
        self.quadros_personagem = {}
        arquivo = self.pasta / 'personagem_principal.png'
        if not arquivo.is_file():
            return self.quadros_personagem
        try:
            folha = pygame.image.load(str(arquivo)).convert_alpha()
            # A folha fornecida tem margens e espaçamentos irregulares.
            # Limites entre as poses, referenciados à imagem original 1230x1278.
            xs = [round(x * folha.get_width() / 1230) for x in (100, 350, 620, 880, 1150)]
            ys = [round(y * folha.get_height() / 1278) for y in (35, 320, 625, 930, 1230)]
            for linha, direcao in enumerate(('baixo', 'cima', 'esquerda', 'direita')):
                quadros = []
                for coluna in range(4):
                    celula = folha.subsurface((xs[coluna], ys[linha], xs[coluna + 1] - xs[coluna], ys[linha + 1] - ys[linha]))
                    limites = celula.get_bounding_rect(min_alpha=128)
                    quadros.append(celula.subsurface(limites).copy())
                self.quadros_personagem[direcao] = quadros
        except (pygame.error, OSError, ValueError):
            self.quadros_personagem = {}
        return self.quadros_personagem

    def desenhar_jogador(self, tela, jogador):
        self.desenhar(tela, 'pelezin', jogador.rect, (70, 225, 155),
                      jogador.direcao, jogador.quadro_animacao,
                      altura=getattr(jogador, 'altura_visual', None))

    def desenhar(self, tela, nome, rect, cor, direcao='baixo', quadro=0, altura=None):
        if nome == 'pelezin' and self.carregar_personagem():
            altura = altura or round(rect.height * 1.7)
            chave = (direcao, quadro, altura)
            if chave not in self.cache_personagem:
                original = self.quadros_personagem[direcao][quadro]
                largura = max(1, round(original.get_width() * altura / original.get_height()))
                self.cache_personagem[chave] = pygame.transform.scale(original, (largura, altura))
            imagem = self.cache_personagem[chave]
            tela.blit(imagem, imagem.get_rect(midbottom=rect.midbottom))
            return
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
