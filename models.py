import pygame
class Personagem():
    def __init__(self,nome,velocidade, x, y):
        self.nome = nome
        self.velocidade = velocidade

class Pelezin(Personagem):
    def __init__(self, estado_do_tempo,  pontuacao, velocidade, x, y):
        super().__init__("PeLeZiN",velocidade, x,y)
        self.rect = pygame.rect #colocar parametros (x e y,33,33)
        self.estado_do_tempo = estado_do_tempo
        self.pontuacao = pontuacao


class Professor(Personagem):
    #o estado emocional vai ser raiva e "normal"
    def __init__(self, estado_emocional, x,y , velocidade):
        super().__init__("joaildo" , velocidade, x,y)
        self.estado_emocional =    estado_emocional   # false or True
        self.rect =pygame.rect
         #colocar parametros (x e y, 32,32)
    
        

class Prova():
    def __init__(self,quantidade_questoes, dificuldade_questoes, opcoes, pontucao_total): #A ate D
        self.quantidade_questoes = quantidade_questoes
        self.dificuldade_questoes = dificuldade_questoes
        self.opcoes = opcoes
        self.potuacao_final = pontucao_total

class questoes(): #classe pai das questoes (facil, media, dificil)
    def __init__(self, dificuldade_perguntas,pontucao_perguntas, opcoes_perguntas):
        self.dificuldade_perguntas = dificuldade_perguntas
        self.pontucao_perguntas = pontucao_perguntas
        self.opcoes_perguntas = opcoes_perguntas
        
class Perguntas_Faceis(questoes):
    def __init__(self,dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas):
        super().__init__(dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas)
  
class PErguntas_Medias(questoes):
    def __init__(self,dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas):
        super().__init__(dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas)
  
class Perguntas_Dificeis(questoes):
    def __init__(self,dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas):
        super().__init__(dificuldade_perguntas, pontucao_perguntas, opcoes_perguntas)
  

class BotoesInit():
    def __init__(self, x, y, cor , largura , altura):
        self.x = x
        self.y = y
        self.cor = cor
        self.largura = largura
        self.altura = altura
       
        
    def desenhar(self, tela):

        retangulo =  pygame.Rect(self.x, self.y,self.largura,self.altura)
        pygame.draw.rect(tela,(255,0,0), retangulo)
        
    



























