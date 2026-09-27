import json
from pathlib import Path
import random

from jogo.models import PerguntaFacil, PerguntaMedia, PerguntaDificil

# Caminho absoluto para não depender de onde o jogo foi executado
CAMINHO_QUESTOES = Path(__file__).resolve().parents[2] / "data" / "questions.json"

# Mapeia a chave usada no JSON para a classe de Questao correspondente
_CLASSES_POR_DIFICULDADE = {
    "facil": PerguntaFacil,
    "media": PerguntaMedia,
    "dificil": PerguntaDificil,
}


def _carregar_banco_bruto():
    with open(CAMINHO_QUESTOES, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _construir_questoes(lista_dados, classe_questao):
    return [
        classe_questao(
            opcoes=dados["opcoes"],
            enunciado=dados["enunciado"],
            correta=dados["correta"],
        )
        for dados in lista_dados
    ]


def carregar_todas_as_questoes():
    banco_bruto = _carregar_banco_bruto()
    return {
        dificuldade: _construir_questoes(banco_bruto.get(dificuldade, []), classe)
        for dificuldade, classe in _CLASSES_POR_DIFICULDADE.items()
    }


def sortear_prova(qtd_facil=5, qtd_media=5, qtd_dificil=5, assunto=None):
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
