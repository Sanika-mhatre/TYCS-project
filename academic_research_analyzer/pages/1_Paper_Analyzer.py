import streamlit as st
import os
from utils.pdf_utils import extract_text_from_pdf, extract_features
from utils.structure_predictor import predict_scores
from utils.grammar_checker import check_grammar
from utils.plagiarism_checker import check_plagiarism
from utils.citation_analyzer import analyze_citations
from utils.keyword_extractor import extract_keywords
from utils.report_generator import generate_pdf_report

st.set_page_config(page_title="Paper Analyzer", layout="wide")

st.markdown(
    "<h2 style='color:#4A7EBB;'>📄 Academic Paper Analyzer</h2>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("📎 Upload a research paper (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting and analyzing..."):
        temp_path = "temp_uploaded.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract text
        text = extract_text_from_pdf(temp_path)

        # Extract features for ML model
        features = extract_features(text)

        # Predict novelty and clarity
        novelty_score, clarity_score = predict_scores(features)

        # Grammar Check
        grammar_results = check_grammar(text)
        matches = grammar_results.get("matches", []) if isinstance(grammar_results, dict) else []

        # Plagiarism Check
        plagiarism_result = check_plagiarism(text)
        plagiarism_percent = plagiarism_result.get("plagiarism_percent", 0.0)

        # Citation Analysis
        citation_count = analyze_citations(text)

        # Keywords
        keywords = extract_keywords(text)

    # Results Section
    st.success("✅ Analysis Complete!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Novelty Score", f"{novelty_score:.2f} / 1.0")
    with col2:
        st.metric("✍️ Clarity Score", f"{clarity_score:.2f} / 1.0")
    with col3:
        st.metric("📄 Plagiarism", f"{plagiarism_percent:.2f}%")

    st.metric("🔖 Citations", citation_count["count"])
    st.write("🔢 Citation Breakdown:")
    st.markdown(f"- 📚 Bracket Style: **{citation_count['bracket_style']}**")
    st.markdown(f"- 🧾 Author-Year Style: **{citation_count['author_year_style']}**")

    st.markdown("### 🔑 Extracted Keywords")
    st.code(", ".join(keywords))

    st.markdown("---")
    st.markdown("### 🧹 Grammar Suggestions")
    if matches:
        for m in matches:
            context = m.get("context", {}).get("text", "")
            offset = m.get("context", {}).get("offset", 0)
            length = m.get("context", {}).get("length", 0)
            error_text = context[offset:offset+length]
            message = m.get("message", "")
            replacements = [r["value"] for r in m.get("replacements", [])]
            st.markdown(f"**⚠️ Error:** `{error_text}`")
            st.markdown(f"**📌 Message:** {message}")
            if replacements:
                st.markdown(f"**✅ Suggestions:** {', '.join(replacements)}")
            st.markdown("---")
    else:
        st.success("✅ No major grammar issues found.")

    st.markdown("### 📃 Full Extracted Text")
    with st.expander("Click to view full text"):
        st.text_area("PDF Text", value=text, height=300)

    # Export button
    if st.button("📤 Download Analysis Report (PDF)"):
        output_path = generate_pdf_report(
            text, novelty_score, clarity_score, plagiarism_percent,
            citation_count, keywords, matches
        )
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download Report", data=f, file_name="analysis_report.pdf", mime="application/pdf")
