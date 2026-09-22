"""
Banco de perguntas da prova.

Responsável por:
- Carregar o banco de questões de data/questions.json
- Sortear aleatoriamente N perguntas de cada dificuldade (sem repetição)
- Devolver a prova já montada na ordem fácil -> média -> difícil,
  seguindo a progressão de dificuldade descrita no README.

Mantido separado de sala_prova.py de propósito: aqui só cuidamos dos
dados (de onde vêm as perguntas e como são sorteadas); sala_prova.py
cuida da interface/lógica de jogo. Isso deixa mais fácil trocar a fonte
das perguntas no futuro (ex: outro arquivo, banco de dados, API) sem
tocar na tela da prova.
"""
import json
import os
import random

from models import PerguntaFacil, PerguntaMedia, PerguntaDificil

# Caminho absoluto para não depender de onde o jogo foi executado
CAMINHO_QUESTOES = os.path.join(os.path.dirname(__file__), "data", "questions.json")

# Mapeia a chave usada no JSON para a classe de Questao correspondente
_CLASSES_POR_DIFICULDADE = {
    "facil": PerguntaFacil,
    "media": PerguntaMedia,
    "dificil": PerguntaDificil,
}


def _carregar_banco_bruto():
    """Lê o questions.json e devolve o dicionário cru (facil/media/dificil)."""
    with open(CAMINHO_QUESTOES, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _construir_questoes(lista_dados, classe_questao):
    """Converte uma lista de dicts do JSON em objetos Questao (Facil/Media/Dificil)."""
    return [
        classe_questao(
            opcoes=dados["opcoes"],
            enunciado=dados["enunciado"],
            correta=dados["correta"],
        )
        for dados in lista_dados
    ]


def carregar_todas_as_questoes():
    """Carrega o banco inteiro já convertido em objetos Questao, por dificuldade.

    Devolve um dict: {"facil": [...], "media": [...], "dificil": [...]}
    Útil se algum dia quisermos, por exemplo, mostrar quantas perguntas
    existem no banco, ou validar o JSON num teste.
    """
    banco_bruto = _carregar_banco_bruto()
    return {
        dificuldade: _construir_questoes(banco_bruto.get(dificuldade, []), classe)
        for dificuldade, classe in _CLASSES_POR_DIFICULDADE.items()
    }


def sortear_prova(qtd_facil=5, qtd_media=5, qtd_dificil=5, assunto=None):
    """Monta uma prova sorteando perguntas aleatórias do banco, sem repetição.

    A ordem final é sempre fácil -> média -> difícil (progressão de
    dificuldade), mas QUAIS perguntas de cada nível aparecem muda a
    cada prova, já que são sorteadas com random.sample().

    Levanta ValueError se o banco não tiver perguntas suficientes para
    a quantidade pedida em alguma dificuldade — melhor descobrir isso
    na inicialização do que travar o jogo no meio da prova.
    """
    banco = carregar_todas_as_questoes()
    if assunto:
        banco_bruto = _carregar_banco_bruto()
        banco = {nivel: _construir_questoes(
            [q for q in banco_bruto[nivel] if q.get("assunto", "POO e Python") == assunto], classe)
            for nivel, classe in _CLASSES_POR_DIFICULDADE.items()}

    pedidos = {
        "facil": qtd_facil,
        "media": qtd_media,
        "dificil": qtd_dificil,
    }

    for dificuldade, quantidade_pedida in pedidos.items():
        disponiveis = len(banco[dificuldade])
        if quantidade_pedida > disponiveis:
            raise ValueError(
                f"Pedidas {quantidade_pedida} perguntas '{dificuldade}', mas o banco "
                f"só tem {disponiveis}. Adicione mais perguntas em data/questions.json."
            )

    sorteadas_facil = random.sample(banco["facil"], qtd_facil)
    sorteadas_media = random.sample(banco["media"], qtd_media)
    sorteadas_dificil = random.sample(banco["dificil"], qtd_dificil)

    return sorteadas_facil + sorteadas_media + sorteadas_dificil
