import pygame
from jogo.ui.interface import texto


def desenhar_caderno(tela, game):
    sombra = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    sombra.fill((8, 13, 25, 235))
    tela.blit(sombra, (0, 0))
    pygame.draw.rect(tela, (237, 225, 192), (35, 30, 730, 540), border_radius=16)
    cor = (38, 47, 63)
    texto(tela, 'CADERNO DE MEMÓRIAS', 65, 50, 29, cor)
    texto(tela, f'Tentativa {game.tentativa} • As descobertas atravessam o tempo.', 65, 95, 18, cor)
    objetivo = 'Prova em andamento: alcance 50 pontos.' if getattr(game.cena_atual, 'prova', None) else game.progresso.objetivo
    if game.nota >= 50:
        objetivo = 'Você passou! Volte para casa e celebre com sua família.'
    texto(tela, objetivo, 65, 127, 19, cor, 655)
    entradas = list(game.progresso.memorias.values())
    paginas = max(1, (len(entradas) + 2) // 3)
    game.pagina_caderno = max(0, min(game.pagina_caderno, paginas - 1))
    if not entradas:
        texto(tela, 'Seu caderno ainda está vazio. Investigue o quarto e converse com as pessoas.', 65, 205, 22, cor, 640)
    for i, (titulo, descricao) in enumerate(entradas[game.pagina_caderno * 3:game.pagina_caderno * 3 + 3]):
        y = 195 + i * 105
        texto(tela, titulo, 65, y, 22, cor)
        texto(tela, descricao, 65, y + 30, 18, cor, 650)
    texto(tela, f'Setas: páginas ({game.pagina_caderno + 1}/{paginas}) • TAB ou ESC: fechar', 65, 525, 18, cor)
