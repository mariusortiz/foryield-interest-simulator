# app.py (BTC)
import streamlit as st
import altair as alt
from common import simulate

st.set_page_config(page_title="ForYield – Simulateur BTC", page_icon="🟡", layout="wide")

st.title("BTC Growth + ForYield Interest Simulator")
st.caption("Modélisez l’évolution d’un capital avec appréciation/dépréciation de l’actif, APY composé mensuellement, versements mensuels et frais de sortie.")

with st.sidebar:
    st.header("Paramètres")
    initial_capital = st.number_input("Capital initial (€)", min_value=0.0, value=100_000.0, step=1_000.0, format="%.2f")
    monthly_contribution = st.number_input("Versement mensuel (€)", min_value=0.0, value=2_000.0, step=100.0, format="%.2f")
    years = int(st.number_input("Horizon (années)", min_value=1, max_value=50, value=5, step=1))
    start_price = st.number_input("Prix BTC de départ (€)", min_value=0.01, value=60_000.0, step=100.0, format="%.2f")
    annual_app_pct = st.number_input("Appréciation BTC annuelle (%)", min_value=-99.0, max_value=500.0, value=10.0, step=0.5, format="%.2f")
    apy_pct = st.number_input("Rendement APY ForYield (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.1, format="%.2f")
    exit_fee_pct = st.number_input("Frais de sortie (%)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f")
    st.markdown("---")
    st.info("Hypothèses : rendement composé **mensuellement** ; contributions au **prix du mois** ; croissance **géométrique** du prix. **Frais de sortie** appliqués en fin d’horizon.")

res = simulate(initial_capital, monthly_contribution, years, start_price, annual_app_pct, apy_pct, exit_fee_pct)
df = res["df"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Valeur finale après frais", f"€ {res['final_net_value']:,.0f}")
c2.metric("Valeur finale brute", f"€ {res['gross_final_value']:,.0f}")
c3.metric("Total investi", f"€ {res['invested']:,.0f}")
c4.metric("Frais de sortie", f"€ {res['exit_fee_amount']:,.0f}")

st.subheader("Évolution du portefeuille (brut)")
price_line = alt.Chart(df).mark_line(strokeDash=[6,4]).encode(
    x="Mois:Q", y=alt.Y("Prix:Q", axis=alt.Axis(title="Prix", orient="right"))
)
value_line = alt.Chart(df).mark_line().encode(
    x="Mois:Q", y=alt.Y("Valeur:Q", axis=alt.Axis(title="Valeur (€)"))
)
invested_line = alt.Chart(df).mark_line(strokeDash=[2,4]).encode(
    x="Mois:Q", y=alt.Y("Investi:Q", axis=alt.Axis(title="Investi (€)", labels=False, ticks=False))
)
chart = alt.layer(value_line, price_line, invested_line).resolve_scale(y="independent")
st.altair_chart(chart, use_container_width=True)

st.subheader("Tableau (aperçu 24 mois)")
st.dataframe(df.head(24), use_container_width=True)

st.caption("**Simulation éducative** — ceci n'est pas un conseil en investissement.")
