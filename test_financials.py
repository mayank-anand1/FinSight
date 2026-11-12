from rag.financials import (
    find_financial_statement_pages,
    extract_income_statement,
    calculate_margins,
    calculate_revenue_growth,
    extract_balance_sheet,
    calculate_debt_to_equity,
    calculate_roe,
    extract_cash_flow
)


pdf_path = "data/annual_report.pdf"

statements = find_financial_statement_pages(pdf_path)

balance_pages = statements["balance_sheet"]

balance_sheet = extract_balance_sheet(
    balance_pages[0]
)

debt_to_equity = calculate_debt_to_equity(
    balance_sheet
)

income_pages = statements["income_statement"]

income_statement = extract_income_statement(
    income_pages[0]
)

balance_pages = statements["balance_sheet"]

balance_sheet = extract_balance_sheet(
    balance_pages[0]
)

roe = calculate_roe(
    income_statement,
    balance_sheet
)

cash_flow_pages = statements["cash_flow"]

cash_flow = extract_cash_flow(
    cash_flow_pages[0]
)

print("\n==============================")
print("EXTRACTED CASH FLOW")
print("==============================")

for metric, value in cash_flow.items():
    print(f"{metric}: {value}")
print("\n==============================")
print("EXTRACTED BALANCE SHEET")
print("==============================")

for metric, value in balance_sheet.items():
    print(f"{metric}: {value}")
    
print("\n==============================")
print("LEVERAGE ANALYSIS")
print("==============================")

print(
    f"Debt-to-Equity: "
    f"{debt_to_equity:.3f}x"
)

print("\n==============================")
print("PROFITABILITY ANALYSIS")
print("==============================")

print(
    f"ROE: {roe:.2f}%"
)