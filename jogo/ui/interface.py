"""Texto com quebra de linha, compartilhado por menus e prova."""
import pygame


def texto(tela, mensagem, x, y, tamanho=22, cor=(235, 240, 250), largura=700):
    fonte = pygame.font.SysFont('arial', tamanho)
    linha = ''
    for palavra in mensagem.split():
        tentativa = (linha + ' ' + palavra).strip()
        if fonte.size(tentativa)[0] > largura and linha:
            tela.blit(fonte.render(linha, True, cor), (x, y))
            y += fonte.get_linesize()
            linha = palavra
        else:
            linha = tentativa
    tela.blit(fonte.render(linha, True, cor), (x, y))
    return y + fonte.get_linesize()
