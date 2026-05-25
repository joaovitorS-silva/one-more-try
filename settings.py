import pygame

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

    botao_jogar = pygame.Rect(300, 255, 200, 50) 
    pygame.draw.rect(tela,(255,0,0) ,botao_jogar)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

