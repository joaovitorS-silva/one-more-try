import pygame
from settings import LARGURA, ALTURA, FPS, TITULO
from botoes_tela_inicial import Botao
from cena import TelaQuarto
from interface import texto


class TelaInicial:
    """Menu desenhado com formas e fontes, sem imagens externas."""
    def __init__(self, game):
        self.game = game
        self.ajuda = False
        self.botoes = [Botao(t, 70, 300 + i * 72, 280, 55)
                       for i, t in enumerate(('Jogar', 'Como jogar', 'Sair'))]

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.game.nova_partida()
                return
            for i, botao in enumerate(self.botoes):
                if botao.clicado(evento):
                    if i == 0:
                        self.game.nova_partida()
                    elif i == 1:
                        self.ajuda = not self.ajuda
                    else:
                        self.game.sair()
                    return

    def atualizar(self):
        for botao in self.botoes:
            botao.verificar_hover(pygame.mouse.get_pos())

    def desenhar(self, tela):
        tela.fill((17, 25, 43))
        for y in range(0, ALTURA, 30):
            pygame.draw.line(tela, (24, 35, 54), (0, y), (800, y))
        pygame.draw.circle(tela, (38, 66, 83), (650, 160), 150, 2)
        pygame.draw.circle(tela, (68, 187, 173), (650, 160), 95, 3)
        pygame.draw.line(tela, (242, 196, 110), (650, 160), (650, 100), 5)
        pygame.draw.line(tela, (242, 196, 110), (650, 160), (695, 190), 5)
        texto(tela, 'IFRN • UMA AVENTURA SOBRE RECOMEÇAR', 70, 65, 17, (90, 212, 193))
        texto(tela, 'ONE MORE', 65, 110, 58)
        texto(tela, 'TRY', 65, 173, 66, (242, 196, 110))
        texto(tela, 'Uma prova. Um dia. Outra chance.', 70, 257, 21)
        for botao in self.botoes:
            botao.desenhar(tela)
        if self.ajuda:
            linhas = ['WASD: mover • E: interagir', 'ENTER: avançar diálogos', '1–4 ou mouse: responder', 'H: comprar dica • ESC: pausar', 'Meta: 50 pontos. Com −30, o dia reinicia.', '9 questões • até 90 s de prova']
        else:
            linhas = ['Acompanhe PeLezin até a escola.', 'Acerte a prova e volte para celebrar.', 'Se der errado... tente mais uma vez.', 'Partida aproximada: 2 minutos']
        for i, linha in enumerate(linhas):
            texto(tela, linha, 390, 315 + i * 34, 17, largura=370)
        texto(tela, 'PROJETO ANUAL • PROGRAMAÇÃO ORIENTADA A OBJETOS', 70, 555, 15, (145, 162, 185))


class Game:
    """Mantém a troca direta de cenas da base original."""
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.pausado = False
        self.dt = 0
        self.tentativa = 1
        self.nota = 0
        self.cena_atual = TelaInicial(self)

    def trocar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def nova_partida(self):
        self.tentativa = 1
        self.nota = 0
        self.pausado = False
        self.trocar_cena(TelaQuarto(self))

    def executar(self):
        while self.rodando:
            self.dt = min(self.clock.tick(FPS) / 1000, 0.05)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.sair()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    if not isinstance(self.cena_atual, TelaInicial):
                        self.pausado = not self.pausado
                    eventos = []
                    break
            if not self.rodando:
                break
            if self.pausado:
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                        self.pausado = False
                        self.trocar_cena(TelaInicial(self))
                        eventos = []
                        break
            else:
                cena = self.cena_atual
                cena.processar_eventos(eventos)
                if cena is self.cena_atual:
                    cena.atualizar()
            self.cena_atual.desenhar(self.tela)
            if self.pausado:
                overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                overlay.fill((10, 15, 25, 225))
                self.tela.blit(overlay, (0, 0))
                texto(self.tela, 'PAUSA', 320, 240, 42)
                texto(self.tela, 'ESC: continuar • M: menu principal', 220, 315)
            pygame.display.flip()
        pygame.quit()

    def sair(self):
        self.rodando = False


if __name__ == '__main__':
    Game().executar()
