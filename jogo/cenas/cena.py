import pygame
from jogo.settings import LARGURA, ALTURA, FONTE_NOME, BRANCO
from jogo.models import Pelezin, NPC
from jogo.sistemas.sprites import sprites
from jogo.ui.interface import texto
from jogo.sistemas.dialogo import GerenciadorDialogo
from jogo.objetos.objetos_cenarios import ObjetoCenario, Porta, Banco, Chao


class FaseBase:

    usa_transicao_automatica = True

    def __init__(self, game, cor_fundo, nome_fase):
        self.game = game
        self.cor_fundo = cor_fundo
        self.nome_fase = nome_fase
        self.jogador = Pelezin("sol", 0, 5, 50, ALTURA // 2)
        self.chao = None  # Será setado nas subclasses que usam chão

        # Fonte criada uma única vez
        self._fonte_nome_fase = pygame.font.SysFont(FONTE_NOME, 24, bold=True)

    

    def atualizar(self):
        anterior = self.jogador.rect.topleft
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(int(teclas[pygame.K_d]) - int(teclas[pygame.K_a]),
                                 int(teclas[pygame.K_s]) - int(teclas[pygame.K_w]))
        if direcao.length_squared():
            direcao = direcao.normalize() * self.jogador.velocidade * 60 * self.game.dt
        obstaculos = [getattr(self, nome).rect for nome in ('cama', 'fliperama', 'escrivaninha')
                      if hasattr(self, nome)]
        for eixo in ('x', 'y'):
            deslocamento = round(getattr(direcao, eixo))
            setattr(self.jogador.rect, eixo, getattr(self.jogador.rect, eixo) + deslocamento)
            for obstaculo in obstaculos:
                if self.jogador.rect.colliderect(obstaculo):
                    if eixo == 'x':
                        if deslocamento > 0:
                            self.jogador.rect.right = obstaculo.left
                        elif deslocamento < 0:
                            self.jogador.rect.left = obstaculo.right
                    else:
                        if deslocamento > 0:
                            self.jogador.rect.bottom = obstaculo.top
                        elif deslocamento < 0:
                            self.jogador.rect.top = obstaculo.bottom
        limite_y = self.chao.rect.top if self.chao else ALTURA
        self.jogador.rect.clamp_ip(pygame.Rect(0, 65, LARGURA, limite_y - 65))
        self.jogador.atualizar_animacao((self.jogador.rect.x - anterior[0], self.jogador.rect.y - anterior[1]), self.game.dt)
        if self.usa_transicao_automatica and self.jogador.rect.right >= LARGURA:
            self.proxima_fase()

    def perto(self, objeto):
        return self.jogador.rect.inflate(90, 90).colliderect(objeto.rect)

    def interagir(self, evento, objeto):
        return self.perto(objeto) and (
            (evento.type == pygame.KEYDOWN and evento.key == pygame.K_e)
            or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and objeto.rect.collidepoint(evento.pos)))

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        sprites.desenhar_jogador(tela, self.jogador)




class FaseExploracao(FaseBase):
    usa_transicao_automatica = False

    def __init__(self, game, cor, nome):
        super().__init__(game, cor, nome)
        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)
        self.objetos = []
        self.interacoes = []
        self.dialogo = GerenciadorDialogo([])
        self.desafio = None
        self.imagem_fundo = None
        self.objetos_no_fundo = []

    def adicionar(self, objeto, acao, novidade=lambda: False):
        self.objetos.append(objeto)
        self.interacoes.append((objeto, acao, novidade))
        return objeto

    def falar(self, linhas):
        self.dialogo.linhas = linhas
        self.dialogo.iniciar()

    def ir(self, classe, voltando=False):
        cena = classe(self.game)
        if voltando:
            cena.jogador.rect.topleft = getattr(cena, 'posicao_retorno', (650, 310))
        self.game.trocar_cena(cena)

    def alvo(self, evento=None):
        candidatos = [item for item in self.interacoes if self.perto(item[0])]
        if evento is not None and evento.type == pygame.MOUSEBUTTONDOWN:
            candidatos = [item for item in candidatos if item[0].rect.collidepoint(evento.pos)]
        if not candidatos:
            return None
        return min(candidatos, key=lambda item: pygame.Vector2(getattr(item[0], 'area_interacao', item[0].rect).center).distance_squared_to(self.jogador.rect.center))

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.desafio and self.desafio.ativo:
                self.desafio.processar(evento)
                return
            if self.dialogo.ativo:
                if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    self.dialogo.proximo()
                return
            if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_e) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                alvo = self.alvo(evento)
                if alvo:
                    alvo[1]()
                    return

    def atualizar(self):
        if self.dialogo.ativo or (self.desafio and self.desafio.ativo):
            self.jogador.atualizar_animacao((0, 0), self.game.dt)
            return
        super().atualizar()

    def desenhar(self, tela):
        if self.imagem_fundo is not None:
            tela.blit(self.imagem_fundo, (0, 0))
        else:
            tela.fill(self.cor_fundo)
            if self.chao:
                self.chao.desenhar(tela)
        for objeto in self.objetos:
            if objeto in self.objetos_no_fundo:
                continue
            if isinstance(objeto, NPC):
                sprites.desenhar(tela, objeto.nome.lower(), objeto.rect, (85, 155, 185))
                texto(tela, objeto.nome, objeto.rect.x - 5, objeto.rect.y - 24, 17)
            else:
                objeto.desenhar(tela, self._fonte_rotulo)
        for objeto, _, novidade in self.interacoes:
            if novidade():
                pygame.draw.circle(tela, (250, 207, 105), (objeto.rect.centerx, objeto.rect.top - 38), 10)
                texto(tela, '!', objeto.rect.centerx - 3, objeto.rect.top - 49, 18, (30, 35, 45))
        if self.imagem_fundo is not None:
            sombra = pygame.Rect(0, 0, 42, 9)
            sombra.midbottom = self.jogador.rect.midbottom
            pygame.draw.ellipse(tela, (68, 45, 33), sombra)
        sprites.desenhar_jogador(tela, self.jogador)
        alvo = self.alvo()
        if alvo and not self.dialogo.ativo:
            nome = getattr(alvo[0], 'nome', getattr(alvo[0], 'rotulo', ''))
            pygame.draw.rect(tela, (23, 32, 45), (20, 520, 760, 38), border_radius=8)
            texto(tela, f'E — Interagir: {nome}', 35, 527, 20)
        if self.dialogo.ativo:
            self.dialogo.desenhar(tela)
        if self.desafio and self.desafio.ativo:
            self.desafio.desenhar(tela)


class TelaQuarto(FaseExploracao):
    def __init__(self, game):
        super().__init__(game, (100, 55, 30), '1. Quarto • O começo de mais um dia')
        self.chao = Chao(500, LARGURA, 100, (80, 50, 20))
        self.cama = ObjetoCenario('Cama', (101, 67, 33), 60, 420, 180, 90)
        self.objetos.append(self.cama)
        self.fliperama = self.adicionar(ObjetoCenario('Fliperama', (40, 40, 90), 340, 330, 90, 170), self.jogar, lambda: 'sequencia' not in game.progresso.memorias)
        self.porta = self.adicionar(Porta(440, 330, 60, 170, 'Cozinha >'), self.proxima_fase)
        self.escrivaninha = self.adicionar(ObjetoCenario('Escrivaninha', (125, 90, 55), 160, 155, 150, 65), self.estudar, lambda: 'estudo' not in game.progresso.memorias)
        self.relogio = self.adicionar(ObjetoCenario('Relógio 07:10', (45, 75, 90), 575, 145, 80, 65), self.investigar, lambda: ('relogio_repetido' if game.tentativa > 1 else 'relogio') not in game.progresso.memorias)
        self.imagem_fundo = sprites.carregar_fundo('quarto', (LARGURA, ALTURA))
        if self.imagem_fundo is not None:
            # Áreas alinhadas aos móveis pintados no fundo de 800x600.
            self.cama.rect = pygame.Rect(32, 365, 275, 92)
            self.fliperama.rect = pygame.Rect(322, 252, 96, 196)
            self.porta.rect = pygame.Rect(427, 192, 114, 255)
            self.escrivaninha.rect = pygame.Rect(582, 351, 168, 103)
            self.relogio.rect = pygame.Rect(28, 379, 29, 20)
            self.objetos_no_fundo = [self.cama, self.fliperama, self.porta, self.escrivaninha, self.relogio]
            self.chao.rect.top = 555
            # O retângulo representa os pés, não toda a altura do sprite.
            self.jogador.rect = pygame.Rect(130, 484, 34, 16)
            self.jogador.altura_visual = 152
            self.jogador.velocidade = 3
            self.posicao_retorno = (466, 484)
            self.area_caminhada = pygame.Rect(16, 438, 768, 74)
            self.obstaculos = [
                pygame.Rect(0, 435, 307, 27),       # cama e criado-mudo
                pygame.Rect(322, 430, 96, 24),      # base do fliperama
                pygame.Rect(582, 434, 168, 23),     # escrivaninha e cadeira
                pygame.Rect(546, 439, 38, 20),      # mochila
                pygame.Rect(750, 430, 50, 50),      # guarda-roupa
            ]
            self.fliperama.area_interacao = pygame.Rect(327, 459, 86, 43)
            self.porta.area_interacao = pygame.Rect(435, 453, 100, 49)
            self.escrivaninha.area_interacao = pygame.Rect(602, 463, 125, 39)
            self.relogio.area_interacao = pygame.Rect(20, 466, 65, 36)

    def perto(self, objeto):
        if self.imagem_fundo is None:
            return super().perto(objeto)
        area = getattr(objeto, 'area_interacao', objeto.rect)
        return self.jogador.rect.inflate(16, 16).colliderect(area)

    def atualizar(self):
        if self.imagem_fundo is None:
            return super().atualizar()
        if self.dialogo.ativo or (self.desafio and self.desafio.ativo):
            self.jogador.atualizar_animacao((0, 0), self.game.dt)
            return
        antes = self.jogador.rect.topleft
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(int(teclas[pygame.K_d]) - int(teclas[pygame.K_a]),
                                 int(teclas[pygame.K_s]) - int(teclas[pygame.K_w]))
        if direcao.length_squared():
            direcao = direcao.normalize() * self.jogador.velocidade * 60 * self.game.dt
        for eixo in ('x', 'y'):
            passo = round(getattr(direcao, eixo))
            # Subpassos impedem atravessar uma base fina com um quadro lento.
            sinal = 1 if passo > 0 else -1
            for _ in range(abs(passo)):
                setattr(self.jogador.rect, eixo, getattr(self.jogador.rect, eixo) + sinal)
                if not self.area_caminhada.contains(self.jogador.rect) or any(self.jogador.rect.colliderect(o) for o in self.obstaculos):
                    setattr(self.jogador.rect, eixo, getattr(self.jogador.rect, eixo) - sinal)
                    break
        self.jogador.atualizar_animacao((self.jogador.rect.x - antes[0], self.jogador.rect.y - antes[1]), self.game.dt)


    def estudar(self):
        from jogo.ui.desafio import Desafio
        self.desafio = Desafio('Uma revisão antes de sair', 'Em POO, o que permite uma classe aproveitar outra?', ['Herança', 'Um comentário', 'Uma variável local', 'Um número decimal'], 0,
            'Herança permite que uma classe reutilize atributos e métodos de outra.',
            lambda: self.game.registrar('estudo', 'Revisão: herança', 'Uma classe filha pode herdar atributos e métodos de uma classe base.'))

    def jogar(self):
        from jogo.ui.desafio import Desafio
        self.desafio = Desafio('Fliperama • Descubra o padrão', 'Qual é o próximo número? 2, 4, 8, 16, ...', ['18', '24', '32', '64'], 2,
            'Cada número é o anterior multiplicado por 2.',
            lambda: self.game.registrar('sequencia', 'Padrões e potências', '2, 4, 8, 16, 32: multiplicar por 2 gera potências de 2.'))

    def investigar(self):
        self.game.registrar('relogio', 'O relógio do quarto', 'Ao acordar, o relógio marcava 07:10. Seu ponteiro parece tremer.')
        linhas = ['PeLezin: 07:10. Ainda dá tempo de revisar antes de sair.', 'O ponteiro treme por um instante, como se quisesse andar para trás.']
        if self.game.tentativa > 1:
            self.game.registrar('relogio_repetido', '07:10 outra vez', 'Depois da prova queimar, acordei no mesmo horário. As anotações do caderno ficaram!')
            linhas = ['PeLezin: 07:10 de novo?! Eu já fiz aquela prova...', 'PeLezin: O dia voltou, mas meu caderno ainda tem o que descobri. Preciso falar com Ana.']
        self.falar(linhas)

    def proxima_fase(self):
        self.ir(TelaCozinha)


class TelaCozinha(FaseExploracao):
    def __init__(self, game):
        super().__init__(game, (180, 140, 90), '2. Cozinha')
        self.chao = Chao(490, LARGURA, 110, (160, 120, 80))
        self.mae = self.adicionar(NPC('Mãe', 380, 200), self.conversar, lambda: 'mae' not in game.progresso.conversas)
        self.dialogo_mae = self.dialogo
        self.porta = self.adicionar(Porta(730, 240, 50, 120, 'Rua >'), self.proxima_fase)
        self.volta = self.adicionar(Porta(20, 200, 45, 105, '< Quarto'), lambda: self.ir(TelaQuarto, True))

    def conversar(self):
        self.game.progresso.conversas.add('mae')
        linhas = ['Mãe: Bom dia, filho! Respire e leia cada questão com calma.', 'PeLezin: Vou revisar e encontrar meus amigos antes da prova.', 'Mãe: Aprender também é pedir ajuda. Veja se alguém precisa da sua.']
        if self.game.tentativa > 1:
            linhas = ['PeLezin: Já sei: respirar e ler cada questão com calma...', 'Mãe: Como adivinhou o que eu ia dizer?', 'PeLezin: Acho que esta manhã está se repetindo. Mas desta vez tenho minhas anotações.']
            self.game.registrar('mae_repeticao', 'Uma fala antecipada', 'Consegui dizer o conselho da minha mãe antes dela. O ciclo parece real.')
        self.falar(linhas)

    def proxima_fase(self):
        self.ir(TelaRua)


class TelaRua(FaseExploracao):
    def __init__(self, game):
        super().__init__(game, (60, 60, 65), '3. Ponto de ônibus')
        self.chao = Chao(480, LARGURA, 120, (70, 70, 70))
        self.placa_onibus = ObjetoCenario('Ponto de ônibus', (80, 80, 95), 200, 150, 90, 140)
        self.objetos.append(self.placa_onibus)
        self.banco = self.adicionar(Banco(400, 420), self.descansar)
        self.dialogo_banco = self.dialogo
        self.dialogo_banco.linhas = ['PeLezin: Um respiro antes da prova.']
        self.volta = self.adicionar(Porta(20, 230, 45, 110, '< Casa'), lambda: self.ir(TelaCozinha, True))
        self.saida = self.adicionar(Porta(730, 230, 45, 110, 'Pátio >'), self.proxima_fase)
        self.anotacoes = ObjetoCenario('Folhas de Ana', (240, 225, 160), 575, 390, 35, 25)
        if game.progresso.missao_ana not in ('encontradas', 'concluida'):
            self.adicionar(self.anotacoes, self.recolher, lambda: True)

    def descansar(self):
        self.dialogo_banco.iniciar()

    def recolher(self):
        if self.game.progresso.recolher_anotacoes():
            self.objetos.remove(self.anotacoes)
            self.interacoes = [i for i in self.interacoes if i[0] is not self.anotacoes]
            self.game.registrar('folhas', 'As anotações de Ana', 'Encontrei folhas perto do banco no ponto de ônibus. Elas têm o nome de Ana.')
            self.game.notificar('Anotações recolhidas! Encontre Ana no pátio.')
            self.falar(['PeLezin: Estas folhas são da Ana! Vou levar para ela no pátio.'])

    def proxima_fase(self):
        self.ir(TelaCorredor)


class TelaCorredor(FaseExploracao):
    def __init__(self, game):
        super().__init__(game, (150, 165, 120), '4. Pátio da escola')
        self.chao = Chao(470, LARGURA, 130, (115, 135, 95))
        self.colegas = [NPC('Ana', 270, 230), NPC('Bruno', 430, 280), NPC('Carla', 580, 200)]
        self.adicionar(self.colegas[0], self.conversar_ana, lambda: game.progresso.missao_ana in ('desconhecida', 'encontradas') or (game.tentativa > 1 and 'ana_ciclo' not in game.progresso.memorias))
        self.adicionar(self.colegas[1], self.conversar_bruno, lambda: 'bruno' not in game.progresso.conversas)
        self.adicionar(self.colegas[2], self.conversar_carla, lambda: 'carla' not in game.progresso.conversas)
        self.dialogo_amigos = self.dialogo
        self.volta = self.adicionar(Porta(20, 240, 45, 110, '< Ponto'), lambda: self.ir(TelaRua, True))
        self.saida = self.adicionar(Porta(730, 240, 45, 110, 'Prova >'), self.proxima_fase)

    def conversar_ana(self):
        progresso = self.game.progresso
        linhas = []
        if self.game.tentativa > 1:
            linhas += ['PeLezin: Ana, você sente que já viveu este dia?', 'Ana: Sonhei com uma prova pegando fogo... e um relógio marcando 07:10. Como você sabia?']
            self.game.registrar('ana_ciclo', 'Ana também se lembra', 'Ana sonhou com a prova queimando e com 07:10. Talvez eu não esteja sozinho neste ciclo.')
        if progresso.devolver_anotacoes():
            self.game.registrar('amizade_ana', 'Uma ajuda de volta', 'Devolver as folhas de Ana concede 5 créditos no início da prova daquela manhã.')
            self.game.registrar('revisao_ana', 'Revisão com Ana', 'Matemática: faça multiplicações antes das somas. POO: encapsulamento organiza e controla o acesso ao estado do objeto.')
            self.game.notificar('Missão concluída! +5 créditos ao começar a prova.')
            linhas += ['Ana: Minhas anotações! Obrigada por voltar para me ajudar.', 'Ana: Em Matemática, resolva multiplicações antes das somas. Em POO, lembre do encapsulamento.', 'Ana: Você terá cinco créditos de dica quando começar a prova. Pode consultar nossa revisão no caderno!']
        elif progresso.missao_ana == 'concluida':
            linhas += ['Ana: Obrigada pela ajuda. Nossa revisão está no seu caderno. Boa prova!']
        else:
            progresso.aceitar_missao()
            self.game.notificar('Missão: encontre as anotações no ponto de ônibus.')
            linhas += ['Ana: Perdi minhas anotações! Acho que deixei perto do banco no ponto de ônibus.', 'PeLezin: Posso voltar e procurar. Ainda não comecei a prova.', 'Ana: Obrigada! Se encontrar, traga aqui e revisamos juntos.']
        self.falar(linhas)

    def conversar_bruno(self):
        self.game.progresso.conversas.add('bruno')
        self.game.registrar('creditos', 'Dicas sem perder nota', 'Dois acertos seguidos rendem 5 créditos. H elimina uma alternativa errada; no máximo duas dicas por prova.')
        self.falar(['Bruno: Dois acertos seguidos rendem cinco créditos de dica.', 'Bruno: Use H na prova. Os créditos são separados da nota!'])

    def conversar_carla(self):
        self.game.progresso.conversas.add('carla')
        self.game.registrar('regras', 'Preparação para a prova', 'São nove questões em 90 segundos. Meta: 50 pontos. Com -30, o tempo volta. TAB abre o caderno e pausa o cronômetro.')
        self.falar(['Carla: Começa fácil e termina difícil. Você precisa de 50 pontos.', 'Carla: Revise no caderno com TAB. Entre naquela porta à direita quando estiver pronto.'])

    def proxima_fase(self):
        from jogo.cenas.sala_prova import TelaSalaProva
        self.game.trocar_cena(TelaSalaProva(self.game))
