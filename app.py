# app.py — v3
import streamlit as st
import altair as alt
from common import simulate

st.set_page_config(page_title="ForYield – Simulateur", page_icon="🧮", layout="wide")

st.title("ForYield – Simulateur de rendement & appréciation")

with st.sidebar:
    st.header("Stratégie")
    strategy = st.selectbox("Choisir la stratégie", ["BTC", "ETH", "USD", "EUR"])
    if strategy == "BTC":
        default_price, default_app = 60000.0, 10.0
        unit_label, currency = "BTC", "€"
    elif strategy == "ETH":
        default_price, default_app = 3000.0, 10.0
        unit_label, currency = "ETH", "€"
    elif strategy == "USD":
        default_price, default_app = 1.0, 0.0
        unit_label, currency = "USD", "$"
    else:
        default_price, default_app = 1.0, 0.0
        unit_label, currency = "EUR", "€"

    st.header("Paramètres")
    initial_capital = st.number_input(f"Capital initial ({currency})", min_value=0.0, value=100_000.0, step=1_000.0, format="%.2f")
    monthly_contribution = st.number_input(f"Versement mensuel ({currency})", min_value=0.0, value=2_000.0, step=100.0, format="%.2f")
    years = int(st.number_input("Horizon (années)", min_value=1, max_value=50, value=5, step=1))
    start_price = st.number_input(f"Prix {unit_label} de départ ({currency})", min_value=0.01, value=default_price, step=10.0 if default_price>2 else 0.01, format="%.2f")
    annual_app_pct = st.number_input(f"Appréciation {unit_label} annuelle (%)", min_value=-99.0, max_value=500.0, value=default_app, step=0.5, format="%.2f")
    apy_pct = st.number_input("Rendement APY ForYield (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.1, format="%.2f")
    exit_fee_pct = st.number_input("Frais de sortie (%)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f")
    st.markdown("---")
    st.info("Hypothèses : rendement composé **mensuellement** ; contributions au **prix du mois** ; croissance **géométrique** du prix. **Frais de sortie** appliqués en fin d’horizon.")

# Simulation
res = simulate(initial_capital, monthly_contribution, years, start_price, annual_app_pct, apy_pct, exit_fee_pct)
df = res["df"]

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Valeur finale après frais", f"{currency} {res['final_net_value']:,.0f}")
c2.metric("Valeur finale brute", f"{currency} {res['gross_final_value']:,.0f}")
c3.metric("Total investi", f"{currency} {res['invested']:,.0f}")
c4.metric("Frais de sortie", f"{currency} {res['exit_fee_amount']:,.0f}")
c5.metric(f"Volume final ({unit_label})", f"{res['final_units']:,.4f} {unit_label}")

# Chart: Red = value with yield, Blue = invested only; single y-axis
st.subheader("Évolution du portefeuille")
value_line = alt.Chart(df).mark_line(color="#E11D48", strokeWidth=2).encode(
    x="Mois:Q",
    y=alt.Y("Valeur:Q", axis=alt.Axis(title=f"Valeur ({currency})")),
    tooltip=["Mois","Valeur"]
).properties(title="Rouge = Monnaie + YIELD, Bleu = Monnaie seule")

invested_line = alt.Chart(df).mark_line(color="#2563EB", strokeDash=[4,4]).encode(
    x="Mois:Q",
    y=alt.Y("Investi:Q"),
    tooltip=["Mois","Investi"]
)

chart = alt.layer(value_line, invested_line)
st.altair_chart(chart, use_container_width=True)

# Full table
st.subheader("Tableau (toute la durée)")
st.dataframe(df, use_container_width=True, hide_index=True)

# CSV
st.download_button("📥 Télécharger le CSV", df.to_csv(index=False).encode("utf-8"),
                   file_name=f"simulation_{strategy.lower()}.csv", mime="text/csv")

st.caption("**Simulation éducative** — ceci n'est pas un conseil en investissement.")
