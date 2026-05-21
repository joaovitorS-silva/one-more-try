import pygame
#linha teste(()#(*$@)#(*$)(@#*$)(@#*))
pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('One More Try')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

rodando = True
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False


    tela.fill(PRETO)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()