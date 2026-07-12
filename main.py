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


     
     
    
    
    


    pygame.display.flip()
    clock.tick(FPS)
    tela.fill(PRETO)

pygame.quit()





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


class Game:
    """Gerenciador principal do jogo — controla o loop e as cenas."""

    def __init__(self):
        pygame.init()
        self.tela       = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock      = pygame.time.Clock()
        self.rodando    = True
        self.cena_atual = None
        pygame.display.set_caption(TITULO)

    def trocar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def executar(self):
        self.trocar_cena(TelaInicial(self))

        while self.rodando:
            eventos = pygame.event.get()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.sair()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.sair()

            self.cena_atual.processar_eventos(eventos)
            self.cena_atual.atualizar()

            self.tela.fill(PRETO)
            self.cena_atual.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(FPS)

    def sair(self):
        self.rodando = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().executar()
