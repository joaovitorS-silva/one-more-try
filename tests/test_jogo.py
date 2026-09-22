"""Regressões das regras e do percurso, sem abrir janela."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from unittest.mock import patch
import pygame
from main import Game, TelaInicial
from cena import TelaQuarto, TelaCozinha, TelaRua, TelaCorredor
from sala_prova import TelaSalaProva
from finais import TelaViagemTempo, TelaVoltaCorredor, TelaRuaVolta, TelaCelebracao
from models import Prova, LojaDicas, PerguntaFacil, PerguntaMedia, PerguntaDificil
from banco_perguntas import sortear_prova


def tecla(k):
    return pygame.event.Event(pygame.KEYDOWN, key=k)


class JogoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.game.nova_partida()
        self.game.dt = 1 / 60

    def test_pontuacao_e_resposta_unica(self):
        for classe, acerto, erro in [(PerguntaFacil, 5, -15), (PerguntaMedia, 10, -10), (PerguntaDificil, 20, -5)]:
            q = classe(['a','b','c','d'], 'Teste', 0)
            for acertou, esperado in [(True, acerto), (False, erro)]:
                prova = Prova([q])
                prova.responder(q, acertou)
                prova.responder(q, acertou)
                self.assertEqual(prova.pontuacao_total, esperado)

    def test_bancos_progressivos_sem_repeticao(self):
        for assunto in ('POO e Python', 'Matemática'):
            questoes = sortear_prova(3,3,3,assunto)
            self.assertEqual(len({q.enunciado for q in questoes}),9)
            self.assertEqual([q.dificuldade for q in questoes], ['facil']*3+['media']*3+['dificil']*3)

    def test_loja_limite_e_nota_preservada(self):
        loja = LojaDicas()
        q = PerguntaFacil(['a','b','c','d'],'Teste',0)
        self.assertIsNone(loja.comprar(q, []))
        for _ in range(6):
            loja.registrar_resposta(True)
        eliminadas = []
        for _ in range(2):
            eliminadas.append(loja.comprar(q, eliminadas))
        self.assertNotIn(0, eliminadas)
        self.assertEqual(len(set(eliminadas)), 2)
        self.assertIsNone(loja.comprar(q, eliminadas))
        loja.registrar_resposta(False)
        self.assertEqual(loja.sequencia, 0)

    def test_derrota_e_reinicio(self):
        sala = TelaSalaProva(self.game)
        self.game.trocar_cena(sala)
        sala.iniciar_prova('Matemática')
        for _ in range(2):
            sala.responder((sala.questoes[sala.idx_atual].correta + 1) % 4)
            if self.game.cena_atual is sala:
                self.game.dt = 1.4
                sala.atualizar()
        self.assertIsInstance(self.game.cena_atual, TelaViagemTempo)
        self.game.dt = 4
        self.game.cena_atual.atualizar()
        self.assertIsInstance(self.game.cena_atual, TelaQuarto)
        self.assertEqual(self.game.tentativa,2)
        self.assertEqual(self.game.nota,0)

    def test_vitoria_e_celebracao(self):
        sala = TelaSalaProva(self.game)
        self.game.trocar_cena(sala)
        sala.iniciar_prova('POO e Python')
        for _ in range(9):
            sala.responder(sala.questoes[sala.idx_atual].correta)
            self.game.dt = 1.4
            sala.atualizar()
        self.assertEqual(self.game.nota,105)
        self.assertIsInstance(self.game.cena_atual,TelaVoltaCorredor)
        self.game.cena_atual.proxima_fase()
        self.assertIsInstance(self.game.cena_atual,TelaRuaVolta)
        self.game.cena_atual.proxima_fase()
        celebracao = self.game.cena_atual
        self.assertIsInstance(celebracao,TelaCelebracao)
        for _ in range(3):
            celebracao.processar_eventos([tecla(pygame.K_RETURN)])
        self.assertTrue(celebracao.concluiu)
        celebracao.desenhar(self.game.tela)
        celebracao.processar_eventos([tecla(pygame.K_RETURN)])
        self.assertIsInstance(self.game.cena_atual,TelaInicial)

    def test_tempo_esgotado(self):
        for nota, tipo in [(0,TelaViagemTempo), (50,TelaVoltaCorredor)]:
            sala = TelaSalaProva(self.game)
            sala.iniciar_prova('Matemática')
            sala.prova.pontuacao_total = nota
            sala.restante = 0.01
            sala.atualizar()
            self.assertIsInstance(self.game.cena_atual,tipo)

    def test_porta_exige_proximidade(self):
        quarto = self.game.cena_atual
        quarto.processar_eventos([tecla(pygame.K_e)])
        self.assertIs(self.game.cena_atual,quarto)
        quarto.jogador.rect.center = quarto.porta.rect.center
        quarto.processar_eventos([tecla(pygame.K_e)])
        self.assertIsInstance(self.game.cena_atual,TelaCozinha)
        self.game.cena_atual.proxima_fase()
        self.assertIsInstance(self.game.cena_atual,TelaRua)
        self.game.cena_atual.proxima_fase()
        self.assertIsInstance(self.game.cena_atual,TelaCorredor)
        self.game.cena_atual.proxima_fase()
        self.assertIsInstance(self.game.cena_atual,TelaSalaProva)

    def test_paredes_e_moveis(self):
        quarto = self.game.cena_atual
        quarto.jogador.rect.topleft = (795,510)
        quarto.atualizar()
        self.assertLessEqual(quarto.jogador.rect.right,800)
        self.assertLessEqual(quarto.jogador.rect.bottom,500)
        quarto.jogador.rect.topleft = (300,360)
        with patch('pygame.key.get_pressed',return_value={k:k == pygame.K_d for k in [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]}):
            for _ in range(10):
                quarto.atualizar()
        self.assertEqual(quarto.jogador.rect.right,quarto.fliperama.rect.left)

    def test_duplo_evento_nao_responde_duas_questoes(self):
        sala = TelaSalaProva(self.game)
        sala.iniciar_prova('Matemática')
        evento = tecla(pygame.K_1 + sala.questoes[0].correta)
        sala.processar_eventos([evento,evento])
        self.assertEqual(sala.prova.pontuacao_total,5)
        self.assertEqual(len(sala.prova.respondidas),1)

    def test_pausa_congela_prova_e_retorna(self):
        sala = TelaSalaProva(self.game)
        sala.iniciar_prova('Matemática')
        self.game.trocar_cena(sala)
        tempos = []
        quadros = [[tecla(pygame.K_ESCAPE)], [], [tecla(pygame.K_ESCAPE)],
                   [pygame.event.Event(pygame.QUIT)]]
        def eventos():
            tempos.append(sala.restante)
            return quadros.pop(0)
        with patch('pygame.event.get', side_effect=eventos), patch('pygame.quit'):
            self.game.executar()
        self.assertEqual(tempos[0],tempos[1])
        self.assertEqual(tempos[1],tempos[2])
        self.assertLess(tempos[3],tempos[2])
        # Mantém o SDL dos testes e recria apenas o controlador encerrado.
        self.__class__.game = Game()

    def test_sprites_opcionais(self):
        from tempfile import TemporaryDirectory
        from sprites import GerenciadorSprites
        with TemporaryDirectory() as pasta:
            gerenciador = GerenciadorSprites(pasta)
            tela = pygame.Surface((40,40))
            rect = pygame.Rect(0,0,20,20)
            gerenciador.desenhar(tela,'ausente',rect,(20,40,60))
            self.assertEqual(tuple(tela.get_at((10,10)))[:3],(20,40,60))
            imagem = pygame.Surface((5,5),pygame.SRCALPHA)
            imagem.fill((70,80,90))
            pygame.image.save(imagem,os.path.join(pasta,'presente.png'))
            gerenciador.desenhar(tela,'presente',rect,(0,0,0))
            self.assertEqual(tuple(tela.get_at((10,10)))[:3],(70,80,90))
            with open(os.path.join(pasta,'invalido.png'),'w') as arquivo:
                arquivo.write('imagem inválida')
            gerenciador.desenhar(tela,'invalido',rect,(20,40,60))
            self.assertEqual(tuple(tela.get_at((10,10)))[:3],(20,40,60))

    def test_renderizar_todas_as_telas(self):
        for classe in (TelaInicial,TelaQuarto,TelaCozinha,TelaRua,TelaCorredor,TelaSalaProva,TelaVoltaCorredor,TelaRuaVolta,TelaCelebracao):
            classe(self.game).desenhar(self.game.tela)
        viagem = TelaViagemTempo(self.game,'Teste')
        for tempo in (0,1,2.5,3.8):
            viagem.tempo = tempo
            viagem.desenhar(self.game.tela)
        sala = TelaSalaProva(self.game)
        for assunto in sala.assuntos:
            sala.iniciar_prova(assunto)
            for i in range(9):
                sala.idx_atual = i
                sala._carregar_botoes_da_questao()
                sala.desenhar(self.game.tela)


if __name__ == '__main__':
    unittest.main()
