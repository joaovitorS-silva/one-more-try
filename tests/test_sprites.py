"""Folha real do personagem e estado de animação independente da renderização."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
import pygame
from jogo.models import Pelezin
from jogo.sistemas.sprites import GerenciadorSprites


class SpritesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_folha_tem_dezesseis_poses_completas(self):
        sprites = GerenciadorSprites()
        poses = sprites.carregar_personagem()
        self.assertEqual(set(poses), {'baixo', 'cima', 'esquerda', 'direita'})
        tela = pygame.Surface((100, 100), pygame.SRCALPHA)
        for direcao, quadros in poses.items():
            self.assertEqual(len(quadros), 4)
            for i, imagem in enumerate(quadros):
                self.assertGreater(imagem.get_height(), 240)
                self.assertLess(imagem.get_height(), 270)
                self.assertLess(imagem.get_width(), 150)
                tela.fill((0, 0, 0, 0))
                sprites.desenhar(tela, 'pelezin', pygame.Rect(30, 40, 33, 33), (0, 255, 0), direcao, i)
                self.assertGreater(tela.get_bounding_rect().height, 45)
                self.assertLessEqual(tela.get_bounding_rect().bottom, 73)

    def test_movimento_direcao_parada_e_colisao(self):
        jogador = Pelezin('sol', 0, 5, 50, 50)
        for movimento, direcao in [((5, 0), 'direita'), ((-5, 0), 'esquerda'), ((0, -5), 'cima'), ((0, 5), 'baixo')]:
            jogador.atualizar_animacao(movimento, 0.13)
            self.assertEqual(jogador.direcao, direcao)
            self.assertIn(jogador.quadro_animacao, (1, 2, 3))
            jogador.atualizar_animacao((0, 0), 0.13)
            self.assertEqual(jogador.quadro_animacao, 0)
            self.assertEqual(jogador.direcao, direcao)
        self.assertEqual(jogador.rect.size, (33, 33))
