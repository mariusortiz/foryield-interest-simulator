# common.py
import pandas as pd

def apy_to_monthly(apy: float) -> float:
    return (1 + apy) ** (1/12) - 1

def annual_to_monthly_growth(annual: float) -> float:
    base = 1 + annual
    if base <= 1e-6:
        return -0.999999
    return base ** (1/12) - 1

def simulate(initial_capital, monthly_contribution, years, start_price, annual_app_pct, apy_pct, exit_fee_pct):
    months = int(years * 12)
    r_price = annual_to_monthly_growth(annual_app_pct / 100.0)
    r_yield = apy_to_monthly(apy_pct / 100.0)
    exit_fee = max(0.0, min(exit_fee_pct / 100.0, 1.0))

    price_series = [start_price * ((1 + r_price) ** k) for k in range(months + 1)]

    invested = initial_capital
    units_no_yield = initial_capital / start_price
    units = units_no_yield

    rows = [{
        "Mois": 0,
        "Prix": price_series[0],
        "Unités": units,
        "Valeur": units * price_series[0],
        "Investi": invested,
    }]

    for k in range(1, months + 1):
        units *= (1 + r_yield)
        pk = price_series[k]
        if monthly_contribution > 0:
            invested += monthly_contribution
            add_units = monthly_contribution / pk
            units_no_yield += add_units
            units += add_units
        rows.append({"Mois": k, "Prix": pk, "Unités": units, "Valeur": units * pk, "Investi": invested})

    final_price = price_series[months]
    gross_final_value = units * final_price
    exit_fee_amount = exit_fee * gross_final_value
    final_net_value = gross_final_value - exit_fee_amount
    extra_units_from_yield = max(units - units_no_yield, 0)
    yield_value_component = extra_units_from_yield * final_price

    import pandas as pd
    df = pd.DataFrame(rows)
    return {
        "df": df,
        "gross_final_value": gross_final_value,
        "final_net_value": final_net_value,
        "invested": invested,
        "exit_fee_amount": exit_fee_amount,
        "yield_value_component": yield_value_component,
        "final_units": units,
        "final_price": final_price,
    }
