import pygame
from settings import PONTOS_FACIL_ACERTO, PONTOS_MEDIO_ACERTO, PONTOS_DIFICIL_ACERTO
from settings import PONTOS_FACIL_ERRO, PONTOS_MEDIO_ERRO, PONTOS_DIFICIL_ERRO


# ── Personagens ───────────────────────────────────────────────────────────────
#possivel classe abstrata)()()()9
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
    def __init__(self, estado_emocional, velocidade, x, y):
        super().__init__("Joaildo", velocidade, x, y)
        self.rect             = pygame.Rect(x, y, 32, 32)
        self.estado_emocional = estado_emocional  # False = normal | True = raiva


# ── Sistema de Questões ───────────────────────────────────────────────────────

class Questao:
    """Classe base para todas as questões da prova."""
    def __init__(self, dificuldade, pontuacao_acerto, pontuacao_erro, opcoes):
        self.dificuldade      = dificuldade
        self.pontuacao_acerto = pontuacao_acerto
        self.pontuacao_erro   = pontuacao_erro
        self.opcoes           = opcoes  # lista de alternativas A-D


class PerguntaFacil(Questao):
    def __init__(self, opcoes):
        super().__init__("facil", PONTOS_FACIL_ACERTO, PONTOS_FACIL_ERRO, opcoes)


class PerguntaMedia(Questao):
    def __init__(self, opcoes):
        super().__init__("media", PONTOS_MEDIO_ACERTO, PONTOS_MEDIO_ERRO, opcoes)


class PerguntaDificil(Questao):
    def __init__(self, opcoes):
        super().__init__("dificil", PONTOS_DIFICIL_ACERTO, PONTOS_DIFICIL_ERRO, opcoes)


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
