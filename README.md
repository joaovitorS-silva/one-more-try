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
5. **Ato 4 — Prova:** PeLezin entra na sala → escolhe os assuntos → prova começa com questões fáceis e vai ficando progressivamente mais difícil
6. **Ramificação:**
   - **Passou:** Sai da sala → interage no corredor → caminho de volta → cena de celebração em casa
   - **Reprovou:** Game Over → cena dramática da prova queimando → viagem no tempo → retorno ao Ato 1

---

## 10. Regras do Jogo

- PeLezin **não pode atravessar paredes** ou sair dos limites de cada cenário
- Durante a prova, o personagem está **fixo** — apenas as teclas de resposta funcionam
- Cada questão só pode ser respondida **uma vez**
- Itens de dica são **limitados** e custam pontos acumulados na loja
- O jogador **não pode pular fases** — o storyboard é linear
- Ao reprovar, **toda a jornada é reiniciada** (mas o banco de perguntas pode variar)
- Diálogos com NPCs são **opcionais**, mas podem fornecer dicas sobre as questões

---

## 11. Estrutura do Projeto

```
one-more-try/
│
├── assets/
│   ├── sprites/          # Imagens do personagem, NPCs, cenários
│   ├── sounds/           # Músicas e efeitos sonoros por fase
│   └── fonts/            # Fontes do jogo
│
├── data/
│   └── questions.json    # Banco de perguntas (fácil, médio, difícil)
│
├── src/
│   ├── main.py           # Ponto de entrada do jogo
│   ├── settings.py       # Configurações globais (resolução, FPS, etc.)
│   │
│   ├── scenes/           # Cada fase/cenário é uma cena separada
│   │   ├── bedroom.py
│   │   ├── kitchen.py
│   │   ├── street.py
│   │   ├── schoolyard.py
│   │   ├── classroom.py
│   │   ├── hallway.py
│   │   └── home_celebration.py
│   │
│   ├── entities/         # Classes dos personagens
│   │   ├── player.py
│   │   └── npc.py
│   │
│   ├── systems/          # Lógica do jogo
│   │   ├── quiz.py       # Sistema de perguntas e pontuação
│   │   ├── shop.py       # Loja de itens/dicas
│   │   ├── dialogue.py   # Sistema de diálogos
│   │   └── time_travel.py# Mecânica de viagem no tempo (game over)
│   │
│   └── ui/               # Interface visual
│       ├── hud.py        # HUD com pontuação atual
│       ├── menus.py      # Telas de menu, pausa e game over
│       └── question_screen.py # Tela de questões da prova
│
└── README.md
```

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
