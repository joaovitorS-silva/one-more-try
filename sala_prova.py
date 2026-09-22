"""Prova curta com nota, dificuldade progressiva e loja de dicas."""
import math
import pygame
from settings import NOTA_APROVACAO, PONTUACAO_GAME_OVER, TEMPO_PROVA, QUESTOES_POR_NIVEL
from models import Professor, Prova, LojaDicas
from banco_perguntas import sortear_prova
from botoes_tela_inicial import Botao
from cena import FaseBase
from objetos_cenarios import Chao
from sala_prova_objetos import MesaProfessor, CadeiraAluno
from interface import texto
from sprites import sprites


class TelaSalaProva(FaseBase):
    usa_transicao_automatica = False

    def __init__(self, game):
        super().__init__(game, (45, 90, 140), '5. Sala de Prova')
        self.professor = Professor(2, 400, 150)
        self.chao = Chao(480, 800, 120, (40, 60, 100))
        self.mesa_professor = MesaProfessor(580, 80)
        self.cadeiras = [CadeiraAluno(x, y) for x in range(200, 650, 80) for y in (280, 380)]
        self.fonte = pygame.font.SysFont('arial', 16)
        self.prova = None
        self.loja = LojaDicas()
        self.idx_atual = 0
        self.restante = TEMPO_PROVA
        self.feedback = ''
        self.espera = 0
        self.eliminadas = []
        self.botoes_alternativas = []
        self.assuntos = ['POO e Python', 'Matemática']
        self.botoes_assuntos = [Botao(t, 160, 295 + i * 80, 480, 60)
                               for i, t in enumerate(self.assuntos)]

    def iniciar_prova(self, assunto):
        self.questoes = sortear_prova(QUESTOES_POR_NIVEL, QUESTOES_POR_NIVEL,
                                     QUESTOES_POR_NIVEL, assunto=assunto)
        self.prova = Prova(self.questoes)
        self._carregar_botoes_da_questao()

    def _carregar_botoes_da_questao(self):
        self.eliminadas = []
        self.botoes_alternativas = [Botao(f'{i + 1}. {opcao}', 75, 255 + i * 58, 650, 50)
                                   for i, opcao in enumerate(self.questoes[self.idx_atual].opcoes)]

    def responder(self, indice):
        if self.espera or indice in self.eliminadas:
            return
        questao = self.questoes[self.idx_atual]
        acertou = indice == questao.correta
        self.prova.responder(questao, acertou)
        self.loja.registrar_resposta(acertou)
        self.feedback = (f'Acertou! +{questao.pontuacao_acerto} pontos.' if acertou else
                         f'{questao.pontuacao_erro} pontos. Correta: {questao.opcoes[questao.correta]}')
        self.espera = 1.3
        if self.prova.pontuacao_total <= PONTUACAO_GAME_OVER:
            self.encerrar('A nota chegou a −30 pontos.')

    def encerrar(self, motivo='A prova terminou.'):
        from finais import TelaViagemTempo, TelaVoltaCorredor
        self.game.nota = self.prova.pontuacao_total
        if self.game.nota >= NOTA_APROVACAO:
            self.game.trocar_cena(TelaVoltaCorredor(self.game))
        else:
            self.game.trocar_cena(TelaViagemTempo(self.game, motivo))

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.prova is None:
                for i, botao in enumerate(self.botoes_assuntos):
                    if botao.clicado(evento) or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_1 + i):
                        self.iniciar_prova(self.assuntos[i])
                        return
                continue
            if self.espera:
                continue
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_h:
                eliminada = self.loja.comprar(self.questoes[self.idx_atual], self.eliminadas)
                if eliminada is not None:
                    self.eliminadas.append(eliminada)
                    self.feedback = 'Dica comprada: uma alternativa errada foi eliminada.'
                else:
                    self.feedback = 'Você precisa de 5 créditos. Limite: 2 dicas por prova.'
                return
            for i, botao in enumerate(self.botoes_alternativas):
                if botao.clicado(evento) or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_1 + i):
                    self.responder(i)
                    return

    def atualizar(self):
        botoes = self.botoes_assuntos if self.prova is None else self.botoes_alternativas
        for botao in botoes:
            botao.verificar_hover(pygame.mouse.get_pos())
        if self.prova is None:
            return
        self.restante = max(0, self.restante - self.game.dt)
        if self.restante <= 0:
            self.encerrar('O tempo da prova acabou.')
            return
        if self.espera:
            self.espera = max(0, self.espera - self.game.dt)
            if self.espera == 0:
                self.idx_atual += 1
                if self.idx_atual == len(self.questoes):
                    self.encerrar()
                    return
                self.feedback = ''
                self._carregar_botoes_da_questao()

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        self.chao.desenhar(tela)
        self.mesa_professor.desenhar(tela, self.fonte)
        for cadeira in self.cadeiras:
            cadeira.desenhar(tela)
        sprites.desenhar(tela, 'professor', self.professor.rect, (200, 100, 40))
        sprites.desenhar(tela, 'pelezin', self.jogador.rect, (0, 255, 0))
        pygame.draw.rect(tela, (20, 31, 49), (40, 45, 720, 510), border_radius=18)
        if self.prova is None:
            texto(tela, 'A prova do ano', 75, 80, 36)
            texto(tela, 'Professor: escolha o assunto e mostre o que aprendeu!', 75, 140, 21)
            texto(tela, '9 questões • 90 segundos • aprovação: 50 pontos', 75, 190, 21)
            texto(tela, 'Fácil → média → difícil. Escolha com 1, 2 ou mouse.', 75, 225, 19)
            for botao in self.botoes_assuntos:
                botao.desenhar(tela)
            return
        questao = self.questoes[self.idx_atual]
        texto(tela, f'Nota: {self.prova.pontuacao_total} / meta: 50', 75, 65, 24)
        texto(tela, f'Tempo: {math.ceil(self.restante)} s', 560, 65, 24,
              (255, 140, 110) if self.restante < 20 else (235, 240, 250))
        texto(tela, f'Questão {self.idx_atual + 1}/9 • {questao.dificuldade} • +{questao.pontuacao_acerto} / {questao.pontuacao_erro}', 75, 105, 19)
        texto(tela, questao.enunciado, 75, 150, 20, largura=650)
        for i, botao in enumerate(self.botoes_alternativas):
            if i not in self.eliminadas:
                botao.desenhar(tela)
            else:
                texto(tela, f'{i + 1}. Alternativa eliminada', botao.rect.x + 15, botao.rect.y + 12, 19, (130, 150, 170))
        texto(tela, self.feedback or f'H: dica (5 créditos) • saldo: {self.loja.creditos} • usadas: {self.loja.usadas}/2', 75, 493, 17, largura=650)
        texto(tela, '1–4 ou clique: responder • ESC: pausar', 180, 570, 18)
