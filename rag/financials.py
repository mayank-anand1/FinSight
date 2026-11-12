import re

from rag.loader import load_pdf


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def normalize_text(text):
    """
    Normalize PDF-extracted text so that
    different spacing/newline formats are easier
    to match.
    """

    text = text.replace("\u2019", "'")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_number(value):
    """
    Convert a financial number such as:
    1,234
    $1,234
    (1,234)

    into a float.
    """

    if value is None:
        return None

    value = value.replace(",", "")
    value = value.replace("$", "")
    value = value.strip()

    if value in {"-", "—", ""}:
        return 0.0

    negative = False

    if value.startswith("(") and value.endswith(")"):
        negative = True
        value = value[1:-1]

    try:
        number = float(value)
    except ValueError:
        return None

    if negative:
        number *= -1

    return number


def find_first_match(text, patterns):
    """
    Try multiple regex patterns and return
    the first successful match.
    """

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match

    return None


# ==========================================
# FIND FINANCIAL STATEMENT PAGES
# ==========================================

def find_financial_statement_pages(pdf_path):

    pages = load_pdf(pdf_path)

    statements = {
        "income_statement": [],
        "balance_sheet": [],
        "cash_flow": []
    }

    for page in pages:

        text = normalize_text(
            page["text"]
        )

        lower_text = text.lower()

        # ----------------------------------
        # INCOME STATEMENT
        # ----------------------------------

        income_keywords = [
            "statements of income",
            "statement of income",
            "statements of operations",
            "statement of operations",
            "statements of earnings",
            "statement of earnings",
            "statements of profit",
            "income statement",
            "consolidated income statements",
            "consolidated statements of operations",
        ]

        income_found = any(
            keyword in lower_text
            for keyword in income_keywords
        )

        income_metrics_found = sum(
            metric in lower_text
            for metric in [
                "revenue",
                "net income",
                "gross profit",
                "operating income",
                "cost of revenue",
                "total revenues",
            ]
        )

        if (
            income_found
            and income_metrics_found >= 2
        ):
            statements["income_statement"].append(
                page
            )

        # ----------------------------------
        # BALANCE SHEET
        # ----------------------------------

        balance_keywords = [
            "balance sheets",
            "balance sheet",
            "consolidated balance sheets",
            "consolidated balance sheet",
            "statements of financial position",
            "statement of financial position",
        ]

        balance_found = any(
            keyword in lower_text
            for keyword in balance_keywords
        )

        balance_metrics_found = sum(
            metric in lower_text
            for metric in [
                "total assets",
                "total liabilities",
                "total equity",
                "shareholders' equity",
                "stockholders' equity",
            ]
        )

        if (
            balance_found
            and balance_metrics_found >= 2
        ):
            statements["balance_sheet"].append(
                page
            )

        # ----------------------------------
        # CASH FLOW
        # ----------------------------------

        cash_flow_keywords = [
            "statements of cash flows",
            "statement of cash flows",
            "consolidated statements of cash flows",
            "consolidated statement of cash flows",
            "cash flow statement",
        ]

        cash_flow_found = any(
            keyword in lower_text
            for keyword in cash_flow_keywords
        )

        cash_flow_metrics_found = sum(
            metric in lower_text
            for metric in [
                "operating activities",
                "investing activities",
                "financing activities",
                "net cash",
            ]
        )

        if (
            cash_flow_found
            and cash_flow_metrics_found >= 1
        ):
            statements["cash_flow"].append(
                page
            )

    return statements


# ==========================================
# INCOME STATEMENT
# ==========================================

def extract_income_statement(page):

    text = normalize_text(
        page["text"]
    )

    metrics = {}

    patterns = {

        "revenue": [
            r"\bRevenue\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"\bRevenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"\bTotal revenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],

        "cost_of_revenue": [
            r"Cost of revenue\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
            r"Cost of revenues\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
            r"Cost of sales\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        ],

        "gross_profit": [
    r"Gross profit\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
    r"Gross income\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
    r"Gross margin\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
],

        "operating_income": [
            r"Operating income\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
            r"Income from operations\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
            r"Operating profit\s+\$?\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        ],

        "net_income": [
            r"Net income\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Net earnings\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Net profit\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],
    }

    for metric, metric_patterns in patterns.items():

        match = find_first_match(
            text,
            metric_patterns
        )

        if match:

            metrics[metric] = {
                "2026": extract_number(
                    match.group(1)
                ),
                "2025": extract_number(
                    match.group(2)
                ),
                "2024": extract_number(
                    match.group(3)
                ),
            }

    return metrics


# ==========================================
# MARGINS
# ==========================================

def calculate_margins(metrics):

    results = {}

    required_metrics = [
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income",
    ]

    if not all(
        metric in metrics
        for metric in required_metrics
    ):
        return results

    for year in [
        "2026",
        "2025",
        "2024"
    ]:

        revenue = metrics["revenue"].get(year)

        if not revenue:
            continue

        results[year] = {
            "gross_margin": (
                metrics["gross_profit"][year]
                / revenue
            ) * 100,

            "operating_margin": (
                metrics["operating_income"][year]
                / revenue
            ) * 100,

            "net_margin": (
                metrics["net_income"][year]
                / revenue
            ) * 100,
        }

    return results


# ==========================================
# REVENUE GROWTH
# ==========================================

def calculate_revenue_growth(metrics):

    if "revenue" not in metrics:
        return None

    revenue_2026 = metrics["revenue"].get(
        "2026"
    )

    revenue_2025 = metrics["revenue"].get(
        "2025"
    )

    if not revenue_2026 or not revenue_2025:
        return None

    growth = (
        (revenue_2026 - revenue_2025)
        / revenue_2025
    ) * 100

    return growth


# ==========================================
# BALANCE SHEET
# ==========================================

def extract_balance_sheet(page):

    text = normalize_text(
        page["text"]
    )

    metrics = {}

    patterns = {

        "total_assets": [
            r"Total assets\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],

        "total_liabilities": [
            r"Total liabilities\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Total liabilities and equity\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],

        "total_equity": [
            r"Total shareholders['’]? equity\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Total stockholders['’]? equity\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Total equity\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],

        "short_term_debt": [
            r"Short-term debt\s+\$?\s*([\d,]+)\s+\$?\s*(?:([\d,]+)|[-—])",
            r"Current portion of long-term debt\s+\$?\s*([\d,]+)\s+\$?\s*(?:([\d,]+)|[-—])",
        ],

        "long_term_debt": [
            r"Long-term debt\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
            r"Long term debt\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)",
        ],
    }

    for metric, metric_patterns in patterns.items():

        match = find_first_match(
            text,
            metric_patterns
        )

        if not match:
            continue

        value_2026 = extract_number(
            match.group(1)
        )

        value_2025 = extract_number(
            match.group(2)
        )

        if value_2025 is None:
            value_2025 = 0.0

        metrics[metric] = {
            "2026": value_2026,
            "2025": value_2025,
        }

    return metrics


# ==========================================
# DEBT TO EQUITY
# ==========================================

def calculate_debt_to_equity(
    balance_sheet
):

    required = [
        "short_term_debt",
        "long_term_debt",
        "total_equity",
    ]

    if not all(
        metric in balance_sheet
        for metric in required
    ):
        return None

    short_term_debt = (
        balance_sheet[
            "short_term_debt"
        ]["2026"]
    )

    long_term_debt = (
        balance_sheet[
            "long_term_debt"
        ]["2026"]
    )

    total_equity = (
        balance_sheet[
            "total_equity"
        ]["2026"]
    )

    if not total_equity:
        return None

    total_debt = (
        short_term_debt
        + long_term_debt
    )

    return total_debt / total_equity


# ==========================================
# ROE
# ==========================================

def calculate_roe(
    income_statement,
    balance_sheet
):

    if (
        "net_income" not in income_statement
        or "total_equity" not in balance_sheet
    ):
        return None

    net_income = (
        income_statement[
            "net_income"
        ]["2026"]
    )

    equity_2026 = (
        balance_sheet[
            "total_equity"
        ]["2026"]
    )

    equity_2025 = (
        balance_sheet[
            "total_equity"
        ]["2025"]
    )

    average_equity = (
        equity_2026
        + equity_2025
    ) / 2

    if not average_equity:
        return None

    roe = (
        net_income
        / average_equity
    ) * 100

    return roe


# ==========================================
# CASH FLOW
# ==========================================

def extract_cash_flow(page):

    text = normalize_text(
        page["text"]
    )

    metrics = {}

    operating_cash_flow_patterns = [

        r"Net cash provided by operating activities\s+\$?\s*([\d,]+)",

        r"Net cash provided by \(used in\) operating activities\s+\$?\s*([\d,]+)",

        r"Cash provided by operating activities\s+\$?\s*([\d,]+)",

        r"Net cash from operating activities\s+\$?\s*([\d,]+)",
    ]

    capital_expenditure_patterns = [

        r"Purchases related to property and equipment and intangible assets\s+\(([\d,]+)\)",

        r"Purchases of property and equipment\s+\(([\d,]+)\)",

        r"Capital expenditures\s+\(([\d,]+)\)",

        r"Capital expenditures\s+\$?\s*([\d,]+)",
    ]

    match = find_first_match(
        text,
        operating_cash_flow_patterns
    )

    if match:
        metrics["operating_cash_flow"] = (
            extract_number(match.group(1))
        )

    match = find_first_match(
        text,
        capital_expenditure_patterns
    )

    if match:
        metrics["capital_expenditures"] = (
            extract_number(match.group(1))
        )

    return metrics


# ==========================================
# FREE CASH FLOW
# ==========================================

def calculate_free_cash_flow(
    cash_flow
):

    if (
        "operating_cash_flow"
        not in cash_flow
        or "capital_expenditures"
        not in cash_flow
    ):
        return None

    operating_cash_flow = (
        cash_flow[
            "operating_cash_flow"
        ]
    )

    capital_expenditures = (
        cash_flow[
            "capital_expenditures"
        ]
    )

    return (
        operating_cash_flow
        - capital_expenditures
    )
    
def calculate_risk_features(
    income_statement,
    balance_sheet,
    cash_flow,
):
    """
    Convert extracted financial statement values
    into the seven features expected by the
    trained risk model.
    """

    revenue = income_statement["revenue"]["2026"]
    gross_profit = income_statement["gross_profit"]["2026"]
    operating_income = income_statement["operating_income"]["2026"]
    net_income = income_statement["net_income"]["2026"]

    total_assets = balance_sheet["total_assets"]["2026"]
    total_liabilities = balance_sheet["total_liabilities"]["2026"]
    total_equity = balance_sheet["total_equity"]["2026"]

    operating_cash_flow = cash_flow["operating_cash_flow"]

    features = {
        "Operating_Gross_Margin": (
            gross_profit / revenue
        ),

        "Operating_Profit_Rate": (
            operating_income / revenue
        ),

        "Debt_Ratio": (
            total_liabilities / total_assets
        ),

        "Net_Income_to_Assets": (
            net_income / total_assets
        ),

        "Net_Income_to_Equity": (
            net_income / total_equity
        ),

        "Liability_to_Equity": (
            total_liabilities / total_equity
        ),

        "Cash_Flow_to_Assets": (
            operating_cash_flow / total_assets
        ),
    }

    return features