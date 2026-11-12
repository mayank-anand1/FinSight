import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("data/data.csv")


# ==========================================
# CREATE FEATURES
# ==========================================

df["Operating_Gross_Margin"] = (
    df[" Operating Gross Margin"]
)

df["Operating_Profit_Rate"] = (
    df[" Operating Profit Rate"]
)

df["Debt_Ratio"] = (
    df[" Debt ratio %"]
)

df["Net_Income_to_Assets"] = (
    df[" Net Income to Total Assets"]
)

df["Net_Income_to_Equity"] = (
    df[" Net Income to Stockholder's Equity"]
)

df["Liability_to_Equity"] = (
    df[" Liability to Equity"]
)

df["Cash_Flow_to_Assets"] = (
    df[" Cash Flow to Total Assets"]
)


# ==========================================
# FEATURE LIST
# ==========================================

features = [
    "Operating_Gross_Margin",
    "Operating_Profit_Rate",
    "Debt_Ratio",
    "Net_Income_to_Assets",
    "Net_Income_to_Equity",
    "Liability_to_Equity",
    "Cash_Flow_to_Assets",
]


X = df[features]
y = df["Bankrupt?"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


# ==========================================
# MODEL
# ==========================================

model = Pipeline(
    [
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "classifier",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            ),
        ),
    ]
)


# ==========================================
# TRAIN
# ==========================================

model.fit(
    X_train,
    y_train,
)


# ==========================================
# PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)

y_probability = (
    model.predict_proba(X_test)[:, 1]
)


# ==========================================
# EVALUATION
# ==========================================

print("\n")
print("=" * 60)
print("LOGISTIC REGRESSION - 7 FEATURES")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Non-Bankrupt",
            "Bankrupt",
        ],
    )
)


print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred,
    )
)


print("\nROC-AUC:")

print(
    roc_auc_score(
        y_test,
        y_probability,
    )
)

import joblib

joblib.dump(
    model,
    "models/risk_model.pkl"
)

print("\nModel saved to models/risk_model.pkl")