import fitz  # PyMuPDF
import re
import textstat  # For readability score

# -----------------------------
# 1. Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# -----------------------------
# 2. Extract features from text
# -----------------------------
def extract_features(text):
    num_citations = len(re.findall(r"\[\d+\]", text)) + len(re.findall(r"\(\d{4}\)", text))
    num_figures = len(re.findall(r"Figure \d+|Fig. \d+", text, re.IGNORECASE))
    num_equations = len(re.findall(r"\$.*?\$", text))  # Roughly count inline math
    words = text.split()
    total_words = len(words)

    sentences = re.split(r'[.!?]', text)
    sentence_lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
    avg_sentence_length = round(sum(sentence_lengths) / len(sentence_lengths), 2) if sentence_lengths else 0

    return {
        "num_citations": num_citations,
        "num_figures": num_figures,
        "num_equations": num_equations,
        "total_words": total_words,
        "avg_sentence_length": avg_sentence_length
    }

# -----------------------------
# 3. Calculate Readability Score
# -----------------------------
def get_readability_score(text):
    try:
        score = textstat.flesch_reading_ease(text)
        return round(score, 2)
    except:
        return 0.0
