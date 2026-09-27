# One More Try


---

## 1. Título do Jogo

**One More Try** — um jogo de aventura e puzzle onde o destino do personagem depende do seu desempenho em uma prova escolar. Ao reprovar, PeLezin é jogado de volta no tempo e precisa recomeçar tudo — quantas vezes for necessário.

---

## 2. Descrição Geral

- **Tipo:** Aventura 2D com elementos de Puzzle
- **Perspectiva:** Side-scroller (2D Lateral)
- **Ambiente:** Dia a dia escolar — do quarto do aluno até a sala de aula do IFRN
- **Ideia principal:** Acompanhe PeLezin em sua jornada matinal até a escola, enfrente a prova mais temida do ano e descubra se ele passa de ano — ou se precisa voltar no tempo para tentar de novo.

O jogo captura a tensão real de uma semana de provas no IFRN, transformando a experiência cotidiana do estudante em uma narrativa interativa e dramática.

---

## 3. Objetivo do Jogo

O jogador precisa guiar PeLezin desde seu quarto até a sala de aula e, ao chegar lá, responder corretamente às questões da prova para **acumular pontos suficientes e passar de ano**.

**Meta principal:** Atingir a nota mínima de aprovação respondendo às questões dentro da sala de aula.

- **Vitória:** Pontuação suficiente → PeLezin sai da sala, interage no corredor e volta para casa para uma celebração com a família.
- **Derrota:** Pontuação abaixo do mínimo (−30 pontos) → a prova queima na tela e o jogo ativa o **mecanismo de viagem no tempo**, retornando ao início para uma nova tentativa.

---

## 4. Personagem Principal

**Nome:** PeLezin
**Quem é:** Um aluno do ensino médio que luta para conseguir sua aprovação no ano letivo, enfrentando o Professor de Matemática como seu maior obstáculo.

| Atributo       | Descrição                                                   |
|----------------|-------------------------------------------------------------|
| Movimentação   | 2D com teclas W, A, S, D                                   |
| Vida / Energia | Representada pela **pontuação** da prova                   |
| Velocidade     | Padrão (sem variação por enquanto)                         |
| Pontuação      | Funciona como nota — acertos sobem, erros descem           |
| Estado especial| Pode "viajar no tempo" ao reprovar, reiniciando a jornada  |

---

## 5. Inimigos e Obstáculos

Não há inimigos físicos no jogo. Os verdadeiros adversários de PeLezin são:

| Adversário            | Comportamento                                                                 | Efeito ao "colidir"                        |
|-----------------------|------------------------------------------------------------------------------|--------------------------------------------|
| **Questões fáceis**   | Estáticas, apresentadas na tela de prova                                    | Erro = −pontos (penalidade maior que difícil) |
| **Questões médias**   | Estáticas, com grau intermediário                                           | Erro = −pontos médios                      |
| **Questões difíceis** | Estáticas, maior complexidade                                               | Erro = −pontos menores |
| **O tempo**           | Pressão psicológica — a dificuldade vai aumentando progressivamente         | Aumenta o estresse do jogador               |



---

## 6. Sistema de Pontuação

| Ação                          | Efeito na Pontuação            |
|-------------------------------|-------------------------------|
| Acertar questão fácil         | +5 pontos                     |
| Acertar questão média         | +10 pontos                    |
| Acertar questão difícil       | +20 pontos                    |
| Errar questão fácil           | −15 pontos (penalidade maior) |
| Errar questão média           | −10 pontos                    |
| Errar questão difícil         | −5 pontos (penalidade menor)  |
| Usar item de dica (da loja)   | Revela ou descarta alternativa |

> A loja interna pode ser acessada com pontos acumulados após sequências de acertos.

---

## 7. Sistema de Vida

- **Representação:** A pontuação é a "vida" do jogador
- **Início:** 0 pontos (a prova começa zerada)
- **Perda de vida:** Respostas erradas diminuem a pontuação
- **Game Over:** Ao atingir **−30 pontos**, a prova queima na tela
- **Consequência do Game Over:** Ativa a mecânica de **viagem no tempo** — PeLezin retorna ao quarto e o jogador recomeça a jornada

---

## 8. Controles

| Tecla(s)         | Função                                      |
|------------------|---------------------------------------------|
| `W` `A` `S` `D`  | Movimentação do personagem                  |
| `1` `2` `3` `4`  | Seleção de alternativas na prova            |
| `ESC`            | Pausar / sair do jogo                       |
| `E`              | Interagir com NPCs e objetos do cenário     |
| `ENTER`          | Confirmar ação / avançar diálogos           |

---

## 9. Fluxo do Jogo

1. **Início:** PeLezin acorda em seu quarto
2. **Ato 1 — Casa:** Diálogo com a mãe na cozinha (contexto narrativo)
3. **Ato 2 — Caminho:** Travessia a pé ou de ônibus até a escola
4. **Ato 3 — Escola:** Interação com NPCs no pátio (clima leve, árvores, flores)
5. **Ato 4 — Prova:** PeLezin explora a sala e conversa com a turma → senta na carteira marcada → escolhe o assunto → prova começa com questões fáceis e vai ficando progressivamente mais difícil
6. **Ramificação:**
   - **Passou:** Sai da sala → interage no corredor → caminho de volta → cena de celebração em casa
   - **Reprovou:** Game Over → cena dramática da prova queimando → viagem no tempo → retorno ao Ato 1

---

## 10. Regras do Jogo

- PeLezin **não pode atravessar paredes** ou sair dos limites de cada cenário
- Durante a prova, o personagem está **fixo** — apenas as teclas de resposta funcionam
- Cada questão só pode ser respondida **uma vez**
- Itens de dica são **limitados** e custam pontos acumulados na loja
- Antes da prova, o jogador pode voltar entre quarto, cozinha, rua e pátio para explorar
- Ao reprovar, a manhã e a missão recomeçam; o caderno mantém descobertas durante a mesma partida
- Diálogos com NPCs são **opcionais**, mas podem fornecer dicas sobre as questões

---

## 11. Estrutura do Projeto

```
one-more-try/
├── main.py                      # Ponto de entrada
├── jogo/
│   ├── __init__.py
│   ├── game.py                  # Loop principal, pausa e troca de cenas
│   ├── settings.py              # Configurações e regras de pontuação
│   ├── models.py                # Personagens, questões, prova e loja de dicas
│   ├── cenas/
│   │   ├── menu.py              # Tela inicial e ajuda
│   │   ├── cena.py              # Base das fases, quarto, cozinha, rua e pátio
│   │   ├── sala_prova.py        # Escolha de assunto e interface da prova
│   │   └── finais.py            # Viagem no tempo, volta para casa e celebração
│   ├── sistemas/
│   │   ├── banco_perguntas.py   # Carregamento e sorteio das questões
│   │   ├── dialogo.py           # Gerenciamento de diálogos
│   │   ├── sprites.py           # Carregamento de imagens opcionais
│   │   └── progresso.py         # Memórias e missão de cada manhã
│   ├── ui/
│   │   ├── botoes_tela_inicial.py # Botões reutilizáveis
│   │   ├── interface.py         # Renderização de texto
│   │   ├── caderno.py           # Caderno de memórias paginado
│   │   └── desafio.py           # Exercícios interativos
│   └── objetos/
│       ├── objetos_cenarios.py  # Móveis, portas, banco e chão
│       └── sala_prova_objetos.py # Objetos da sala de aula
├── assets/
│   └── sprites/                 # PNGs opcionais de personagens e objetos
├── data/
│   └── questions.json          # Banco de perguntas
├── tests/
│   └── test_expansao.py         # Missão, memórias, desafios e percurso
├── requirements.txt
└── README.md
```

O código usa imports a partir do pacote `jogo`. Os arquivos de perguntas e
sprites são localizados em relação ao projeto, independentemente do diretório
de onde o jogo é iniciado.

---

## 12. Funcionalidades Mínimas (MVP — v1.0)

Para a primeira versão funcional, o jogo **obrigatoriamente** deve ter:

- [x] Movimentação básica do PeLezin (W, A, S, D)
- [x] Pelo menos **3 cenários** funcionais: pátio da escola, sala de aula e tela de game over
- [x] Banco de perguntas com ao menos **10 questões** nos 3 níveis de dificuldade
- [x] Sistema de pontuação funcional (acertos e erros com penalidades corretas)
- [x] Tela de game over com animação da prova queimando
- [x] Mecânica de reinício (viagem no tempo → volta ao início)
- [x] Transição básica entre as cenas do storyboard
- [x] HUD mostrando a pontuação atual durante a prova

---

## 13. Melhorias Futuras

- **Criação de perguntas pelo jogador:** Interface para o aluno adicionar suas próprias questões ao banco de dados
- **Modo Boss — Vire o Professor:** O jogador assume o papel do professor e desafia outros alunos
- **Modo Multiplayer local:** Dois jogadores competem na mesma prova
- **Loja expandida:** Mais itens com efeitos diferentes (eliminar alternativa, pausar tempo, revisar questão)
- **Cutscenes animadas:** Cenas de transição com animação para o storyboard completo
- **Trilha sonora adaptativa:** Música que muda conforme a pontuação do jogador
- **Ranking de pontuações:** Placar salvo localmente com os melhores desempenhos
- **Variações de dificuldade:** Modo "Véspera de Prova" com penalidades dobradas

---

*Desenvolvido como projeto da disciplina de Programação Orientada a Objetos — IFRN Campus Caicó, 2º ano.*

---

## 14. Versão implementada — setembro de 2026

O código está organizado no pacote `jogo/`, conforme a estrutura acima.
O arquivo `main.py` da raiz inicia a aplicação. Não é preciso ter sprites para jogar.

```bash
python -m pip install -r requirements.txt
python main.py
```

Dependência: **pygame-ce 2.5.8**, importado normalmente como `pygame`.
Não instalar `pygame` e `pygame-ce` juntos no mesmo ambiente virtual.

- Jornada completa: quarto → cozinha → rua → pátio → prova → corredor →
  volta para casa → celebração. Ao reprovar, a viagem no tempo retorna ao quarto.
- WASD move; E interage perto de portas/NPCs; ENTER avança diálogos.
- Prova com escolha de Matemática ou POO/Python, nove questões e até 90 segundos.
- **Aprovação: 50 pontos; derrota imediata: −30; máximo: 105.** Ao acabar
  tempo/questões, nota abaixo de 50 também reprova.
- 1–4 ou mouse responde. H compra dica por 5 créditos (até duas dicas).
  Cada dois acertos consecutivos rendem 5 créditos, separados da nota.
- ESC pausa/continua. Durante a pausa, M volta ao menu.
- A exploração é livre antes da prova; só a prova possui cronômetro.

Detalhes: [relatório de implementação](RELATORIO_IMPLEMENTACAO.md),
[contexto para continuidade](CONTEXTO_PROJETO.md) e
[preparação de sprites](assets/sprites/README.md).

Testes sem abrir janela:

```bash
python -B -m unittest discover -s tests -v
```


## 15. Primeira expansão — memórias e exploração

- **TAB** abre e fecha o caderno; **← / →** trocam suas páginas. Ele mostra o
  objetivo atual e as descobertas. Enquanto está aberto, o jogo e o cronômetro
  da prova ficam pausados. **ESC** também fecha o caderno.
- No quarto, aproxime-se da **escrivaninha** para revisar herança em POO ou do
  **fliperama** para resolver uma sequência numérica. Use **1–4** para responder
  e **ENTER** para sair. Não há penalidade por erro; acertos registram dicas.
- Investigue o **relógio 07:10**. Depois de uma reprovação, ele, a mãe e Ana
  revelam novas falas e pistas sobre a repetição do dia.
- Converse com **Ana no pátio**, procure as folhas perto do banco na rua e
  devolva-as. Também é possível encontrar as folhas antes de conhecer a missão.
  A devolução registra uma revisão de Matemática/POO e concede **5 créditos de
  dica no início da prova**, uma vez naquela manhã, sem alterar a nota.
- Portas identificadas permitem ir e voltar entre os cenários antes da prova.
  A entrada na sala é voluntária; os desafios e a missão são opcionais.
- **E** interage com o alvo próximo mais perto do personagem. Também é possível
  clicar no objeto estando perto. Indicadores **!** marcam novidades; o rodapé
  mostra o alvo da interação e avisos confirmam novas descobertas.
- Na viagem no tempo, o **caderno permanece**, mas as folhas, a missão e as
  conversas da manhã são reiniciadas. Escolher **Jogar** no menu começa uma
  partida nova e limpa as memórias. Esta versão não salva progresso em disco.

Verificação automática sem abrir janela:

```bash
python -B -m unittest discover -s tests -v
```

### Sala de prova explorável

- Use **WASD** para caminhar e **E** para conversar com Lucas, Bia e o professor.
- A porta permite voltar ao pátio antes da prova.
- A carteira dourada abre a escolha de assunto. **BACKSPACE** permite levantar.
- O cronômetro começa somente após escolher o assunto.
- Alunos têm pequenas animações e balões de conversa; o professor caminha perto do quadro.
- Após uma reprovação, conversar com o professor revela uma memória do ciclo.


### Interface da prova — painel inferior

Durante a escolha do assunto e a prova, a sala permanece visível acima do painel.
A barra superior reúne nota, questão e tempo. As alternativas ficam em duas colunas,
com atalhos **1–4** ou clique, destaque ao passar o mouse e cores de acerto/erro.
O painel ajusta e quebra textos longos; dicas eliminadas ficam desativadas.
**H**, **TAB** e **ESC** continuam disponíveis. A troca de questão tem uma breve
transição visual; o professor e os colegas mantêm movimentos discretos ao fundo.


O jogo abre em **tela cheia**, mantendo a proporção original de 800×600.
Em monitores mais largos, podem aparecer faixas laterais. Os cliques são
ajustados automaticamente à escala da imagem; **ESC** continua pausando o jogo.
