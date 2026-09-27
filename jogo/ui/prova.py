"""Interface compacta da prova: texto ajustado e alternativas em duas colunas."""
from functools import lru_cache
import pygame
from jogo.ui.botoes_tela_inicial import Botao

FUNDO = (20, 32, 49)
TEXTO = (239, 242, 244)
SUAVE = (164, 186, 206)
VERDE = (68, 218, 182)
ERRO = (255, 148, 139)


@lru_cache(maxsize=24)
def _fonte(tamanho, negrito=False):
    return pygame.font.SysFont('arial', tamanho, bold=negrito)


def fonte(tamanho, negrito=False):
    f = _fonte(tamanho, negrito)
    try:
        f.size('')
    except pygame.error:
        _fonte.cache_clear()
        f = _fonte(tamanho, negrito)
    return f


def ajustar_texto(mensagem, largura, altura, tamanho=21):
    """Quebra também palavras longas; reduz a fonte somente quando necessário."""
    for pontos in range(tamanho, 10, -1):
        f = fonte(pontos)
        linhas = []
        for paragrafo in mensagem.split('\n'):
            linha = ''
            for palavra in paragrafo.split():
                if f.size((linha + ' ' + palavra).strip())[0] <= largura:
                    linha = (linha + ' ' + palavra).strip()
                    continue
                if linha:
                    linhas.append(linha)
                linha = ''
                for letra in palavra:
                    if f.size(linha + letra)[0] > largura:
                        linhas.append(linha)
                        linha = ''
                    linha += letra
            linhas.append(linha)
        if len(linhas) * f.get_linesize() <= altura:
            return f, linhas
    return f, linhas


def bloco(tela, mensagem, rect, tamanho=21, cor=TEXTO):
    rect = pygame.Rect(rect)
    f, linhas = ajustar_texto(mensagem, rect.width, rect.height, tamanho)
    anterior = tela.get_clip()
    tela.set_clip(rect.clip(anterior))
    for i, linha in enumerate(linhas):
        tela.blit(f.render(linha, True, cor), (rect.x, rect.y + i * f.get_linesize()))
    tela.set_clip(anterior)


class Alternativa(Botao):
    def __init__(self, indice, mensagem, rect):
        super().__init__(mensagem, *rect)
        self.indice = indice

    def desenhar_estado(self, tela, estado='normal'):
        fundo, borda, cor = (29, 47, 66), (85, 111, 136), TEXTO
        if estado == 'eliminada':
            fundo, borda, cor = (24, 37, 52), (48, 64, 79), (119, 136, 151)
        elif estado == 'correta':
            fundo, borda = (22, 67, 65), VERDE
        elif estado == 'errada':
            fundo, borda = (77, 42, 50), ERRO
        elif self.hover and estado == 'normal':
            fundo, borda = (36, 67, 84), VERDE
        pygame.draw.rect(tela, fundo, self.rect, border_radius=8)
        pygame.draw.rect(tela, borda, self.rect, 2, border_radius=8)
        badge = pygame.Rect(self.rect.x + 10, self.rect.y + 9, 28, 28)
        pygame.draw.rect(tela, borda, badge, border_radius=5)
        numero = fonte(18, True).render(str(self.indice + 1), True, FUNDO)
        tela.blit(numero, numero.get_rect(center=badge.center))
        mensagem = 'Alternativa eliminada' if estado == 'eliminada' else self.texto
        bloco(tela, mensagem, (self.rect.x + 49, self.rect.y + 5, self.rect.width - 59, self.rect.height - 10), 18, cor)
