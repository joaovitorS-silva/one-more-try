"""Desfechos com as mesmas cenas e diálogos simples da jornada."""
import math
import pygame
from cena import FaseBase, TelaRua, TelaCozinha, TelaQuarto
from models import NPC
from dialogo import GerenciadorDialogo
from interface import texto
from sprites import sprites


class TelaViagemTempo:
    def __init__(self, game, motivo):
        self.game = game
        self.motivo = motivo
        self.tempo = 0

    def processar_eventos(self, eventos):
        pass  # A viagem acontece automaticamente depois da animação curta.

    def atualizar(self):
        self.tempo += self.game.dt
        if self.tempo >= 4:
            self.game.tentativa += 1
            self.game.nota = 0
            self.game.trocar_cena(TelaQuarto(self.game))

    def desenhar(self, tela):
        tela.fill((23, 17, 30))
        texto(tela, 'AINDA HÁ OUTRA CHANCE', 140, 65, 34, (250, 190, 105))
        texto(tela, f'{self.motivo} Nota: {self.game.nota}', 100, 125, 22)
        altura = max(0, int(220 * (1 - self.tempo / 3)))
        if altura:
            pygame.draw.rect(tela, (240, 227, 199), (280, 200, 240, altura))
            for i in range(12):
                x = 280 + i * 20
                y = 200 + altura
                chama = int(25 + 20 * (1 + math.sin(self.tempo * 14 + i)))
                pygame.draw.polygon(tela, (250, 100 + i * 8, 40), [(x, y), (x + 10, y - chama), (x + 20, y)])
        if self.tempo > 2:
            for raio in range(30, 240, 35):
                pygame.draw.circle(tela, (90, 130, 210), (400, 310), int(raio + self.tempo * 15) % 240, 2)
        texto(tela, 'O relógio volta... você acordará no quarto.', 170, 490, 22)
        texto(tela, f'Próxima tentativa: {self.game.tentativa + 1}', 285, 530, 20)


class TelaVoltaCorredor(FaseBase):
    def __init__(self, game):
        super().__init__(game, (93, 115, 108), '6. Aprovado! Saída da escola →')
        self.colega = NPC('Ana', 370, 300)
        self.dialogo = GerenciadorDialogo([
            f'Ana: Você conseguiu! {game.nota} pontos! Vamos comemorar?',
            'PeLezin: Vou contar para minha família. Valeu pela força!',
        ])

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.dialogo.ativo:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    self.dialogo.proximo()
            elif self.interagir(evento, self.colega):
                self.dialogo.iniciar()

    def atualizar(self):
        if not self.dialogo.ativo:
            super().atualizar()

    def desenhar(self, tela):
        super().desenhar(tela)
        sprites.desenhar(tela, 'ana', self.colega.rect, (90, 140, 200))
        texto(tela, 'Ana • E para conversar', 300, 265, 18)
        texto(tela, f'Nota final: {self.game.nota} • Siga à direita para voltar para casa.', 30, 90)
        if self.dialogo.ativo:
            self.dialogo.desenhar(tela)

    def proxima_fase(self):
        self.game.trocar_cena(TelaRuaVolta(self.game))


class TelaRuaVolta(TelaRua):
    def __init__(self, game):
        super().__init__(game)
        self.nome_fase = '7. Caminho de casa →'
        self.dialogo_banco.linhas = ['PeLezin: A prova passou. Agora posso respirar!']

    def proxima_fase(self):
        self.game.trocar_cena(TelaCelebracao(self.game))


class TelaCelebracao(TelaCozinha):
    def __init__(self, game):
        super().__init__(game)
        self.nome_fase = '8. Lar, doce lar!'
        self.dialogo_mae.linhas = [
            f'PeLezin: Mãe, passei! Tirei {game.nota} pontos!',
            'Mãe: Eu sabia que você conseguiria. Estamos orgulhosos!',
            'PeLezin: Cada tentativa me ensinou alguma coisa. Vamos celebrar!',
        ]
        self.dialogo_mae.iniciar()
        self.concluiu = False

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if self.dialogo_mae.ativo:
                    self.dialogo_mae.proximo()
                    if not self.dialogo_mae.ativo:
                        self.concluiu = True
                    return
                if self.concluiu:
                    from main import TelaInicial
                    self.game.trocar_cena(TelaInicial(self.game))
                    return

    def atualizar(self):
        pass

    def desenhar(self, tela):
        super().desenhar(tela)
        if self.concluiu:
            pygame.draw.rect(tela, (20, 35, 45), (90, 130, 620, 270), border_radius=20)
            texto(tela, 'VOCÊ PASSOU DE ANO!', 165, 170, 36, (245, 205, 110))
            texto(tela, f'Nota: {self.game.nota} • Tentativas: {self.game.tentativa}', 230, 240, 24)
            texto(tela, 'ENTER para voltar ao menu', 240, 315, 22)
