from rag.financials import (
    find_financial_statement_pages,
    extract_income_statement,
    extract_balance_sheet,
    extract_cash_flow,
    calculate_risk_features,
)


pdf_path = "data/annual_report.pdf"


# Find statements
statements = find_financial_statement_pages(pdf_path)


# Extract statements
income_statement = extract_income_statement(
    statements["income_statement"][0]
)

balance_sheet = extract_balance_sheet(
    statements["balance_sheet"][0]
)

cash_flow = extract_cash_flow(
    statements["cash_flow"][0]
)


# Calculate ML features
features = calculate_risk_features(
    income_statement,
    balance_sheet,
    cash_flow,
)


print("\nRisk model features:")
print("-" * 50)

for name, value in features.items():
    print(f"{name}: {value:.6f}")