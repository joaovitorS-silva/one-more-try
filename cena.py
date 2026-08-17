import pygame
from settings import (
    LARGURA, ALTURA, PONTUACAO_GAME_OVER, FONTE_NOME,
    BRANCO, VERDE, DOURADO,
    COR_FUNDO_QUARTO, COR_FUNDO_RUA, COR_FUNDO_CORREDOR, COR_FUNDO_SALA,
    COR_QUADRO, COR_PAINEL_PROVA, COR_OVERLAY,
)
from models import Pelezin, PerguntaFacil, PerguntaMedia, PerguntaDificil
from botoes_tela_inicial import Botao

class FaseBase:
    def __init__(self, game, cor_fundo, nome_fase):
        self.game = game
        self.cor_fundo = cor_fundo
        self.nome_fase = nome_fase
        self.jogador = Pelezin("sol", 0, 5, 50, ALTURA // 2)

        # Fonte criada uma única vez:
        self._fonte_nome_fase = pygame.font.SysFont(FONTE_NOME, 24, bold=True)

    def processar_eventos(self, eventos):
        pass

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:  self.jogador.rect.y -= self.jogador.velocidade
        if teclas[pygame.K_s]:  self.jogador.rect.y += self.jogador.velocidade
        if teclas[pygame.K_a]:  self.jogador.rect.x -= self.jogador.velocidade
        if teclas[pygame.K_d]:  self.jogador.rect.x += self.jogador.velocidade
            
        if self.jogador.rect.top < 0: self.jogador.rect.top = 0
        if self.jogador.rect.bottom > ALTURA: self.jogador.rect.bottom = ALTURA
        if self.jogador.rect.left < 0: self.jogador.rect.left = 0

        if self.jogador.rect.right >= LARGURA:
            self.proxima_fase()

    def desenhar(self, tela):
        tela.fill(self.cor_fundo) 
        pygame.draw.rect(tela, (0, 255, 0), self.jogador.rect)
        
        fonte = pygame.font.SysFont("arial", 24, bold=True)
        texto_surf = self._fonte_nome_fase.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, 20))

    def proxima_fase(self):
        pass


# ─── FASES DE TRANSIÇÃO (Caminhada) ──────────────────────────────────────────

class TelaQuarto(FaseBase):
    def __init__(self, game): super().__init__(game, (100, 55, 30), "1. Quarto do PeLezin")
    def proxima_fase(self): self.game.trocar_cena(TelaRua(self.game))

class TelaRua(FaseBase):
    def __init__(self, game): super().__init__(game, (60, 60, 65), "2. Rua em Direção ao IFRN")
    def proxima_fase(self): self.game.trocar_cena(TelaCorredor(self.game))

class TelaCorredor(FaseBase):
    def __init__(self, game): super().__init__(game, (210, 180, 140), "3. Corredor da Escola")
    def proxima_fase(self): self.game.trocar_cena(TelaSalaProva(self.game))


# ─── FASE DA SALA DE AULA (Com ativação por colisão e Overlay) ────────────────

class TelaSalaProva(FaseBase):
    """Sala de aula onde o jogador precisa andar até o quadro para iniciar a prova."""
    
    def __init__(self, game):
        super().__init__(game, COR_FUNDO_SALA, "4. Sala de Prova")

        self._fonte_quadro = pygame.font.SysFont(FONTE_NOME, 18, bold=True)
        self._fonte_hud = pygame.font.SysFont(FONTE_NOME, 20, bold=True)
        self._fonte_pergunta = pygame.font.SysFont(FONTE_NOME, 20, bold=True)
        self._fonte_fim_titulo = pygame.font.SysFont(FONTE_NOME, 28, bold=True)
        self._fonte_fim_sub = pygame.font.SysFont(FONTE_NOME, 16)

        # Criação do Quadro Interativo (no centro da sala, mais ao topo)
        self.quadro_rect = pygame.Rect(LARGURA // 2 - 100, 100, 200, 100)

        # Controle de Estado da Prova
        self.exibindo_prova = False
        self.prova_encerrada = False
        self.idx_atual = 0
        self.botoes_alternativas = []

        self._inicializar_questoes()

    def _inicializar_questoes(self):
        self.questoes = [
            PerguntaFacil(
                ["A) Pygame", "B) C++", "C) HTML", "D) Assembly"],
                enunciado="Qual biblioteca estamos usando para criar este jogo?",
                correta=0,
            ),
            PerguntaMedia(
                ["A) Perder pontos", "B) Mudar de cor", "C) Viagem no tempo", "D) Nada"],
                enunciado="O que acontece em 'One More Try' se atingir -30 pontos?",
                correta=2,
            ),
            PerguntaDificil(
                ["A) Polimorfismo", "B) Encapsulamento", "C) Herança", "D) Instanciação"],
                enunciado="Qual conceito de POO foi usado para reaproveitar a FaseBase?",
                correta=2,
            ),
        ]

    def _carregar_botoes_da_questao(self):
        self.botoes_alternativas.clear()
        if self.prova_encerrada: return
        
        questao = self.questoes[self.idx_atual]
        largura_b, altura_b = 500, 45
        # Centraliza os botões dentro do painel flutuante da prova
        x_botao = (LARGURA - largura_b) // 2
        y_inicial = 260
        espacamento = 12
        
        for i, texto_opcao in enumerate(questao.opcoes):
            y_botao = y_inicial + i * (altura_b + espacamento)
            self.botoes_alternativas.append(Botao(texto_opcao, x_botao, y_botao, largura_b, altura_b))

    def processar_eventos(self, eventos):
        for evento in eventos:
            if not self.exibindo_prova:
                # Enquanto a prova não abriu, o jogador não interage com o menu dela
                continue
                
            if self.prova_encerrada:
                if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    if self.jogador.pontuacao <= PONTUACAO_GAME_OVER:
                        self.game.trocar_cena(TelaQuarto(self.game))
                    else:
                        from main import TelaInicial
                        self.game.trocar_cena(TelaInicial(self.game))
                continue
                
            # Interação com os botões das alternativas
            questao = self.questoes[self.idx_atual]
            for i, botao in enumerate(self.botoes_alternativas):
                if botao.clicado(evento):
                    if i == questao.correta:
                        self.jogador.pontuacao += questao.pontuacao_acerto
                    else:
                        self.jogador.pontuacao += questao.pontuacao_erro
                    
                    self.idx_atual += 1
                    if self.idx_atual >= len(self.questoes):
                        self.prova_encerrada = True
                    self._carregar_botoes_da_questao()

    def atualizar(self):
        if not self.exibindo_prova:
            # Se a prova NÃO está aberta, o PeLezin pode andar normalmente
            super().atualizar()
            
            # CHECAGEM DE COLISÃO: Se o PeLezin encostar no Quadro, a prova inicia!
            if self.jogador.rect.colliderect(self.quadro_rect):
                self.exibindo_prova = True
                self._carregar_botoes_da_questao()
        else:
            # Se a prova ESTÁ aberta, PeLezin fica parado e atualizamos apenas o hover dos botões
            if not self.prova_encerrada:
                pos_mouse = pygame.mouse.get_pos()
                for botao in self.botoes_alternativas:
                    botao.verificar_hover(pos_mouse)

    def desenhar(self, tela):
        # 1. DESENHA O SEGUNDO PLANO (Cenário da Sala e o Jogador andando ou parado)
        tela.fill(self.cor_fundo)
        
        # Desenha o Quadro na parede (preto com borda branca)
        pygame.draw.rect(tela, (20, 35, 20), self.quadro_rect)
        pygame.draw.rect(tela, (255, 255, 255), self.quadro_rect, width=3)
        
        # Escreve "PROVA AQUI" no quadro para guiar o jogador
        fonte_q = pygame.font.SysFont("arial", 18, bold=True)
        txt_quadro = fonte_q.render("QUADRO DA PROVA", True, (255, 255, 255))
        tela.blit(txt_quadro, txt_quadro.get_rect(center=self.quadro_rect.center))
        
        # Desenha o PeLezin (quadrado verde)
        pygame.draw.rect(tela, (0, 255, 0), self.jogador.rect)
        
        # Desenha o nome da fase no topo
        fonte_fase = pygame.font.SysFont("arial", 24, bold=True)
        texto_surf = fonte_fase.render(self.nome_fase, True, (255, 255, 255))
        tela.blit(texto_surf, (20, 20))
        
        # Mostra a Pontuação no topo superior direito
        fonte_hud = pygame.font.SysFont("arial", 20, bold=True)
        txt_pontos = fonte_hud.render(f"Pontuação: {self.jogador.pontuacao}", True, (255, 215, 0))
        tela.blit(txt_pontos, (LARGURA - txt_pontos.get_width() - 30, 20))

        # 2. DESENHA O PRIMEIRO PLANO (Pop-up/Overlay flutuante da Prova)
        if self.exibindo_prova:
            # Criamos uma superfície semi-transparente preta para escurecer de leve o fundo
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # O 150 controla a opacidade (0 transparente, 255 totalmente opaco)
            tela.blit(overlay, (0, 0))
            
            # Caixa flutuante centralizada onde as perguntas vão aparecer
            largura_p, altura_p = 650, 460
            x_painel = (LARGURA - largura_p) // 2
            y_painel = (ALTURA - altura_p) // 2
            
            # Fundo do painel da prova (Azul Escuro com borda dourada/branca)
            pygame.draw.rect(tela, (25, 45, 75), (x_painel, y_painel, largura_p, altura_p), border_radius=20)
            pygame.draw.rect(tela, (255, 255, 255), (x_painel, y_painel, largura_p, altura_p), width=3, border_radius=20)
            
            if self.prova_encerrada:
                self._desenhar_fim_da_prova(tela)
            else:
                # Texto de progresso das perguntas dentro da caixa
                txt_progresso = fonte_hud.render(f"Questão: {self.idx_atual + 1} / {len(self.questoes)}", True, (200, 220, 255))
                tela.blit(txt_progresso, (x_painel + 30, y_painel + 20))
                
                # Texto do Enunciado
                fonte_pergunta = pygame.font.SysFont("arial", 20, bold=True)
                txt_enunciado = fonte_pergunta.render(self.questoes[self.idx_atual].enunciado, True, (255, 255, 255))
                tela.blit(txt_enunciado, txt_enunciado.get_rect(center=(LARGURA // 2, y_painel + 90)))
                
                # Desenha as alternativas
                for botao in self.botoes_alternativas:
                    botao.desenhar(tela)

    def _desenhar_fim_da_prova(self, tela):
        fonte_tit = pygame.font.SysFont("arial", 28, bold=True)
        fonte_sub = pygame.font.SysFont("arial", 16)
        
        if self.jogador.pontuacao <= PONTUACAO_GAME_OVER:
            tit, sub, cor = "REPROVADO! O tempo está retrocedendo...", "Pressione qualquer tecla para viajar no tempo.", (255, 100, 100)
        else:
            tit, sub, cor = "APROVADO! Você superou o IFRN!", "Pressione qualquer tecla para voltar ao Menu Inicial.", (100, 255, 100)
            
        surf_tit = self._fonte_fim_titulo.render(tit, True, cor)
        surf_sub = self._fonte_fim_sub.render(sub, True, (230, 230, 230))
        tela.blit(surf_tit, surf_tit.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))
        tela.blit(surf_sub, surf_sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30)))