import os

import streamlit as st

from rag.embeddings import model
from rag.financials import (
    calculate_debt_to_equity,
    calculate_free_cash_flow,
    calculate_margins,
    calculate_roe,
    calculate_revenue_growth,
    extract_balance_sheet,
    extract_cash_flow,
    extract_income_statement,
    find_financial_statement_pages,
)
from rag.generator import generate_answer
from rag.pipeline import build_knowledge_base
from rag.reranker import rerank_results


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="FinSight",
    page_icon="📊",
    layout="wide",
)


# ==========================================
# SESSION STATE
# ==========================================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "document_pages" not in st.session_state:
    st.session_state.document_pages = None

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = None

if "financials" not in st.session_state:
    st.session_state.financials = None


# ==========================================
# HEADER
# ==========================================

st.title("📊 FinSight")

st.write(
    "Upload a financial report and ask questions "
    "using AI-powered document analysis."
)


# ==========================================
# PDF UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)


# ==========================================
# PROCESS PDF
# ==========================================

if uploaded_file is not None:

    # Only process when a new document is uploaded
    if st.session_state.document_name != uploaded_file.name:

        os.makedirs("data", exist_ok=True)

        pdf_path = os.path.join(
            "data",
            uploaded_file.name,
        )

        with open(pdf_path, "wb") as file:
            file.write(
                uploaded_file.getbuffer()
            )

        # --------------------------------------
        # PROCESS DOCUMENT
        # --------------------------------------

        with st.spinner(
            "Processing document..."
        ):

            retriever = build_knowledge_base(
                pdf_path
            )

        # --------------------------------------
        # ANALYZE FINANCIAL STATEMENTS
        # --------------------------------------

        with st.spinner(
            "Analyzing financial statements..."
        ):

            statements = find_financial_statement_pages(
                pdf_path
            )

            financials = None

            # ----------------------------------
            # CHECK AVAILABLE STATEMENTS
            # ----------------------------------

            has_income_statement = bool(
                statements["income_statement"]
            )

            has_balance_sheet = bool(
                statements["balance_sheet"]
            )

            has_cash_flow = bool(
                statements["cash_flow"]
            )

            # ----------------------------------
            # INCOME STATEMENT
            # ----------------------------------

            if has_income_statement:

                income_statement = (
                    extract_income_statement(
                        statements[
                            "income_statement"
                        ][0]
                    )
                )

            else:

                income_statement = {}

            # ----------------------------------
            # BALANCE SHEET
            # ----------------------------------

            if has_balance_sheet:

                balance_sheet = (
                    extract_balance_sheet(
                        statements[
                            "balance_sheet"
                        ][0]
                    )
                )

            else:

                balance_sheet = {}

            # ----------------------------------
            # CASH FLOW
            # ----------------------------------

            if has_cash_flow:

                cash_flow = (
                    extract_cash_flow(
                        statements[
                            "cash_flow"
                        ][0]
                    )
                )

            else:

                cash_flow = {}

            # ----------------------------------
            # CALCULATE FINANCIAL METRICS
            # ----------------------------------

            margins = calculate_margins(
                income_statement
            )

            revenue_growth = (
                calculate_revenue_growth(
                    income_statement
                )
            )

            debt_to_equity = (
                calculate_debt_to_equity(
                    balance_sheet
                )
            )

            roe = calculate_roe(
                income_statement,
                balance_sheet,
            )

            free_cash_flow = (
                calculate_free_cash_flow(
                    cash_flow
                )
            )

            # ----------------------------------
            # CREATE FINANCIAL DASHBOARD DATA
            # ----------------------------------

            if (
                income_statement
                and margins
                and revenue_growth is not None
                and debt_to_equity is not None
                and roe is not None
                and free_cash_flow is not None
            ):

                financials = {
                    "income_statement": (
                        income_statement
                    ),
                    "balance_sheet": (
                        balance_sheet
                    ),
                    "cash_flow": (
                        cash_flow
                    ),
                    "margins": margins,
                    "revenue_growth": (
                        revenue_growth
                    ),
                    "debt_to_equity": (
                        debt_to_equity
                    ),
                    "roe": roe,
                    "free_cash_flow": (
                        free_cash_flow
                    ),
                }

        # --------------------------------------
        # STORE DOCUMENT INFORMATION
        # --------------------------------------

        st.session_state.retriever = retriever

        st.session_state.document_name = (
            uploaded_file.name
        )

        st.session_state.document_chunks = len(
            retriever.chunks
        )

        st.session_state.document_pages = len(
            set(
                chunk["page"]
                for chunk in retriever.chunks
            )
        )

        # --------------------------------------
        # STORE FINANCIAL INFORMATION
        # --------------------------------------

        st.session_state.financials = financials

        st.success(
            "Document processed successfully!"
        )


# ==========================================
# DOCUMENT INFORMATION
# ==========================================

if st.session_state.retriever is not None:

    st.divider()

    st.subheader("📄 Document")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "File",
            st.session_state.document_name,
        )

    with col2:
        st.metric(
            "Pages",
            st.session_state.document_pages,
        )

    with col3:
        st.metric(
            "Chunks",
            st.session_state.document_chunks,
        )

    # ======================================
    # FINANCIAL OVERVIEW
    # ======================================

    if st.session_state.financials is not None:

        st.divider()

        st.subheader(
            "📊 Financial Overview"
        )

        financials = (
            st.session_state.financials
        )

        # ----------------------------------
        # FIRST ROW
        # ----------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Revenue",
                (
                    f"${financials['income_statement']['revenue']['2026'] / 1000:.1f}B"
                ),
            )

        with col2:
            st.metric(
                "Revenue Growth",
                (
                    f"{financials['revenue_growth']:.1f}%"
                ),
            )

        with col3:
            st.metric(
                "Gross Margin",
                (
                    f"{financials['margins']['2026']['gross_margin']:.1f}%"
                ),
            )

        with col4:
            st.metric(
                "Net Margin",
                (
                    f"{financials['margins']['2026']['net_margin']:.1f}%"
                ),
            )

        # ----------------------------------
        # SECOND ROW
        # ----------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Operating Margin",
                (
                    f"{financials['margins']['2026']['operating_margin']:.1f}%"
                ),
            )

        with col2:
            st.metric(
                "Debt / Equity",
                (
                    f"{financials['debt_to_equity']:.3f}x"
                ),
            )

        with col3:
            st.metric(
                "ROE",
                (
                    f"{financials['roe']:.1f}%"
                ),
            )

        with col4:
            st.metric(
                "Free Cash Flow",
                (
                    f"${financials['free_cash_flow'] / 1000:.1f}B"
                ),
            )

    # ======================================
    # QUESTION
    # ======================================

    st.divider()

    st.subheader(
        "💬 Ask FinSight"
    )

    question = st.text_input(
        "Ask a question about the document",
        placeholder=(
            "Example: What are the major business risks?"
        ),
    )

    # ======================================
    # ANALYZE QUESTION
    # ======================================

    if st.button(
        "🔍 Analyze",
        type="primary",
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the document and generating an answer..."
            ):

                # ----------------------------------
                # EMBED QUESTION
                # ----------------------------------

                query_embedding = model.encode(
                    [question],
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )

                # ----------------------------------
                # RETRIEVE
                # ----------------------------------

                results = (
                    st.session_state.retriever.search(
                        query_embedding,
                        k=10,
                    )
                )

                # ----------------------------------
                # KEYWORDS
                # ----------------------------------

                stop_words = {
                    "what",
                    "are",
                    "the",
                    "is",
                    "a",
                    "an",
                    "of",
                    "in",
                    "for",
                    "to",
                    "how",
                    "did",
                    "was",
                    "were",
                }

                keywords = [
                    word.lower().strip(
                        "?,.!'\""
                    )
                    for word in question.split()
                    if word.lower().strip(
                        "?,.!'\""
                    ) not in stop_words
                ]

                # ----------------------------------
                # RERANK
                # ----------------------------------

                results = rerank_results(
                    results,
                    keywords,
                    top_k=5,
                )

                # ----------------------------------
                # GEMINI
                # ----------------------------------

                answer = generate_answer(
                    question,
                    results,
                )

            # ======================================
            # ANSWER
            # ======================================

            st.divider()

            st.subheader(
                "🤖 FinSight Answer"
            )

            st.write(answer)

            # ======================================
            # SOURCES
            # ======================================

            st.subheader(
                "📚 Sources"
            )

            for result in results:

                with st.expander(
                    f"Page {result['page']} "
                    f"· Similarity "
                    f"{result['score']:.4f}"
                ):

                    st.write(
                        result["text"]
                    )