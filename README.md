# FinSight — GenAI-Powered Financial Intelligence & Risk Analysis

FinSight is a GenAI-powered financial intelligence system that combines Retrieval-Augmented Generation (RAG), financial analytics, and Machine Learning to simplify the analysis of corporate annual reports.

Users can upload annual reports in PDF format, ask questions in natural language, explore financial indicators, and receive ML-based financial distress predictions through an interactive dashboard.

## Key Features

- **PDF Processing:** Extracts and processes text from uploaded annual reports using PyMuPDF.
- **Semantic Search:** Uses Sentence Transformers to generate embeddings and FAISS for similarity-based document retrieval.
- **AI-Powered Q&A:** Integrates Google Gemini to generate context-aware answers using retrieved document content.
- **Source References:** Displays relevant page numbers and retrieved text excerpts.
- **Financial Analysis:** Extracts and calculates revenue, revenue growth, gross margin, operating margin, net margin, debt-to-equity, ROE, and free cash flow.
- **Financial Risk Assessment:** Uses a Logistic Regression classifier to estimate bankruptcy risk from seven engineered financial features.
- **Interactive Dashboard:** Combines document Q&A, financial analysis, and risk assessment using Streamlit.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Frontend / Dashboard | Streamlit |
| PDF Processing | PyMuPDF |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| LLM | Google Gemini API |
| Machine Learning | Scikit-learn, Logistic Regression |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |

## System Architecture

### RAG Pipeline

```text
Annual Report PDF
       |
       v
   PyMuPDF
       |
       v
 Text Extraction
       |
       v
  Text Chunking
       |
       v
Sentence Transformers
       |
       v
   FAISS Index
       |
       v
 User Query
       |
       v
Semantic Retrieval
       |
       v
Keyword-based Reranking
       |
       v
  Google Gemini
       |
       v
Source-grounded Answer
```

### Machine Learning Pipeline

```text
Financial Statements
        |
        v
Financial Data Extraction
        |
        v
Feature Engineering
        |
        v
7 Financial Features
        |
        v
Logistic Regression
        |
        v
Risk Probability
        |
        v
Risk Assessment Dashboard
```

## Machine Learning Performance

The Logistic Regression model was trained using the UCI Taiwanese Bankruptcy Prediction dataset.

- Model: Logistic Regression
- Class imbalance handling: `class_weight="balanced"`
- Input features: 7 engineered financial features
- ROC-AUC: 0.918
- Bankruptcy recall: Approximately 84%
- Bankruptcy precision: Approximately 16%

*Performance is based on the project's held-out test set. Predictions are preliminary risk estimates, not investment recommendations.*

## Project Structure

```text
FinSight/
│
├── rag/
│   ├── loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── vector_store.py
│   ├── generator.py
│   ├── document.py
│   ├── pipeline.py
│   ├── financials.py
│   └── risk.py
│
├── models/
│   └── risk_model.pkl
│
├── data/
├── .streamlit/
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mayank-anand1/FinSight.git
cd FinSight
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key

Obtain an API key through [Google AI Studio](https://aistudio.google.com/).

Set the environment variable:

```bash
export GEMINI_API_KEY="your_api_key"
```

Never commit API keys or secrets to GitHub.

### 5. Run the application

```bash
python3 -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Future Enhancements

- Improve financial statement extraction across different company formats.
- Add OCR and improved financial table extraction.
- Implement hybrid retrieval and neural reranking.
- Improve bankruptcy classification through threshold tuning and model experimentation.
- Add multi-year and multi-company financial comparisons.
- Introduce persistent database storage and cloud deployment.

## Author

**Mayank Anand**

GitHub: [mayank-anand1](https://github.com/mayank-anand1)