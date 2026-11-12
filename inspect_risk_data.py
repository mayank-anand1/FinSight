import pandas as pd

# Load dataset
df = pd.read_csv("data/data.csv")

print("Dataset shape:")
print(df.shape)

print("\nTarget distribution:")
print(df["Bankrupt?"].value_counts())

print("\nTarget percentages:")
print(df["Bankrupt?"].value_counts(normalize=True) * 100)

# Features we are considering
features = [
    " ROA(A) before interest and % after tax",
    " Operating Profit Rate",
    " Operating Gross Margin",
    " Cash flow rate",
    " Debt ratio %",
    " Current Ratio",
    " Net Income to Total Assets",
    " Net Income to Stockholder's Equity",
    " Liability to Equity",
]

print("\nFeature statistics:")
print(df[features].describe().T)

print("\nMissing values:")
print(df[features].isnull().sum())