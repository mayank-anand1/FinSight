from rag.financials import (
    find_financial_statement_pages,
    extract_income_statement,
    extract_balance_sheet,
    extract_cash_flow,
    calculate_risk_features,
)

from rag.risk import predict_risk


pdf_path = "data/annual_report.pdf"


# ==========================================
# EXTRACT FINANCIAL STATEMENTS
# ==========================================

statements = find_financial_statement_pages(
    pdf_path
)

income_statement = extract_income_statement(
    statements["income_statement"][0]
)

balance_sheet = extract_balance_sheet(
    statements["balance_sheet"][0]
)

cash_flow = extract_cash_flow(
    statements["cash_flow"][0]
)


# ==========================================
# CALCULATE RISK FEATURES
# ==========================================

features = calculate_risk_features(
    income_statement,
    balance_sheet,
    cash_flow,
)


# ==========================================
# PREDICT RISK
# ==========================================

result = predict_risk(
    features
)


# ==========================================
# DISPLAY
# ==========================================

print("\nRisk Model Input:")
print("-" * 50)

for name, value in features.items():
    print(f"{name}: {value:.6f}")


print("\nRisk Prediction:")
print("-" * 50)

print(
    f"Probability: "
    f"{result['probability'] * 100:.4f}%"
)

print(
    f"Prediction: "
    f"{result['prediction']}"
)

# ==========================================
# DISPLAY
# ==========================================

print("\nRisk Model Input:")
print("-" * 50)

for name, value in features.items():
    print(f"{name}: {value:.6f}")


print("\nRisk Prediction:")
print("-" * 50)

print(
    f"Probability: "
    f"{result['probability'] * 100:.4f}%"
)

print(
    f"Prediction: "
    f"{result['prediction']}"
)


print("\nRisk Factors:")
print("-" * 50)

for explanation in result["explanations"]:

    print(
        f"{explanation['display_name']}: "
        f"{explanation['contribution']:.4f}"
    )