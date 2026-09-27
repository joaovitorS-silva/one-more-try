"""Fluxo da sala explorável até a prova e retorno ao pátio."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from collections import defaultdict
from unittest.mock import patch
import pygame
from jogo.game import Game
from jogo.cenas.cena import TelaCorredor
from jogo.cenas.sala_prova import TelaSalaProva


def tecla(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


class SalaTest(unittest.TestCase):
    def setUp(self):
        # Fontes em cache não sobrevivem ao pygame.quit() de outras suítes.
        from jogo.ui import botoes_tela_inicial
        botoes_tela_inicial._fonte = None
        self.game = Game()
        self.game.dt = 0.05
        self.sala = TelaSalaProva(self.game)
        self.game.trocar_cena(self.sala)

    def tearDown(self):
        pygame.quit()

    def test_entrada_carteira_cancelamento_e_inicio(self):
        sala = self.sala
        sala.processar_eventos([tecla(pygame.K_1)])
        for _ in range(100):
            sala.atualizar()
        self.assertIsNone(sala.prova)
        self.assertEqual(sala.restante, 90)
        sala.jogador.rect.midtop = (sala.carteira.rect.centerx, sala.carteira.rect.bottom + 5)
        antes = sala.jogador.rect.copy()
        sala.processar_eventos([tecla(pygame.K_e), tecla(pygame.K_1)])
        self.assertTrue(sala.escolhendo)
        self.assertIsNone(sala.prova)
        sala.desenhar(self.game.tela)
        sala.atualizar()
        self.assertEqual(sala.restante, 90)
        sala.processar_eventos([tecla(pygame.K_BACKSPACE)])
        self.assertFalse(sala.escolhendo)
        self.assertEqual(sala.jogador.rect, antes)
        sala.processar_eventos([tecla(pygame.K_e)])
        sala.processar_eventos([tecla(pygame.K_2)])
        self.assertIsNotNone(sala.prova)
        self.assertEqual(len(sala.prova.respondidas), 0)
        sala.atualizar()
        self.assertLess(sala.restante, 90)
        sala.responder(sala.questoes[0].correta)
        sala.responder(sala.questoes[0].correta)
        self.assertEqual(len(sala.prova.respondidas), 1)

    def test_porta_retorna_e_preserva_missao(self):
        self.game.progresso.missao_ana = 'encontradas'
        self.sala.jogador.rect.midleft = (self.sala.volta.rect.right + 5, self.sala.volta.rect.centery)
        self.sala.processar_eventos([tecla(pygame.K_e)])
        self.assertIsInstance(self.game.cena_atual, TelaCorredor)
        self.assertEqual(self.game.progresso.missao_ana, 'encontradas')
        patio = self.game.cena_atual
        patio.jogador.rect.center = patio.saida.rect.center
        patio.processar_eventos([tecla(pygame.K_e)])
        self.assertIsInstance(self.game.cena_atual, TelaSalaProva)
        self.assertIsNone(self.game.cena_atual.prova)

    def test_colisoes_movimento_e_dialogo(self):
        sala = self.sala
        sala.jogador.rect.midright = (sala.cadeiras[0].rect.left - 1, sala.cadeiras[0].rect.centery)
        teclas = defaultdict(bool, {pygame.K_d: True})
        with patch('pygame.key.get_pressed', return_value=teclas):
            sala.atualizar()
        self.assertEqual(sala.jogador.rect.right, sala.cadeiras[0].rect.left)
        sala.jogador.rect.topleft = (100, 330)
        with patch('pygame.key.get_pressed', return_value=teclas):
            sala.atualizar()
        self.assertGreater(sala.jogador.rect.x, 100)
        sala.jogador.rect.center = sala.colegas[0].rect.center
        sala.processar_eventos([tecla(pygame.K_e)])
        self.assertTrue(sala.dialogo.ativo)
        with patch('pygame.key.get_pressed', side_effect=AssertionError('Movimento durante diálogo')):
            sala.atualizar()
        sala.desenhar(self.game.tela)
        sala.processar_eventos([tecla(pygame.K_1)])
        self.assertIsNone(sala.prova)

    def test_professor_reconhecido_no_ciclo(self):
        self.game.tentativa = 2
        self.sala.jogador.rect.center = self.sala.professor.rect.center
        self.sala.processar_eventos([tecla(pygame.K_e)])
        self.assertIn('professor_ciclo', self.game.progresso.memorias)
        self.assertTrue(self.sala.dialogo.ativo)

    def test_grade_mouse_dica_e_feedback(self):
        sala = self.sala
        sala.sentar()
        sala.processar_eventos([pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=sala.botoes_assuntos[1].rect.center)])
        self.assertEqual(sala.assunto, 'Matemática')
        sala.loja.creditos = 5
        sala.processar_eventos([tecla(pygame.K_h)])
        eliminada = sala.eliminadas[0]
        sala.processar_eventos([pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=sala.botoes_alternativas[eliminada].rect.center)])
        self.assertEqual(len(sala.prova.respondidas), 0)
        correta = sala.questoes[0].correta
        clique = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=sala.botoes_alternativas[correta].rect.center)
        sala.processar_eventos([clique, clique])
        self.assertEqual(sala.selecionada, correta)
        self.assertEqual(len(sala.prova.respondidas), 1)
        sala.desenhar(self.game.tela)
        self.game.dt = 1.4
        sala.atualizar()
        self.assertIsNone(sala.selecionada)
        self.assertEqual(sala.eliminadas, [])
        self.assertEqual(sala.idx_atual, 1)
        sala.desenhar(self.game.tela)

    def test_textos_do_banco_cabem_sem_corte(self):
        from jogo.sistemas.banco_perguntas import carregar_todas_as_questoes
        from jogo.ui.prova import ajustar_texto
        for questoes in carregar_todas_as_questoes().values():
            for questao in questoes:
                caixas = [(questao.enunciado, 752, 52, 23)]
                caixas += [(opcao, 311, 38, 18) for opcao in questao.opcoes]
                caixas += [(f'-15 pontos. Correta: {questao.opcoes[questao.correta]}', 752, 35, 17)]
                for mensagem, largura, altura, tamanho in caixas:
                    with self.subTest(mensagem=mensagem):
                        fonte, linhas = ajustar_texto(mensagem, largura, altura, tamanho)
                        self.assertLessEqual(len(linhas) * fonte.get_linesize(), altura)
                        self.assertTrue(all(fonte.size(linha)[0] <= largura for linha in linhas))
