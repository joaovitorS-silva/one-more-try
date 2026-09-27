"""Navegação real pelo chão do quarto com o fundo ilustrado."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from collections import defaultdict
from unittest.mock import patch
import pygame
from jogo.game import Game
from jogo.cenas.cena import TelaQuarto, TelaCozinha


class QuartoTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.nova_partida()
        self.game.dt = 1 / 60
        self.quarto = self.game.cena_atual

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def mover(self, tecla, quadros):
        with patch('pygame.key.get_pressed', return_value=defaultdict(bool, {tecla: True})):
            for _ in range(quadros):
                self.quarto.atualizar()
                self.assertTrue(self.quarto.area_caminhada.contains(self.quarto.jogador.rect))
                self.assertFalse(any(self.quarto.jogador.rect.colliderect(o) for o in self.quarto.obstaculos))

    def test_limites_e_mobilia(self):
        self.mover(pygame.K_w, 100)
        self.assertEqual(self.quarto.jogador.rect.top, 462)
        self.mover(pygame.K_s, 100)
        self.assertEqual(self.quarto.jogador.rect.bottom, 512)
        self.mover(pygame.K_a, 300)
        self.assertEqual(self.quarto.jogador.rect.left, 16)
        self.mover(pygame.K_d, 400)
        self.assertEqual(self.quarto.jogador.rect.right, 784)
        self.game.dt = 0.05
        self.mover(pygame.K_w, 100)
        self.assertEqual(self.quarto.jogador.rect.top, 480)

    def test_todos_os_alvos_acessiveis_pelo_chao(self):
        for objeto in (self.quarto.relogio, self.quarto.fliperama, self.quarto.porta, self.quarto.escrivaninha):
            self.quarto.jogador.rect.topleft = (130, 484)
            alvo_x = objeto.area_interacao.centerx
            for _ in range(250):
                distancia = alvo_x - self.quarto.jogador.rect.centerx
                if abs(distancia) <= 3:
                    break
                self.mover(pygame.K_d if distancia > 0 else pygame.K_a, 1)
            self.assertTrue(self.quarto.perto(objeto))
            self.assertIs(self.quarto.alvo()[0], objeto)

    def test_porta_e_volta_em_posicao_segura(self):
        self.mover(pygame.K_d, 111)
        self.quarto.processar_eventos([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])
        self.assertIsInstance(self.game.cena_atual, TelaCozinha)
        cozinha = self.game.cena_atual
        cozinha.ir(TelaQuarto, True)
        self.quarto = self.game.cena_atual
        self.assertTrue(self.quarto.area_caminhada.contains(self.quarto.jogador.rect))
        self.mover(pygame.K_s, 3)

    def test_clique_no_movel_so_funciona_de_perto(self):
        fliperama = self.quarto.fliperama
        clique = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=fliperama.rect.center)
        self.quarto.processar_eventos([clique])
        self.assertIsNone(self.quarto.desafio)
        self.mover(pygame.K_d, 74)
        self.quarto.processar_eventos([clique])
        self.assertTrue(self.quarto.desafio.ativo)
        antes = self.quarto.jogador.rect.copy()
        self.mover(pygame.K_d, 10)
        self.assertEqual(self.quarto.jogador.rect, antes)
