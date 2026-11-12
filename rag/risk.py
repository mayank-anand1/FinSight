import joblib
import pandas as pd


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "models/risk_model.pkl"
)


# ==========================================
# FEATURE NAMES
# ==========================================

FEATURE_NAMES = [
    "Operating_Gross_Margin",
    "Operating_Profit_Rate",
    "Debt_Ratio",
    "Net_Income_to_Assets",
    "Net_Income_to_Equity",
    "Liability_to_Equity",
    "Cash_Flow_to_Assets",
]


# ==========================================
# FEATURE DISPLAY NAMES
# ==========================================

DISPLAY_NAMES = {
    "Operating_Gross_Margin": "Operating Gross Margin",
    "Operating_Profit_Rate": "Operating Profit Rate",
    "Debt_Ratio": "Debt Ratio",
    "Net_Income_to_Assets": "Net Income / Assets",
    "Net_Income_to_Equity": "Net Income / Equity",
    "Liability_to_Equity": "Liability / Equity",
    "Cash_Flow_to_Assets": "Cash Flow / Assets",
}


# ==========================================
# PREDICT FINANCIAL RISK
# ==========================================

def predict_risk(features):
    """
    Predict financial risk and return
    feature-level explanations.
    """

    # --------------------------------------
    # CREATE INPUT DATA
    # --------------------------------------

    input_data = pd.DataFrame(
        [
            [
                features[name]
                for name in FEATURE_NAMES
            ]
        ],
        columns=FEATURE_NAMES,
    )

    # --------------------------------------
    # PREDICTION
    # --------------------------------------

    probability = float(
        model.predict_proba(
            input_data
        )[0][1]
    )

    prediction = int(
        model.predict(
            input_data
        )[0]
    )

    # --------------------------------------
    # GET MODEL COEFFICIENTS
    # --------------------------------------

    classifier = model.named_steps[
        "classifier"
    ]

    coefficients = (
        classifier.coef_[0]
    )

    # --------------------------------------
    # CALCULATE CONTRIBUTIONS
    # --------------------------------------

    contributions = (
        input_data.iloc[0].values
        * coefficients
    )

    explanations = []

    for name, coefficient, contribution in zip(
        FEATURE_NAMES,
        coefficients,
        contributions,
    ):

        explanations.append(
            {
                "feature": name,
                "display_name": DISPLAY_NAMES[name],
                "coefficient": float(
                    coefficient
                ),
                "contribution": float(
                    contribution
                ),
            }
        )

    # --------------------------------------
    # SORT BY ABSOLUTE IMPACT
    # --------------------------------------

    explanations.sort(
        key=lambda x: abs(
            x["contribution"]
        ),
        reverse=True,
    )

    return {
        "probability": probability,
        "prediction": prediction,
        "explanations": explanations,
    }