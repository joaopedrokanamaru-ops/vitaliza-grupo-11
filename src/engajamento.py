"""Níveis de engajamento dos assinantes da Vitaliza (definição do grupo, 14/11/2026).

Definição dada pelo grupo:
- alto: fez algum treino (qualquer tipo e duração) nos últimos 7 dias;
- médio: fez de 1 a 4 treinos no último mês;
- baixo: não treinou no último mês;
- possível churn: não treina há 45 dias.

Para cada conta cair em um único nível, as regras são aplicadas nesta ordem:
1. alto: último treino há 0 a 6 dias (os 7 dias que terminam na data de referência);
2. médio: último treino há 7 a 29 dias (treinou no mês, mas não na última semana).
   A coluna `medio_5_mais` marca quem fez 5 ou mais treinos no mês sem treinar na última
   semana: a definição original não diz onde essa conta entra, e ela fica no médio;
3. baixo: último treino há 30 a 44 dias;
4. possível churn: último treino há 45 dias ou mais, ou nenhum treino.

Conta sem nenhum treino até a data de referência: os dias sem treinar contam a partir do
início da assinatura, e a coluna `nunca_treinou` marca o caso (um assinante de 10 dias de
casa sem treino não está "há 45 dias sem treinar").
"""
import pandas as pd

NIVEIS = ["1. alto", "2. médio", "3. baixo", "4. possível churn"]


def niveis_engajamento(atividades, contas, ref, inicio=None):
    """Classifica cada conta de `contas` na data `ref`.

    atividades: tabela com `user_id` e `data` (atividades_limpa).
    contas: Series ou lista de user_id a classificar.
    ref: data de referência (o dia da foto, incluído na janela). Pode ser uma data única
        ou uma Series (índice user_id) com a data de cada conta.
    inicio: Series opcional (índice user_id) com o início da assinatura. Conta sem nenhum
        treino até `ref` tem os dias contados a partir do início; sem `inicio`, vai para
        possível churn.

    Devolve um DataFrame por user_id com: ultimo_treino, dias_sem_treinar, treinos_7d,
    treinos_30d, nunca_treinou, medio_5_mais e nivel.
    """
    r = pd.DataFrame(index=pd.Index(pd.unique(pd.Series(contas)), name="user_id"))
    a = atividades.loc[atividades["user_id"].isin(set(r.index)), ["user_id", "data"]]
    if isinstance(ref, pd.Series):
        # data de referência própria de cada conta (ex.: a véspera da saída)
        ref = pd.to_datetime(ref).dt.normalize().reindex(r.index)
        ref_treino = a["user_id"].map(ref)
    else:
        ref = pd.Timestamp(ref)
        ref_treino = ref
    antes = a["data"] <= ref_treino
    a = a[antes]
    dias = ((ref_treino[antes] if isinstance(ref_treino, pd.Series) else ref_treino) - a["data"]).dt.days
    r["ultimo_treino"] = a.groupby("user_id")["data"].max()
    r["treinos_7d"] = a[dias <= 6].groupby("user_id").size()
    r["treinos_30d"] = a[dias <= 29].groupby("user_id").size()
    r[["treinos_7d", "treinos_30d"]] = r[["treinos_7d", "treinos_30d"]].fillna(0).astype(int)
    r["nunca_treinou"] = r["ultimo_treino"].isna()

    base = r["ultimo_treino"]
    if inicio is not None:
        base = base.fillna(pd.to_datetime(inicio).reindex(r.index))
    r["dias_sem_treinar"] = (ref - base).dt.days

    d = r["dias_sem_treinar"]
    r["nivel"] = NIVEIS[3]
    r.loc[d <= 44, "nivel"] = NIVEIS[2]
    r.loc[(d <= 29), "nivel"] = NIVEIS[1]
    r.loc[r["treinos_7d"] > 0, "nivel"] = NIVEIS[0]
    r["medio_5_mais"] = (r["nivel"] == NIVEIS[1]) & (r["treinos_30d"] >= 5)
    return r.reset_index()
