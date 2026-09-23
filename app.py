import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURAÇÃO
# ==================================================

st.set_page_config(
    page_title="Dashboard de Rejeitos MDF",
    layout="wide"
)

st.title("Dashboard de Rejeitos MDF")

# ==================================================
# LEITURA DA PLANILHA
# ==================================================

df = pd.read_excel("Base de dados.xlsx")

df["Data"] = pd.to_datetime(df["Data"])

# ==================================================
# REMOVER CAPA
# ==================================================

df = df[
    ~df["Tipo de rejeitos/CAPA"]
    .astype(str)
    .str.upper()
    .str.contains("CAPA", na=False)
]

# ==================================================
# FILTROS
# ==================================================

st.sidebar.header("Filtros")

linha = st.sidebar.multiselect(
    "Linha",
    options=sorted(df["Linha"].dropna().unique()),
    default=sorted(df["Linha"].dropna().unique())
)

turno = st.sidebar.multiselect(
    "Turno",
    options=sorted(df["Turno"].dropna().unique()),
    default=sorted(df["Turno"].dropna().unique())
)

espessura = st.sidebar.multiselect(
    "Espessura",
    options=sorted(df["Espessura"].dropna().unique()),
    default=sorted(df["Espessura"].dropna().unique())
)

data_inicial = st.sidebar.date_input(
    "Data Inicial",
    df["Data"].min()
)

data_final = st.sidebar.date_input(
    "Data Final",
    df["Data"].max()
)

# ==================================================
# APLICAR FILTROS
# ==================================================

df = df[df["Linha"].isin(linha)]
df = df[df["Turno"].isin(turno)]
df = df[df["Espessura"].isin(espessura)]

df = df[
    (df["Data"] >= pd.to_datetime(data_inicial))
    &
    (df["Data"] <= pd.to_datetime(data_final))
]

# ==================================================
# INDICADORES
# ==================================================

if len(df) > 0:

    principal_defeito = (
        df.groupby("Motivo do rejeitos/CAPA")
        ["Total de rejeitos"]
        .sum()
        .idxmax()
    )

    linha_critica = (
        df.groupby("Linha")
        ["Total de rejeitos"]
        .sum()
        .idxmax()
    )

    turno_critico = (
        df.groupby("Turno")
        ["Total de rejeitos"]
        .sum()
        .idxmax()
    )

else:

    principal_defeito = "-"
    linha_critica = "-"
    turno_critico = "-"

# ==================================================
# CARDS
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Rejeitos",
    int(df["Total de rejeitos"].sum())
)

col2.metric(
    "Volume Perdido (m³)",
    round(df["Volume"].sum(),2)
)

col3.metric(
    "Linha Crítica",
    linha_critica
)

col4.metric(
    "Principal Defeito",
    principal_defeito
)

col5.metric(
    "Turno Crítico",
    turno_critico
)

st.divider()

# ==================================================
# GRÁFICOS - LINHA SUPERIOR
# ==================================================

col_esq, col_dir = st.columns(2)

with col_esq:

    st.subheader("Rejeitos por Linha")

    graf_linha = (
        df.groupby("Linha")
        ["Total de rejeitos"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        graf_linha,
        x="Linha",
        y="Total de rejeitos",
        color="Linha",
        text_auto=True
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col_dir:

    st.subheader("Rejeitos por Turno")

    graf_turno = (
        df.groupby("Turno")
        ["Total de rejeitos"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        graf_turno,
        x="Turno",
        y="Total de rejeitos",
        color="Turno",
        text_auto=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# GRÁFICOS - SEGUNDA LINHA
# ==================================================

col_esq, col_dir = st.columns(2)

with col_esq:

    st.subheader("Pareto dos Motivos")

    graf_motivo = (
        df.groupby("Motivo do rejeitos/CAPA")
        ["Total de rejeitos"]
        .sum()
        .reset_index()
        .sort_values(
            "Total de rejeitos",
            ascending=False
        )
    )

    fig3 = px.bar(
        graf_motivo,
        x="Total de rejeitos",
        y="Motivo do rejeitos/CAPA",
        orientation="h",
        text_auto=True
    )

    fig3.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col_dir:

    st.subheader("Ranking de Defeitos por Turno")

    ranking = (
        df.groupby(
            ["Turno", "Motivo do rejeitos/CAPA"]
        )["Total de rejeitos"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        ranking,
        x="Turno",
        y="Total de rejeitos",
        color="Motivo do rejeitos/CAPA",
        text_auto=True
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==================================================
# REJEITOS POR DIA
# ==================================================

st.subheader("Rejeitos por Dia")

graf_dia = (
    df.groupby("Data")
    ["Total de rejeitos"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    graf_dia,
    x="Data",
    y="Total de rejeitos",
    text_auto=True
)

st.plotly_chart(
    fig5,
    use_container_width=True
)