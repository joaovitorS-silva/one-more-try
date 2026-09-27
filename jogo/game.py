import pygame
from jogo.settings import LARGURA, ALTURA, FPS, TITULO
from jogo.cenas.cena import TelaQuarto
from jogo.cenas.menu import TelaInicial
from jogo.ui.interface import texto
from jogo.sistemas.progresso import Progresso
from jogo.ui.caderno import desenhar_caderno


class Game:
    def __init__(self):
        pygame.init()
        # SCALED mantém as coordenadas do jogo e do mouse em 800x600.
        self.tela = pygame.display.set_mode(
            (LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED
        )
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.pausado = False
        self.dt = 0
        self.tentativa = 1
        self.nota = 0
        self.progresso = Progresso()
        self.caderno_aberto = False
        self.pagina_caderno = 0
        self.aviso = ""
        self.tempo_aviso = 0
        self.cena_atual = TelaInicial(self)

    def trocar_cena(self, nova_cena):
        self.cena_atual = nova_cena
        self.caderno_aberto = False

    def nova_partida(self):
        self.progresso = Progresso()
        self.caderno_aberto = False
        self.pagina_caderno = 0
        self.aviso = ""
        self.tempo_aviso = 0
        self.tentativa = 1
        self.nota = 0
        self.pausado = False
        self.trocar_cena(TelaQuarto(self))

    def notificar(self, mensagem):
        self.aviso = mensagem
        self.tempo_aviso = 4

    def registrar(self, chave, titulo, descricao):
        if self.progresso.registrar(chave, titulo, descricao):
            self.notificar('Caderno atualizado: ' + titulo)

    def reiniciar_manha(self):
        self.tentativa += 1
        self.nota = 0
        self.progresso.reiniciar_manha()
        self.registrar('ciclo', 'Outra chance', 'A prova queimou e acordei no quarto. Minhas descobertas continuam neste caderno.')
        self.trocar_cena(TelaQuarto(self))
        self.notificar('Outra manhã. Suas memórias ficaram! TAB: caderno')

    def executar(self):
        while self.rodando:
            self.dt = min(self.clock.tick(FPS) / 1000, 0.05)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.sair()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
                    if not isinstance(self.cena_atual, TelaInicial) and not self.pausado:
                        self.caderno_aberto = not self.caderno_aberto
                    eventos = []
                    break
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    if self.caderno_aberto:
                        self.caderno_aberto = False
                        eventos = []
                        break
                    if not isinstance(self.cena_atual, TelaInicial):
                        self.pausado = not self.pausado
                    eventos = []
                    break
            if not self.rodando:
                break
            if self.caderno_aberto:
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RIGHT:
                            self.pagina_caderno += 1
                        elif evento.key == pygame.K_LEFT:
                            self.pagina_caderno -= 1
            elif self.pausado:
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
            if self.caderno_aberto:
                desenhar_caderno(self.tela, self)
            elif (not self.pausado and self.tempo_aviso > 0
                  and not getattr(getattr(self.cena_atual, 'dialogo', None), 'ativo', False)
                  and not getattr(getattr(self.cena_atual, 'desafio', None), 'ativo', False)):
                self.tempo_aviso = max(0, self.tempo_aviso - self.dt)
                rect_aviso = pygame.Rect(getattr(self.cena_atual, 'rect_aviso', (20, 533, 760, 32)))
                pygame.draw.rect(self.tela, (20, 37, 49), rect_aviso, border_radius=8)
                texto(self.tela, self.aviso, rect_aviso.x + 15, rect_aviso.y + 7, 17, (245, 210, 135), rect_aviso.width - 30)
            pygame.display.flip()
        pygame.quit()

    def sair(self):
        self.rodando = False
