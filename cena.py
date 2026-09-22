"""
Fases do jogo - telas de transição (Quarto, Cozinha, Ponto de Ônibus, Pátio).

Para a sala de prova, veja sala_prova.py
Para diálogos, veja dialogo.py
Para objetos de cenário (portas, móveis, banco), veja objetos_cenario.py
"""
import pygame
from settings import LARGURA, ALTURA, FONTE_NOME, BRANCO
from models import Pelezin, NPC
from sprites import sprites
from interface import texto
from dialogo import GerenciadorDialogo
from objetos_cenarios import ObjetoCenario, Porta, Banco, Chao


class FaseBase:
    """Classe base para todas as fases do jogo.

    Características:
    - Gerencia o jogador (PeLezin)
    - Controla movimentação com WASD
    - Por padrão, avança de fase sozinha quando o jogador sai pela borda
      direita da tela — algumas fases (com porta clicável) desligam isso
      usando `usa_transicao_automatica = False`
    - Fornece método base para desenhar
    """

    usa_transicao_automatica = True

    def __init__(self, game, cor_fundo, nome_fase):
        self.game = game
        self.cor_fundo = cor_fundo
        self.nome_fase = nome_fase
        self.jogador = Pelezin("sol", 0, 5, 50, ALTURA // 2)
        self.chao = None  # Será setado nas subclasses que usam chão

        # Fonte criada uma única vez
        self._fonte_nome_fase = pygame.font.SysFont(FONTE_NOME, 24, bold=True)

    def processar_eventos(self, eventos):
        """Processa eventos. Sobrescrever em subclasses se necessário."""
        pass

    def atualizar(self):
        """Atualiza posição do jogador com entrada do teclado."""
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(int(teclas[pygame.K_d]) - int(teclas[pygame.K_a]),
                                 int(teclas[pygame.K_s]) - int(teclas[pygame.K_w]))
        if direcao.length_squared():
            direcao = direcao.normalize() * self.jogador.velocidade * 60 * self.game.dt
        obstaculos = [getattr(self, nome).rect for nome in ('cama', 'fliperama')
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
        """Desenha a fase básica."""
        tela.fill(self.cor_fundo)
        sprites.desenhar(tela, "pelezin", self.jogador.rect, (0, 255, 0))
        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))
        texto(tela, "WASD: mover | E perto de pessoas/portas | ENTER: diálogo | ESC: pausa", 20, 555, 17)

    def proxima_fase(self):
        """Chamado quando o jogador avança. Sobrescrever em subclasses."""
        pass


# ─── CENA 1: QUARTO ───────────────────────────────────────────────────────────

class TelaQuarto(FaseBase):
    """Quarto com móveis sólidos e porta acionada por proximidade."""

    usa_transicao_automatica = False

    def __init__(self, game):
        super().__init__(game, (100, 55, 30), "1. Quarto do PeLezin")

        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)

        # Chão da sala
        self.chao = Chao(y=500, largura=LARGURA, altura=100, cor=(80, 50, 20))

        # Móveis sólidos: a colisão é resolvida em FaseBase.
        self.cama = ObjetoCenario("Cama", (101, 67, 33), 60, 420, 180, 90)
        self.fliperama = ObjetoCenario("Fliperama", (40, 40, 90), 340, 330, 90, 170)

        # Porta no meio da sala, perto do fliperama
        self.porta = Porta(440, 330, largura=60, altura=170)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.interagir(evento, self.porta):
                self.proxima_fase()
                return

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)

        self.chao.desenhar(tela)
        self.cama.desenhar(tela, self._fonte_rotulo)
        self.fliperama.desenhar(tela, self._fonte_rotulo)
        self.porta.desenhar(tela, self._fonte_rotulo)

        sprites.desenhar(tela, "pelezin", self.jogador.rect, (0, 255, 0))

        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))
        texto(tela, "WASD: mover | E perto de pessoas/portas | ENTER: diálogo | ESC: pausa", 20, 555, 17)

    def proxima_fase(self):
        self.game.trocar_cena(TelaCozinha(self.game))


# ─── CENA 2: COZINHA ──────────────────────────────────────────────────────────

class TelaCozinha(FaseBase):
    """Cozinha — a mãe do PeLezin dá um recado antes da escola. A porta fica
    na direita (como nas fases antigas), mas também precisa ser clicada."""

    usa_transicao_automatica = False

    def __init__(self, game):
        super().__init__(game, (180, 140, 90), "2. Cozinha")

        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)

        # Chão da cozinha
        self.chao = Chao(y=490, largura=LARGURA, altura=110, cor=(160, 120, 80))

        self.mae = NPC("Mãe", 380, 200)
        self.dialogo_mae = GerenciadorDialogo([
            "Mãe: Bom dia, filho! Respire e leia cada questão com calma.",
            "PeLezin: Hoje eu passo! E se não der, vou tentar de novo.",
            "Mãe: Lembre: uma classe pode herdar características de outra.",
        ])

        # Porta na direita, precisa ser clicada
        self.porta = Porta(730, 240, largura=50, altura=120)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.dialogo_mae.ativo:
                if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    self.dialogo_mae.proximo()
                continue

            if self.interagir(evento, self.mae):
                self.dialogo_mae.iniciar()
                return

            if self.interagir(evento, self.porta):
                self.proxima_fase()
                return

    def atualizar(self):
        if self.dialogo_mae.ativo:
            return  # jogador fica parado durante o diálogo

        super().atualizar()



    def desenhar(self, tela):
        tela.fill(self.cor_fundo)

        self.chao.desenhar(tela)

        sprites.desenhar(tela, "mae", self.mae.rect, (200, 130, 90))
        pygame.draw.rect(tela, (255, 255, 255), self.mae.rect, width=2)
        txt_mae = self._fonte_rotulo.render(self.mae.nome, True, BRANCO)
        tela.blit(txt_mae, txt_mae.get_rect(midbottom=(self.mae.rect.centerx, self.mae.rect.top - 4)))

        self.porta.desenhar(tela, self._fonte_rotulo)

        sprites.desenhar(tela, "pelezin", self.jogador.rect, (0, 255, 0))

        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))
        texto(tela, "WASD: mover | E perto de pessoas/portas | ENTER: diálogo | ESC: pausa", 20, 555, 17)

        if self.dialogo_mae.ativo:
            self.dialogo_mae.desenhar(tela)

    def proxima_fase(self):
        self.game.trocar_cena(TelaRua(self.game))


# ─── CENA 3: PONTO DE ÔNIBUS ──────────────────────────────────────────────────

class TelaRua(FaseBase):
    """Ponto de ônibus — tem a placa e um banco onde o PeLezin pode "sentar"
    (dispara uma falinha de descanso). Sai pela borda da tela, como antes."""

    def __init__(self, game):
        super().__init__(game, (60, 60, 65), "3. Ponto de Ônibus")

        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)

        # Chão do ponto de ônibus
        self.chao = Chao(y=480, largura=LARGURA, altura=120, cor=(70, 70, 70))

        self.placa_onibus = ObjetoCenario("Ponto de Ônibus", (80, 80, 95), 200, 150, 90, 140)
        self.banco = Banco(400, 420)

        self.dialogo_banco = GerenciadorDialogo([
            "PeLezin: Só um minutinho pra descansar antes do ônibus chegar...",
        ])

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.dialogo_banco.ativo:
                if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    self.dialogo_banco.proximo()
                continue

            if self.interagir(evento, self.banco):
                self.dialogo_banco.iniciar()

    def atualizar(self):
        if self.dialogo_banco.ativo:
            return

        super().atualizar()

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)

        self.chao.desenhar(tela)
        self.placa_onibus.desenhar(tela, self._fonte_rotulo)
        self.banco.desenhar(tela, self._fonte_rotulo)

        sprites.desenhar(tela, "pelezin", self.jogador.rect, (0, 255, 0))

        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))
        texto(tela, "WASD: mover | E perto de pessoas/portas | ENTER: diálogo | ESC: pausa", 20, 555, 17)

        if self.dialogo_banco.ativo:
            self.dialogo_banco.desenhar(tela)

    def proxima_fase(self):
        self.game.trocar_cena(TelaCorredor(self.game))


# ─── CENA 4: PÁTIO DA ESCOLA ──────────────────────────────────────────────────

class TelaCorredor(FaseBase):
    """Pátio da escola ("o meio da escola") — o PeLezin encontra 3 colegas
    antes de ir pra prova. Sai pela borda da tela, como antes."""

    def __init__(self, game):
        super().__init__(game, (210, 180, 140), "4. Pátio da Escola")

        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)

        # Chão do pátio
        self.chao = Chao(y=470, largura=LARGURA, altura=130, cor=(180, 160, 120))

        self.colegas = [
            NPC("Ana", 380, 250),
            NPC("Bruno", 420, 250),
            NPC("Carla", 460, 250),
        ]

        self.dialogo_amigos = GerenciadorDialogo([
            "PeLezin: E aí, pessoal! Preparados pra prova?",
            "Ana: Bora que já tá quase na hora!",
            "Bruno: A cada dois acertos seguidos você ganha 5 créditos de dica.",
            "Carla: Na prova, H compra uma dica e elimina uma alternativa errada.",
        ])

    def processar_eventos(self, eventos):
        for evento in eventos:
            if self.dialogo_amigos.ativo:
                if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    self.dialogo_amigos.proximo()
                continue
            if any(self.interagir(evento, npc) for npc in self.colegas):
                self.dialogo_amigos.iniciar()
                return

    def atualizar(self):
        if self.dialogo_amigos.ativo:
            return

        super().atualizar()


    def desenhar(self, tela):
        tela.fill(self.cor_fundo)

        self.chao.desenhar(tela)

        for npc in self.colegas:
            sprites.desenhar(tela, npc.nome.lower(), npc.rect, (90, 140, 200))
            pygame.draw.rect(tela, (255, 255, 255), npc.rect, width=2)
            txt_nome = self._fonte_rotulo.render(npc.nome, True, BRANCO)
            tela.blit(txt_nome, txt_nome.get_rect(midbottom=(npc.rect.centerx, npc.rect.top - 4)))

        sprites.desenhar(tela, "pelezin", self.jogador.rect, (0, 255, 0))

        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))
        texto(tela, "WASD: mover | E perto de pessoas/portas | ENTER: diálogo | ESC: pausa", 20, 555, 17)

        if self.dialogo_amigos.ativo:
            self.dialogo_amigos.desenhar(tela)

    def proxima_fase(self):
        from sala_prova import TelaSalaProva
        self.game.trocar_cena(TelaSalaProva(self.game))