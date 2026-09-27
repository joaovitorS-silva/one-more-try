"""Prova curta com nota, dificuldade progressiva e loja de dicas."""
import math
import re
import pygame
from jogo.settings import NOTA_APROVACAO, PONTUACAO_GAME_OVER, TEMPO_PROVA, QUESTOES_POR_NIVEL
from jogo.models import Professor, Prova, LojaDicas, NPC
from jogo.sistemas.banco_perguntas import sortear_prova
from jogo.ui.prova import Alternativa, bloco, FUNDO, TEXTO, SUAVE, VERDE, ERRO
from jogo.cenas.cena import FaseExploracao, TelaCorredor
from jogo.objetos.objetos_cenarios import Chao, Porta
from jogo.objetos.sala_prova_objetos import MesaProfessor, Carteira
from jogo.ui.interface import texto
from jogo.sistemas.sprites import sprites


class TelaSalaProva(FaseExploracao):
    usa_transicao_automatica = False

    def __init__(self, game):
        super().__init__(game, (45, 90, 140), '5. Sala de Prova')
        self.professor = Professor(2, 330, 170)
        self.professor.nome = 'Professor Joaildo'
        self.chao = Chao(510, 800, 90, (53, 64, 72))
        self.mesa_professor = MesaProfessor(585, 135, 150, 55)
        self.cadeiras = [Carteira(x, y) for y in (270, 395) for x in (200, 380, 560)]
        self.carteira = self.cadeiras[3]
        self.carteira.rotulo = 'Sua carteira'
        self.carteira.destacada = True
        self.colegas = [NPC('Lucas', 223, 245), NPC('Bia', 403, 245),
                        NPC('Rafa', 583, 245), NPC('Lia', 403, 370), NPC('Davi', 583, 370)]
        self.adicionar(self.professor, self.conversar_professor)
        self.adicionar(self.colegas[0], lambda: self.falar([
            'Lucas: Minha cabeça fica em branco só de olhar para o quadro...',
            'PeLezin: Respira. Vamos resolver uma questão de cada vez.',
            'Lucas: Valeu! Boa sorte pra gente.']))
        self.adicionar(self.colegas[1], lambda: self.falar([
            'Bia: Estou revisando: multiplicação vem antes da soma.',
            'Bia: E, em Python, a indentação faz parte do código!',
            'PeLezin: Vou conferir meu caderno antes de sentar.']))
        self.adicionar(self.carteira, self.sentar)
        self.volta = self.adicionar(Porta(25, 300, 48, 100, '< Pátio'),
                                   lambda: self.ir(TelaCorredor, True))
        self.jogador.rect.topleft = (95, 335)
        self.ambiente_tempo = 0
        self.escolhendo = False
        self.posicao_antes_de_sentar = None
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
        self.botoes_assuntos = [Alternativa(i, t, (24 + i * 382, 426, 370, 58))
                               for i, t in enumerate(self.assuntos)]
        self.assunto = ''
        self.selecionada = None
        self.transicao = 0

    def conversar_professor(self):
        linhas = ['Professor: Respirem fundo. Cada questão é uma nova chance.',
                  'Professor: São nove questões em 90 segundos. A meta é 50 pontos.',
                  'Professor: Quando estiver pronto, sente na carteira marcada e escolha o assunto.']
        if self.game.tentativa > 1:
            linhas.insert(1, 'PeLezin: Ele disse exatamente isso da outra vez...')
            self.game.registrar('professor_ciclo', 'As mesmas palavras',
                                'Na sala, o professor repetiu a mesma fala. Eu me lembro da outra tentativa.')
        self.falar(linhas)

    def sentar(self):
        self.posicao_antes_de_sentar = self.jogador.rect.topleft
        self.jogador.rect.midbottom = (self.carteira.rect.centerx, self.carteira.rect.top)
        self.escolhendo = True

    def levantar(self):
        self.escolhendo = False
        self.jogador.rect.topleft = self.posicao_antes_de_sentar

    def mover_na_sala(self):
        anterior = self.jogador.rect.topleft
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(int(teclas[pygame.K_d]) - int(teclas[pygame.K_a]),
                                 int(teclas[pygame.K_s]) - int(teclas[pygame.K_w]))
        if direcao.length_squared():
            direcao = direcao.normalize() * self.jogador.velocidade * 60 * self.game.dt
        obstaculos = [c.rect for c in self.cadeiras] + [self.mesa_professor.rect]
        for eixo in ('x', 'y'):
            passo = round(getattr(direcao, eixo))
            if not passo:
                continue
            setattr(self.jogador.rect, eixo, getattr(self.jogador.rect, eixo) + passo)
            for obstaculo in obstaculos:
                if self.jogador.rect.colliderect(obstaculo):
                    lado = ('right' if passo > 0 else 'left') if eixo == 'x' else ('bottom' if passo > 0 else 'top')
                    borda = ('left' if passo > 0 else 'right') if eixo == 'x' else ('top' if passo > 0 else 'bottom')
                    setattr(self.jogador.rect, lado, getattr(obstaculo, borda))
        self.jogador.rect.clamp_ip(pygame.Rect(15, 155, 770, 355))
        self.jogador.atualizar_animacao((self.jogador.rect.x - anterior[0], self.jogador.rect.y - anterior[1]), self.game.dt)

    def iniciar_prova(self, assunto):
        if self.prova is not None:
            return
        self.escolhendo = False
        self.assunto = assunto
        self.questoes = sortear_prova(QUESTOES_POR_NIVEL, QUESTOES_POR_NIVEL,
                                     QUESTOES_POR_NIVEL, assunto=assunto)
        self.prova = Prova(self.questoes)
        self.loja = LojaDicas()
        if self.game.progresso.missao_ana == 'concluida':
            self.loja.creditos = 5
            self.game.notificar('Ajuda da Ana: você começa com 5 créditos de dica.')
        self._carregar_botoes_da_questao()

    @property
    def rect_aviso(self):
        return (20, 275, 760, 32) if self.prova is not None or self.escolhendo else (20, 533, 760, 32)

    def _carregar_botoes_da_questao(self):
        self.eliminadas = []
        self.selecionada = None
        self.transicao = 0
        self.botoes_alternativas = [
            Alternativa(i, re.sub(r'^[A-D]\)\s*', '', opcao),
                        (24 + (i % 2) * 382, 414 + (i // 2) * 55, 370, 48))
            for i, opcao in enumerate(self.questoes[self.idx_atual].opcoes)]

    def responder(self, indice):
        if self.espera or indice in self.eliminadas:
            return
        self.selecionada = indice
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
        from jogo.cenas.finais import TelaViagemTempo, TelaVoltaCorredor
        self.game.nota = self.prova.pontuacao_total
        if self.game.nota >= NOTA_APROVACAO:
            self.game.trocar_cena(TelaVoltaCorredor(self.game))
        else:
            self.game.trocar_cena(TelaViagemTempo(self.game, motivo))

    def processar_eventos(self, eventos):
        if self.prova is None and not self.escolhendo:
            super().processar_eventos(eventos)
            return
        for evento in eventos:
            if self.prova is None:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_BACKSPACE:
                    self.levantar()
                    return
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
        if self.prova is None and not self.escolhendo:
            if self.dialogo.ativo:
                self.jogador.atualizar_animacao((0, 0), self.game.dt)
            if not self.dialogo.ativo:
                self.ambiente_tempo += self.game.dt
                self.professor.rect.x = round(345 + 105 * math.sin(self.ambiente_tempo * 0.45))
                self.mover_na_sala()
            return
        self.ambiente_tempo += self.game.dt
        self.transicao = min(1, self.transicao + self.game.dt / 0.2)
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

    def desenhar_sala(self, tela):
        tela.fill((183, 198, 190))
        pygame.draw.rect(tela, (105, 123, 129), (0, 155, 800, 355))
        for y in range(155, 510, 44):
            pygame.draw.line(tela, (116, 133, 137), (0, y), (800, y))
        for x in range(0, 800, 80):
            pygame.draw.line(tela, (116, 133, 137), (x, 155), (x, 510))
        self.chao.desenhar(tela)
        pygame.draw.rect(tela, (117, 85, 55), (220, 76, 330, 77), border_radius=5)
        pygame.draw.rect(tela, (35, 70, 62), (226, 82, 318, 65))
        texto(tela, 'UMA QUESTÃO DE CADA VEZ', 245, 90, 20, (233, 236, 215))
        texto(tela, 'Leia • respire • tente mais uma vez', 245, 120, 16, (205, 223, 204))
        for x in (55, 630):
            pygame.draw.rect(tela, (238, 230, 207), (x, 77, 105, 60), border_radius=3)
            pygame.draw.rect(tela, (140, 201, 216), (x + 5, 82, 95, 50))
            pygame.draw.line(tela, (238, 230, 207), (x + 52, 80), (x + 52, 135), 4)
        self.mesa_professor.desenhar(tela, self.fonte)
        pygame.draw.rect(tela, (237, 227, 201), (610, 145, 30, 19), border_radius=2)
        self.volta.desenhar(tela, self.fonte)
        sprites.desenhar(tela, 'professor', self.professor.rect, (200, 120, 65))
        texto(tela, 'Joaildo', self.professor.rect.x - 10, self.professor.rect.y - 21, 16)
        for i, colega in enumerate(self.colegas):
            rect = colega.rect.move(0, round(math.sin(self.ambiente_tempo * 2 + i) * 2))
            sprites.desenhar(tela, colega.nome.lower(), rect, [(102, 163, 206), (195, 132, 163), (221, 175, 90)][i % 3])
            texto(tela, colega.nome, rect.x - 4, rect.y - 22, 16)
        sprites.desenhar_jogador(tela, self.jogador)
        for cadeira in self.cadeiras:
            cadeira.desenhar(tela, self.fonte)
        if not self.dialogo.ativo and not self.escolhendo and self.prova is None:
            fase = self.ambiente_tempo % 12
            if 2 <= fase < 5 or 8 <= fase < 11:
                indice = 0 if fase < 6 else 1
                colega = self.colegas[indice]
                frase = 'Estudou pra hoje?' if indice == 0 else 'Só mais uma revisão...'
                caixa = pygame.Rect(colega.rect.x - 45, colega.rect.y - 65, 200, 33)
                pygame.draw.rect(tela, (244, 239, 220), caixa, border_radius=9)
                texto(tela, frase, caixa.x + 10, caixa.y + 7, 16, (43, 58, 65))

    def desenhar(self, tela):
        if self.prova is None and not self.escolhendo:
            self.desenhar_sala(tela)
            alvo = self.alvo()
            if alvo and not self.dialogo.ativo:
                objeto = alvo[0]
                acao = ('Sentar e fazer a prova' if objeto is self.carteira else
                        'Voltar ao pátio' if objeto is self.volta else f'Conversar com {objeto.nome}')
                pygame.draw.rect(tela, (23, 32, 45), (20, 520, 760, 38), border_radius=8)
                texto(tela, f'E — {acao}', 35, 527, 20)
            if self.dialogo.ativo:
                self.dialogo.desenhar(tela)
            return
        self.desenhar_prova(tela)

    def desenhar_ambiente_prova(self, tela):
        """Enquadramento da turma durante a prova, sem mover as colisões da sala."""
        pygame.draw.rect(tela, (178, 197, 191), (0, 58, 800, 254))
        pygame.draw.rect(tela, (95, 115, 124), (0, 166, 800, 146))
        for y in range(170, 312, 35):
            pygame.draw.line(tela, (110, 130, 137), (0, y), (800, y))
        for x in range(0, 800, 100):
            pygame.draw.line(tela, (110, 130, 137), (x, 166), (x, 312))
        pygame.draw.rect(tela, (120, 87, 57), (235, 71, 330, 85), border_radius=4)
        pygame.draw.rect(tela, (34, 70, 62), (241, 77, 318, 73))
        bloco(tela, 'UMA QUESTÃO DE CADA VEZ', (257, 89, 290, 25), 20)
        bloco(tela, 'Leia. Respire. Você consegue.', (268, 121, 276, 22), 16, (187, 216, 197))
        for x in (48, 650):
            pygame.draw.rect(tela, (236, 226, 201), (x, 77, 104, 68), border_radius=3)
            pygame.draw.rect(tela, (139, 198, 213), (x + 5, 82, 94, 58))
            pygame.draw.line(tela, (236, 226, 201), (x + 52, 80), (x + 52, 144), 4)
        professor = pygame.Rect(round(490 + 18 * math.sin(self.ambiente_tempo * 0.5)), 151, 28, 30)
        sprites.desenhar(tela, 'professor', professor, (200, 120, 65))
        bloco(tela, 'Joaildo', (professor.x - 10, 134, 78, 20), 14, (234, 231, 210))
        pygame.draw.rect(tela, (153, 110, 70), (480, 179, 95, 20), border_radius=4)
        pygame.draw.rect(tela, (239, 232, 212), (531, 182, 22, 13), border_radius=2)
        for i in range(6):
            x, y = 130 + (i % 3) * 220, 208 + (i // 3) * 63
            jogador = i == 3
            nome = 'pelezin' if jogador else self.colegas[i if i < 3 else i - 1].nome.lower()
            oscilacao = round(math.sin(self.ambiente_tempo * 1.8 + i))
            rect = pygame.Rect(x + 34, y - 29 + oscilacao, 26, 30)
            sprites.desenhar(tela, nome, rect, (70, 225, 155) if jogador else [(99, 163, 205), (192, 133, 163), (219, 173, 94)][i % 3], direcao='cima')
            pygame.draw.rect(tela, (60, 54, 47), (x, y + 4, 96, 29), border_radius=5)
            pygame.draw.rect(tela, (184, 140, 88), (x, y, 96, 27), border_radius=5)
            pygame.draw.rect(tela, (242, 234, 213), (x + 32, y + 4, 28, 18), border_radius=2)
            pygame.draw.line(tela, (123, 149, 164), (x + 37, y + 9), (x + 53, y + 9), 1)
            if jogador:
                pygame.draw.rect(tela, VERDE, (x - 2, y - 2, 100, 31), 2, border_radius=6)

    def desenhar_prova(self, tela):
        self.desenhar_ambiente_prova(tela)
        pygame.draw.rect(tela, FUNDO, (0, 0, 800, 58))
        pygame.draw.line(tela, (60, 92, 112), (0, 57), (800, 57), 2)
        nota = self.prova.pontuacao_total if self.prova else 0
        bloco(tela, f'NOTA  {nota} / {NOTA_APROVACAO}', (24, 16, 245, 30), 22)
        progresso = f'QUESTÃO  {self.idx_atual + 1} / {len(self.questoes)}' if self.prova else 'PREPARAÇÃO'
        bloco(tela, progresso, (300, 18, 260, 28), 20, SUAVE)
        bloco(tela, f'TEMPO  {math.ceil(self.restante)} s', (600, 16, 185, 30), 21, ERRO if self.restante < 20 else TEXTO)
        pygame.draw.rect(tela, FUNDO, (0, 312, 800, 288))
        pygame.draw.line(tela, (79, 125, 145), (24, 312), (776, 312), 2)
        if self.prova is None:
            bloco(tela, 'SUA CARTEIRA · ESCOLHA O ASSUNTO', (24, 331, 752, 25), 18, SUAVE)
            bloco(tela, 'Pronto para mais uma tentativa?', (24, 370, 752, 36), 27)
            for botao in self.botoes_assuntos:
                botao.desenhar_estado(tela)
            bloco(tela, '1 ou 2: começar • BACKSPACE: levantar', (24, 510, 752, 30), 20)
            bloco(tela, '9 questões • 90 segundos • TAB: caderno • ESC: pausa', (24, 565, 752, 25), 17, SUAVE)
            return
        questao = self.questoes[self.idx_atual]
        nivel = {'facil': 'FÁCIL', 'media': 'MÉDIA', 'dificil': 'DIFÍCIL'}[questao.dificuldade]
        bloco(tela, f'{self.assunto.upper()} · {nivel}     +{questao.pontuacao_acerto} / {questao.pontuacao_erro} pontos', (24, 326, 752, 23), 16, SUAVE)
        # Anima só o conteúdo; posições de clique permanecem estáveis.
        conteudo = pygame.Surface((800, 600), pygame.SRCALPHA)
        bloco(conteudo, questao.enunciado, (24, 355, 752, 52), 23)
        for i, botao in enumerate(self.botoes_alternativas):
            estado = 'eliminada' if i in self.eliminadas else 'normal'
            if self.selecionada is not None:
                estado = 'bloqueada'
                if i == questao.correta:
                    estado = 'correta'
                elif i == self.selecionada:
                    estado = 'errada'
                elif i in self.eliminadas:
                    estado = 'eliminada'
            botao.desenhar_estado(conteudo, estado)
        conteudo.set_alpha(round(180 + 75 * self.transicao))
        tela.blit(conteudo, (0, 0))
        cor = VERDE if self.selecionada == questao.correta else ERRO if self.selecionada is not None else SUAVE
        bloco(tela, self.feedback or 'Escolha uma alternativa com 1–4 ou clique.', (24, 526, 752, 35), 17, cor)
        pygame.draw.line(tela, (55, 77, 98), (24, 563), (776, 563))
        bloco(tela, f'H: dica · {self.loja.creditos} créditos · {self.loja.usadas}/2 usadas', (24, 574, 430, 22), 16, SUAVE)
        bloco(tela, 'TAB: caderno   ESC: pausa', (532, 574, 255, 22), 16, SUAVE)
