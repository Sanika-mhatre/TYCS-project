import difflib

def check_plagiarism(text):
    # Simulated local database of sample sentences
    known_sentences = [
        "Machine learning is a subfield of artificial intelligence.",
        "Deep learning models are based on neural networks.",
        "The results suggest a significant improvement over traditional methods.",
        "Future work may explore the use of reinforcement learning.",
        "The paper provides an overview of the existing literature."
    ]

    input_sentences = text.split('.')
    matched_sentences = []

    for sentence in input_sentences:
        for known in known_sentences:
            similarity = difflib.SequenceMatcher(None, sentence.strip().lower(), known.lower()).ratio()
            if similarity > 0.8:
                matched_sentences.append(sentence.strip())
                break

    # Calculate percentage
    total = len(input_sentences)
    percent = (len(matched_sentences) / total) * 100 if total > 0 else 0.0

    return {
        "plagiarism_percent": percent,
        "matched_sentences": matched_sentences
    }
