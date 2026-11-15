# Vitaliza · grupo 12

Projeto de análise de dados do case Vitaliza (MBA Inteli, Módulo 2): entender a saída de
assinantes de um app de assinatura para quem treina. Data de corte: 30/09/2026.

## Por onde começar

**Análise exploratória (código e gráficos):**
[`notebooks/analise_exploratoria.ipynb`](notebooks/analise_exploratoria.ipynb), também em
[PDF](saidas/analise_exploratoria.pdf) e [HTML](saidas/analise_exploratoria.html). Um documento só, que
limpa a base, mostra os padrões ligados à saída e monta a segmentação, conferindo cada resultado contra
os notebooks de origem.

**Roteiro dos notebooks:** [`notebooks/00_artefato_tech.ipynb`](notebooks/00_artefato_tech.ipynb) resume
a entrega em quatro partes e aponta para os notebooks onde cada conta está feita.

**Mini deck:** [`saidas/mini_deck_vitaliza_grupo12.pdf`](saidas/mini_deck_vitaliza_grupo12.pdf).

| Parte | O que responde | Notebooks |
|---|---|---|
| Limpeza | O que foi corrigido, removido ou marcado em cada arquivo | 01 a 25 e [`decisoes.md`](decisoes.md) |
| Base única | Uma linha por usuário (63.929 contas, 119 colunas) | 39 a 43 |
| Padrões de saída | Onde, quando e com que sinais os assinantes saem | 26 a 38 |
| Segmentação | Cinco segmentos, com perfil, tamanho e saída histórica | 44 a 51 |
| Mini deck | Gráficos dos slides técnicos (logaritmo, escolha do k, os quatro grupos) | 52 |

## Principais resultados

- Dos 14.059 assinantes ativos em 30/06/2026, 16,7% saíram até 30/09. Quase todas as saídas (93%)
  são por renovação desligada.
- O plano mensal sai cerca de três vezes mais que o anual: cerca de 11% contra 3% ao mês em 2026.
- Quem desliga a renovação já treinava menos: 26% tinham treinado na semana antes da saída, contra
  82% dos ativos com renovação ligada.
- Segmentação oficial (k-means com k = 4, mais um grupo por regra), nos 14.753 ativos do corte:

| Segmento | Assinantes em 30/09 | Saída em três meses (jul a set/2026) |
|---|---|---|
| Esfriando | 2.876 | 26,6% |
| Inativos em 90 dias (regra) | 754 | 25,8% |
| Recém-chegados | 2.092 | 19,0% |
| Ativos ao ar livre | 5.001 | 12,6% |
| Ativos em ambiente fechado | 4.030 | 10,4% |

A saída de cada segmento é medida em quem tinha o mesmo perfil em 30/06/2026 (notebook 51), porque
depois do corte não há dado. Limitações e ressalvas estão no fim do notebook 00.

## Pastas
- `docs/`: enunciado do case, dicionário de dados e premissas.
- `dados/brutos/`: arquivos originais do data room (somente leitura, fora do Git).
- `dados/processados/`: tabelas intermediárias geradas pelo grupo (fora do Git).
- `notebooks/`: notebooks Jupyter de análise, numerados na ordem de execução.
- `src/`: código Python reutilizável (`engajamento.py`: níveis de engajamento).
- `saidas/`: resultados (tabelas e gráficos).

## Arquivos
- `AGENTS.md`: regras do projeto, lidas pelo agente (Claude Code ou Codex) ao começar.
- `CLAUDE.md`: aponta para o AGENTS.md.
- `decisoes.md`: registro das decisões de limpeza e de análise, com motivo, critério e linhas afetadas.
- `requirements.txt`: versões das bibliotecas Python.

## Como rodar
Os dados não vão para o GitHub. Cada integrante copia o data room para `dados/brutos/`, instala as
bibliotecas de `requirements.txt` e roda os notebooks na ordem dos números. O notebook 00 lê só os
arquivos de `saidas/`, que estão no repositório, e roda sem o data room.
