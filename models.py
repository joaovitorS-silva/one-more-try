import pygame
from settings import PONTOS_FACIL_ACERTO, PONTOS_MEDIO_ACERTO, PONTOS_DIFICIL_ACERTO
from settings import PONTOS_FACIL_ERRO, PONTOS_MEDIO_ERRO, PONTOS_DIFICIL_ERRO


# ── Personagens ───────────────────────────────────────────────────────────────
# TODO: candidata a virar classe abstrata (abc.ABC) quando Professor for usado de fato
class Personagem:
    def __init__(self, nome, velocidade, x, y):
        self.nome       = nome
        self.velocidade = velocidade
        self.x          = x
        self.y          = y


class Pelezin(Personagem):
    def __init__(self, estado_do_tempo, pontuacao, velocidade, x, y):
        super().__init__("PeLeZiN", velocidade, x, y)
        self.rect          = pygame.Rect(x, y, 33, 33)
        self.estado_do_tempo = estado_do_tempo  # ex: "sol", "chuva"
        self.pontuacao     = pontuacao


class Professor(Personagem):
    def __init__(self, velocidade, x, y, vida_maxima=100):
        super().__init__("Joaildo", velocidade, x, y)
        self.rect             = pygame.Rect(x, y, 32, 32)
        self.vida_atual       = vida_maxima
        self.vida_maxima      = vida_maxima
        self.direcao          = 1  # 1 = direita, -1 = esquerda
        self.x_min            = 100  # Limite esquerdo de patrulha
        self.x_max            = 700  # Limite direito de patrulha
        self.campo_visao_raio = 150  # Raio do campo de visão
    
    def atualizar(self, delta_time=1):
        """Atualiza posição do professor na patrulha."""
        self.rect.x += self.velocidade * self.direcao * delta_time
        
        # Inverte direção ao atingir limites
        if self.rect.x <= self.x_min or self.rect.x >= self.x_max:
            self.direcao *= -1
    
    def receber_dano(self, dano):
        """Diminui vida do professor."""
        self.vida_atual = max(0, self.vida_atual - dano)
    
    def recuperar_vida(self, quantidade):
        """Aumenta vida do professor (quando aluno erra)."""
        self.vida_atual = min(self.vida_maxima, self.vida_atual + quantidade)
    
    def esta_morto(self):
        """Retorna True se professor perdeu toda a vida."""
        return self.vida_atual <= 0


class NPC(Personagem):
    """NPC genérico e parado — usado pra personagens secundários que só
    conversam (mãe, colegas de turma, etc.), sem precisar criar uma classe
    nova pra cada um."""
    def __init__(self, nome, x, y, largura=32, altura=32):
        super().__init__(nome, 0, x, y)  # velocidade 0: esses NPCs não andam
        self.rect = pygame.Rect(x, y, largura, altura)


# ── Sistema de Questões ───────────────────────────────────────────────────────

class Questao:
    """Classe base para todas as questões da prova.

    enunciado e correta são obrigatórios no construtor — antes eram atribuídos
    por fora depois do `PerguntaFacil(...)`, então nada impedia esquecer de
    setar um dos dois e a questão quebrar (ou pior: rodar com correta=None)
    só quando o jogador clicasse numa alternativa.
    """
    def __init__(self, dificuldade, pontuacao_acerto, pontuacao_erro, opcoes, enunciado, correta):
        self.dificuldade      = dificuldade
        self.pontuacao_acerto = pontuacao_acerto
        self.pontuacao_erro   = pontuacao_erro
        self.opcoes           = opcoes  # lista de alternativas A-D
        self.enunciado        = enunciado
        self.correta          = correta  # índice (0-3) da alternativa correta em `opcoes`

        if not (0 <= correta < len(opcoes)):
            raise ValueError(f"'correta'={correta} fora do intervalo de opções (0-{len(opcoes) - 1})")


class PerguntaFacil(Questao):
    def __init__(self, opcoes, enunciado, correta):
        super().__init__("facil", PONTOS_FACIL_ACERTO, PONTOS_FACIL_ERRO, opcoes, enunciado, correta)


class PerguntaMedia(Questao):
    def __init__(self, opcoes, enunciado, correta):
        super().__init__("media", PONTOS_MEDIO_ACERTO, PONTOS_MEDIO_ERRO, opcoes, enunciado, correta)


class PerguntaDificil(Questao):
    def __init__(self, opcoes, enunciado, correta):
        super().__init__("dificil", PONTOS_DIFICIL_ACERTO, PONTOS_DIFICIL_ERRO, opcoes, enunciado, correta)


# ── Prova ─────────────────────────────────────────────────────────────────────

class Prova:
    def __init__(self, questoes):
        self.questoes       = questoes  # lista de objetos Questao
        self.pontuacao_total = 0

    def responder(self, questao, acertou):
        if acertou:
            self.pontuacao_total += questao.pontuacao_acerto
        else:
            self.pontuacao_total += questao.pontuacao_erro