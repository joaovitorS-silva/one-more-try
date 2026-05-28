import pygame
from botoes_tela_inicial import Botao

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('One More Try')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

bx = LARGURA // 2 - 150
botoes = [
    Botao("Jogar",  bx, 120, 300, 60),
    Botao("Opções", bx, 200, 300, 60),
    Botao("Sair",   bx, 280, 300, 60),
]

rodando = True
while rodando:
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        for botao in botoes:
            if botao.clicado(evento):
                if botao.texto == "Jogar":
                    print("Iniciando jogo...")
                elif botao.texto == "Opções":
                    print("Abrindo opções...")
                elif botao.texto == "Sair":
                    pygame.quit()
                    quit()

    tela.fill(PRETO)

  
    for botao in botoes:
        botao.verificar_hover(pos_mouse)
        botao.desenhar(tela)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

