"""Percurso da missão, memórias, desafios e bloqueio de entrada pelo caderno."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from unittest.mock import patch
import pygame
from jogo.game import Game
from jogo.cenas.cena import TelaQuarto, TelaCozinha, TelaRua, TelaCorredor
from jogo.cenas.sala_prova import TelaSalaProva
from jogo.cenas.finais import TelaViagemTempo, TelaVoltaCorredor, TelaRuaVolta, TelaCelebracao
from jogo.ui.caderno import desenhar_caderno


def tecla(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


class ExpansaoTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.nova_partida()
        self.game.dt = 1 / 60

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def interagir(self, cena, objeto):
        cena.jogador.rect.center = getattr(objeto, 'area_interacao', objeto.rect).center
        cena.processar_eventos([tecla(pygame.K_e)])

    def fechar_dialogo(self, cena):
        while cena.dialogo.ativo:
            cena.processar_eventos([tecla(pygame.K_RETURN)])

    def test_missao_com_ida_e_volta_e_recompensa_unica(self):
        patio = TelaCorredor(self.game)
        self.game.trocar_cena(patio)
        self.interagir(patio, patio.colegas[0])
        self.assertEqual(self.game.progresso.missao_ana, 'procurando')
        self.fechar_dialogo(patio)
        self.interagir(patio, patio.volta)
        rua = self.game.cena_atual
        self.assertIsInstance(rua, TelaRua)
        self.interagir(rua, rua.anotacoes)
        self.assertNotIn(rua.anotacoes, rua.objetos)
        self.fechar_dialogo(rua)
        self.interagir(rua, rua.saida)
        patio = self.game.cena_atual
        self.interagir(patio, patio.colegas[0])
        self.assertEqual(self.game.progresso.missao_ana, 'concluida')
        self.fechar_dialogo(patio)
        self.interagir(patio, patio.colegas[0])
        self.fechar_dialogo(patio)
        self.interagir(patio, patio.saida)
        sala = self.game.cena_atual
        sala.iniciar_prova('Matemática')
        self.assertEqual(sala.loja.creditos, 5)
        sala.processar_eventos([tecla(pygame.K_h)])
        self.assertEqual(sala.loja.creditos, 0)
        self.assertEqual(len(sala.eliminadas), 1)
        self.assertEqual(sala.prova.pontuacao_total, 0)

    def test_coleta_antes_de_conhecer_ana_e_ausencia_ao_revisitar(self):
        rua = TelaRua(self.game)
        self.interagir(rua, rua.anotacoes)
        outra_rua = TelaRua(self.game)
        self.assertNotIn(outra_rua.anotacoes, outra_rua.objetos)
        patio = TelaCorredor(self.game)
        self.interagir(patio, patio.colegas[0])
        self.assertEqual(self.game.progresso.missao_ana, 'concluida')

    def test_reinicio_preserva_memorias_mas_reinicia_missao(self):
        self.game.registrar('teste', 'Uma descoberta', 'Persistente entre tentativas.')
        self.game.progresso.missao_ana = 'concluida'
        viagem = TelaViagemTempo(self.game, 'Teste')
        self.game.dt = 4
        viagem.atualizar()
        self.assertEqual(self.game.tentativa, 2)
        self.assertIn('teste', self.game.progresso.memorias)
        self.assertEqual(self.game.progresso.missao_ana, 'desconhecida')
        sala = TelaSalaProva(self.game)
        sala.iniciar_prova('POO e Python')
        self.assertEqual(sala.loja.creditos, 0)
        self.game.nova_partida()
        self.assertEqual(self.game.progresso.memorias, {})

    def test_desafios_erro_acerto_e_saida_sem_recompensa_duplicada(self):
        quarto = self.game.cena_atual
        for objeto, errada, correta, memoria in [(quarto.escrivaninha, pygame.K_2, pygame.K_1, 'estudo'), (quarto.fliperama, pygame.K_1, pygame.K_3, 'sequencia')]:
            self.interagir(quarto, objeto)
            quarto.processar_eventos([tecla(errada)])
            self.assertNotIn(memoria, self.game.progresso.memorias)
            quarto.processar_eventos([tecla(correta)])
            self.assertIn(memoria, self.game.progresso.memorias)
            quantidade = len(self.game.progresso.memorias)
            quarto.processar_eventos([tecla(correta)])
            self.assertEqual(len(self.game.progresso.memorias), quantidade)
            quarto.desenhar(self.game.tela)
            quarto.processar_eventos([tecla(pygame.K_RETURN)])
            self.assertFalse(quarto.desafio.ativo)

    def test_relogio_mae_e_ana_reagem_a_segunda_tentativa(self):
        quarto = self.game.cena_atual
        self.interagir(quarto, quarto.relogio)
        self.assertNotIn('relogio_repetido', self.game.progresso.memorias)
        self.game.reiniciar_manha()
        quarto = self.game.cena_atual
        self.interagir(quarto, quarto.relogio)
        self.assertIn('relogio_repetido', self.game.progresso.memorias)
        cozinha = TelaCozinha(self.game)
        self.interagir(cozinha, cozinha.mae)
        self.assertIn('mae_repeticao', self.game.progresso.memorias)
        patio = TelaCorredor(self.game)
        self.interagir(patio, patio.colegas[0])
        self.assertIn('ana_ciclo', self.game.progresso.memorias)

    def test_portas_retornam_sem_transicao_em_cascata(self):
        quarto = self.game.cena_atual
        quarto.processar_eventos([tecla(pygame.K_e)])
        self.assertIs(self.game.cena_atual, quarto)
        self.interagir(quarto, quarto.porta)
        cozinha = self.game.cena_atual
        self.interagir(cozinha, cozinha.volta)
        self.assertIsInstance(self.game.cena_atual, TelaQuarto)
        self.game.cena_atual.atualizar()
        self.assertIsInstance(self.game.cena_atual, TelaQuarto)
        cozinha = TelaCozinha(self.game)
        self.interagir(cozinha, cozinha.porta)
        rua = self.game.cena_atual
        self.interagir(rua, rua.volta)
        self.assertIsInstance(self.game.cena_atual, TelaCozinha)

    def test_dialogo_e_desafio_bloqueiam_movimento(self):
        quarto = self.game.cena_atual
        quarto.estudar()
        antes = quarto.jogador.rect.copy()
        with patch('pygame.key.get_pressed', side_effect=AssertionError('Movimento durante desafio')):
            quarto.atualizar()
        self.assertEqual(antes, quarto.jogador.rect)
        cozinha = TelaCozinha(self.game)
        cozinha.conversar()
        with patch('pygame.key.get_pressed', side_effect=AssertionError('Movimento durante diálogo')):
            cozinha.atualizar()

    def test_caderno_pausa_cronometro_e_bloqueia_respostas(self):
        sala = TelaSalaProva(self.game)
        sala.iniciar_prova('Matemática')
        self.game.trocar_cena(sala)
        frames = [[tecla(pygame.K_TAB)], [tecla(pygame.K_1)], [tecla(pygame.K_RIGHT)], [tecla(pygame.K_ESCAPE)], [pygame.event.Event(pygame.QUIT)]]
        tempos = []
        def eventos():
            tempos.append(sala.restante)
            return frames.pop(0)
        with patch('pygame.event.get', side_effect=eventos), patch('pygame.quit'):
            self.game.executar()
        self.assertEqual(tempos[:4], [90] * 4)
        self.assertLess(tempos[4], 90)
        self.assertEqual(len(sala.prova.respondidas), 0)
        self.assertFalse(self.game.pausado)

    def test_caderno_paginas_e_renderizacao_dos_cenarios(self):
        for i in range(12):
            self.game.registrar(str(i), f'Descoberta {i}', 'Uma memória importante para a próxima tentativa.')
        for pagina in (-1, 0, 1, 3, 99):
            self.game.pagina_caderno = pagina
            desenhar_caderno(self.game.tela, self.game)
            self.assertIn(self.game.pagina_caderno, range(4))
        for classe in (TelaQuarto, TelaCozinha, TelaRua, TelaCorredor, TelaSalaProva, TelaVoltaCorredor, TelaRuaVolta, TelaCelebracao):
            classe(self.game).desenhar(self.game.tela)

    def test_prova_opcional_missao_e_finais_preservados(self):
        for acertar, final in ((True, TelaVoltaCorredor), (False, TelaViagemTempo)):
            sala = TelaSalaProva(self.game)
            sala.iniciar_prova('Matemática')
            self.game.trocar_cena(sala)
            self.assertEqual(sala.loja.creditos, 0)
            while self.game.cena_atual is sala:
                correta = sala.questoes[sala.idx_atual].correta
                sala.responder(correta if acertar else (correta + 1) % 4)
                if self.game.cena_atual is sala:
                    self.game.dt = 1.4
                    sala.atualizar()
            self.assertIsInstance(self.game.cena_atual, final)
        self.game.nota = 105
        rua = TelaRuaVolta(self.game)
        self.assertNotIn(rua.anotacoes, rua.objetos)
        self.assertNotIn(rua.volta, rua.objetos)
        self.interagir(rua, rua.saida)
        celebracao = self.game.cena_atual
        self.assertIsInstance(celebracao, TelaCelebracao)
        for _ in range(3):
            celebracao.processar_eventos([tecla(pygame.K_RETURN)])
        self.assertTrue(celebracao.concluiu)


if __name__ == '__main__':
    unittest.main()
