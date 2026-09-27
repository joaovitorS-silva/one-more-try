"""Memórias duram uma partida; objetos e favores recomeçam a cada manhã."""
class Progresso:
    def __init__(self):
        self.memorias = {}
        self.reiniciar_manha()

    def registrar(self, chave, titulo, descricao):
        if chave in self.memorias:
            return False
        self.memorias[chave] = (titulo, descricao)
        return True

    def reiniciar_manha(self):
        self.missao_ana = 'desconhecida'
        self.conversas = set()

    def aceitar_missao(self):
        if self.missao_ana == 'desconhecida':
            self.missao_ana = 'procurando'

    def recolher_anotacoes(self):
        if self.missao_ana in ('desconhecida', 'procurando'):
            self.missao_ana = 'encontradas'
            return True
        return False

    def devolver_anotacoes(self):
        if self.missao_ana == 'encontradas':
            self.missao_ana = 'concluida'
            return True
        return False

    @property
    def objetivo(self):
        return {
            'desconhecida': 'Explore a manhã e encontre Ana no pátio.',
            'procurando': 'Procure as anotações perto do banco no ponto de ônibus.',
            'encontradas': 'Devolva as anotações para Ana no pátio.',
            'concluida': 'Ajuda garantida! Entre na sala quando estiver pronto.',
        }[self.missao_ana]
