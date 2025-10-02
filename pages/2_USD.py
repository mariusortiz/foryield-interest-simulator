# pages/2_USD.py
import streamlit as st
import altair as alt
from common import simulate

st.title("USD Strategy + ForYield Interest")

with st.sidebar:
    st.header("Paramètres")
    initial_capital = st.number_input("Capital initial (USD)", min_value=0.0, value=100_000.0, step=1_000.0, format="%.2f")
    monthly_contribution = st.number_input("Versement mensuel (USD)", min_value=0.0, value=2_000.0, step=100.0, format="%.2f")
    years = int(st.number_input("Horizon (années)", min_value=1, max_value=50, value=5, step=1))
    start_price = st.number_input("Prix USD de départ", min_value=0.01, value=1.0, step=0.01, format="%.2f")
    annual_app_pct = st.number_input("Appréciation USD annuelle (%)", min_value=-99.0, max_value=500.0, value=0.0, step=0.1, format="%.2f")
    apy_pct = st.number_input("Rendement APY ForYield (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.1, format="%.2f")
    exit_fee_pct = st.number_input("Frais de sortie (%)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f")
    st.markdown("---")
    st.info("Par défaut, USD = actif stable (prix 1, appréciation 0%).")

res = simulate(initial_capital, monthly_contribution, years, start_price, annual_app_pct, apy_pct, exit_fee_pct)
df = res["df"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Valeur finale après frais", f"$ {res['final_net_value']:,.0f}")
c2.metric("Valeur finale brute", f"$ {res['gross_final_value']:,.0f}")
c3.metric("Total investi", f"$ {res['invested']:,.0f}")
c4.metric("Frais de sortie", f"$ {res['exit_fee_amount']:,.0f}")

price_line = alt.Chart(df).mark_line(strokeDash=[6,4]).encode(x="Mois:Q", y=alt.Y("Prix:Q", axis=alt.Axis(title="Prix", orient="right")))
value_line = alt.Chart(df).mark_line().encode(x="Mois:Q", y=alt.Y("Valeur:Q", axis=alt.Axis(title="Valeur (USD)")))
invested_line = alt.Chart(df).mark_line(strokeDash=[2,4]).encode(x="Mois:Q", y=alt.Y("Investi:Q"))
st.altair_chart(alt.layer(value_line, price_line, invested_line).resolve_scale(y="independent"), use_container_width=True)

st.dataframe(df.head(24), use_container_width=True)
st.caption("Simulation éducative — pas un conseil en investissement.")
