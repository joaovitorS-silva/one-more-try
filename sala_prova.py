"""
Fase da Sala de Prova (Nova) - onde o professor é o alvo.
O professor patrulha a sala, e o aluno tenta "derrotar" o professor
acertando as questões (que causam dano), enquanto errar faz o professor
recuperar vida.

Inclui: campo de visão do professor, mesa, cadeiras, barra de vida.
"""
import pygame
from settings import (
    LARGURA, ALTURA, FONTE_NOME, BRANCO, COR_FUNDO_SALA, COR_PAINEL_PROVA,
)
from models import Professor, PerguntaFacil, PerguntaMedia, PerguntaDificil
from botoes_tela_inicial import Botao
from dialogo import GerenciadorDialogo
from objetos_cenarios import Chao, Porta
from sala_prova_objetos import (
    MesaProfessor, CadeiraAluno, CampoVisaoProfessor, BarraVidaProfessor
)
from cena import FaseBase


class TelaSalaProva(FaseBase):
    """Sala de prova onde o professor patrulha e o aluno faz a prova.
    
    Dinâmica:
    - Professor anda pela sala com campo de visão visível
    - Aluno acerta questão → causa dano ao professor
    - Aluno erra questão → professor recupera vida
    - Quando professor morre (vida=0) → aluno vence
    - Quando acabam as questões → resultado final
    """
    
    usa_transicao_automatica = False
    
    def __init__(self, game):
        super().__init__(game, COR_FUNDO_SALA, "5. Sala de Prova")
        
        # Diálogos
        self._inicializar_dialogo()
        
        # Fontes
        self._fonte_rotulo = pygame.font.SysFont(FONTE_NOME, 14, bold=True)
        self._fonte_hud = pygame.font.SysFont(FONTE_NOME, 18, bold=True)
        self._fonte_pergunta = pygame.font.SysFont(FONTE_NOME, 18, bold=True)
        self._fonte_fim_titulo = pygame.font.SysFont(FONTE_NOME, 28, bold=True)
        self._fonte_fim_sub = pygame.font.SysFont(FONTE_NOME, 16)
        
        # Chão
        self.chao = Chao(y=480, largura=LARGURA, altura=120, cor=(40, 60, 100))
        
        # Porta (para sair da sala)
        self.porta = Porta(x=50, y=250, largura=50, altura=120)
        
        # Professor com vida e movimento
        # velocidade, x, y, vida_maxima
        self.professor = Professor(velocidade=2, x=LARGURA // 2, y=150, vida_maxima=100)
        
        # Campo de visão do professor
        self.campo_visao = CampoVisaoProfessor(self.professor.rect, raio=150)
        
        # Barra de vida (HUD)
        self.barra_vida = BarraVidaProfessor(
            x=LARGURA // 2 - 200,
            y=10,
            largura=400,
            altura=30
        )
        
        # Objetos de cenário
        self.mesa_professor = MesaProfessor(LARGURA - 220, 60)
        
        # Cadeiras dos alunos (espalhadas pela sala)
        self.cadeiras = [
            CadeiraAluno(200, 280),
            CadeiraAluno(280, 280),
            CadeiraAluno(360, 280),
            CadeiraAluno(440, 280),
            CadeiraAluno(520, 280),
            CadeiraAluno(600, 280),
            CadeiraAluno(200, 380),
            CadeiraAluno(280, 380),
            CadeiraAluno(360, 380),
            CadeiraAluno(440, 380),
            CadeiraAluno(520, 380),
            CadeiraAluno(600, 380),
        ]
        
        # Estado da prova
        self.exibindo_prova = False
        self.prova_encerrada = False
        self.idx_atual = 0
        self.botoes_alternativas = []
        
        self._inicializar_questoes()
    
    def _inicializar_dialogo(self):
        """Cria o diálogo inicial com o professor."""
        linhas = [
            "PeLezin: Professor, eu vim pra fazer a prova.",
            "Prof. Joaildo: Então vamos lá. Você vai enfrentar desafios nesta sala!",
        ]
        self.dialogo = GerenciadorDialogo(linhas)
    
    def _inicializar_questoes(self):
        """Define o banco de questões."""
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
        """Cria os botões de alternativas para a questão atual."""
        self.botoes_alternativas.clear()
        if self.prova_encerrada:
            return
        
        questao = self.questoes[self.idx_atual]
        largura_b, altura_b = 500, 45
        x_botao = (LARGURA - largura_b) // 2
        y_inicial = 260
        espacamento = 12
        
        for i, texto_opcao in enumerate(questao.opcoes):
            y_botao = y_inicial + i * (altura_b + espacamento)
            self.botoes_alternativas.append(Botao(texto_opcao, x_botao, y_botao, largura_b, altura_b))
    
    def processar_eventos(self, eventos):
        """Processa eventos do teclado e mouse."""
        for evento in eventos:
            # Diálogo ativo
            if self.dialogo.ativo:
                if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    if not self.dialogo.proximo():  # Se acabou
                        self.exibindo_prova = True
                        self._carregar_botoes_da_questao()
                continue
            
            # Prova ainda não aberta: ignorar clicks
            if not self.exibindo_prova:
                continue
            
            # Prova encerrada: volta para outra cena
            if self.prova_encerrada:
                if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    if self.professor.esta_morto():
                        # Professor foi derrotado → tela de vitória
                        from main import TelaInicial
                        self.game.trocar_cena(TelaInicial(self.game))
                    else:
                        # Aluno não conseguiu → volta ao quarto
                        from cena import TelaQuarto
                        self.game.trocar_cena(TelaQuarto(self.game))
                continue
            
            # Clique na porta durante a prova
            if self.porta.clicado(evento):
                self.prova_encerrada = True
                continue
            
            # Prova ativa: processar cliques nos botões
            questao = self.questoes[self.idx_atual]
            for i, botao in enumerate(self.botoes_alternativas):
                if botao.clicado(evento):
                    if i == questao.correta:
                        # Acertou! Professor recebe dano
                        dano = questao.pontuacao_acerto  # Ex: 5, 10, 20
                        self.professor.receber_dano(dano)
                    else:
                        # Errou! Professor recupera vida
                        recuperacao = abs(questao.pontuacao_erro)  # Ex: 15, 10, 5
                        self.professor.recuperar_vida(recuperacao)
                    
                    # Próxima questão
                    self.idx_atual += 1
                    if self.idx_atual >= len(self.questoes):
                        self.prova_encerrada = True
                    self._carregar_botoes_da_questao()
                    break
    
    def atualizar(self):
        """Atualiza lógica da cena."""
        # Diálogo ativo → nada muda
        if self.dialogo.ativo:
            return
        
        # Prova não iniciada → jogador pode andar
        if not self.exibindo_prova:
            super().atualizar()
            
            # Colisão com professor → inicia diálogo
            if self.jogador.rect.colliderect(self.professor.rect):
                self.dialogo.iniciar()
        else:
            # Prova ativa → atualizar professor e botões
            if not self.prova_encerrada:
                # Professor patrulha
                self.professor.atualizar()
                self.campo_visao.professor_rect = self.professor.rect
                
                # Atualizar hover dos botões
                pos_mouse = pygame.mouse.get_pos()
                for botao in self.botoes_alternativas:
                    botao.verificar_hover(pos_mouse)
    
    def desenhar(self, tela):
        """Renderiza a tela."""
        # Fundo
        tela.fill(self.cor_fundo)
        
        # Chão
        self.chao.desenhar(tela)
        
        # Objetos de cenário
        self.mesa_professor.desenhar(tela, self._fonte_rotulo)
        for cadeira in self.cadeiras:
            cadeira.desenhar(tela)
        self.porta.desenhar(tela, self._fonte_rotulo)
        
        # Professor
        pygame.draw.rect(tela, (200, 100, 40), self.professor.rect)
        pygame.draw.rect(tela, (255, 255, 255), self.professor.rect, width=2)
        txt_prof = self._fonte_rotulo.render(f"Prof. {self.professor.nome}", True, BRANCO)
        tela.blit(txt_prof, txt_prof.get_rect(midbottom=(
            self.professor.rect.centerx, self.professor.rect.top - 4
        )))
        
        # Campo de visão do professor (visível sempre para o jogador ver)
        self.campo_visao.desenhar(tela)
        
        # PeLezin
        pygame.draw.rect(tela, (0, 255, 0), self.jogador.rect)
        
        # Nome da fase
        texto_surf = self._fonte_hud.render(self.nome_fase, True, BRANCO)
        tela.blit(texto_surf, (20, ALTURA - 30))
        
        # Barra de vida do professor (HUD)
        self.barra_vida.desenhar(tela, self._fonte_rotulo, 
                                  self.professor.vida_atual, 
                                  self.professor.vida_maxima)
        
        # Diálogo se ativo
        if self.dialogo.ativo:
            self.dialogo.desenhar(tela)
        
        # Prova se ativa
        if self.exibindo_prova:
            self._desenhar_prova(tela)
    
    def _desenhar_prova(self, tela):
        """Renderiza o painel flutuante da prova."""
        # Overlay semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        tela.blit(overlay, (0, 0))
        
        # Caixa flutuante centralizada
        largura_p, altura_p = 650, 460
        x_painel = (LARGURA - largura_p) // 2
        y_painel = (ALTURA - altura_p) // 2
        
        pygame.draw.rect(tela, COR_PAINEL_PROVA, (x_painel, y_painel, largura_p, altura_p), border_radius=20)
        pygame.draw.rect(tela, (255, 255, 255), (x_painel, y_painel, largura_p, altura_p), width=3, border_radius=20)
        
        if self.prova_encerrada:
            self._desenhar_fim_prova(tela, x_painel, y_painel)
        else:
            self._desenhar_questao(tela, x_painel, y_painel)
    
    def _desenhar_questao(self, tela, x_painel, y_painel):
        """Renderiza a questão e alternativas."""
        # Progresso
        txt_prog = self._fonte_hud.render(
            f"Questão: {self.idx_atual + 1} / {len(self.questoes)}",
            True, (200, 220, 255)
        )
        tela.blit(txt_prog, (x_painel + 30, y_painel + 20))
        
        # Enunciado
        txt_enum = self._fonte_pergunta.render(
            self.questoes[self.idx_atual].enunciado,
            True, (255, 255, 255)
        )
        tela.blit(txt_enum, txt_enum.get_rect(center=(LARGURA // 2, y_painel + 90)))
        
        # Botões
        for botao in self.botoes_alternativas:
            botao.desenhar(tela)
    
    def _desenhar_fim_prova(self, tela, x_painel, y_painel):
        """Renderiza a tela de resultado final."""
        if self.professor.esta_morto():
            tit = "VITÓRIA! Você derrotou o Professor!"
            sub = "Pressione qualquer tecla para voltar."
            cor = (100, 255, 100)
        else:
            tit = "DERROTA! O Professor venceu!"
            sub = "Pressione qualquer tecla para voltar ao quarto."
            cor = (255, 100, 100)
        
        surf_tit = self._fonte_fim_titulo.render(tit, True, cor)
        surf_sub = self._fonte_fim_sub.render(sub, True, (230, 230, 230))
        
        tela.blit(surf_tit, surf_tit.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))
        tela.blit(surf_sub, surf_sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30)))
