import pygame
from models import BotoesInit 

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('One More Try')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60
botao = BotoesInit(100,200,(255,0,0),300,200)
rodando = True
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False


     
     
    
    botao.desenhar(tela)
    


    pygame.display.flip()
    clock.tick(FPS)
    tela.fill(PRETO)

pygame.quit()







pygame.display.init()
pygame.display.get_init()