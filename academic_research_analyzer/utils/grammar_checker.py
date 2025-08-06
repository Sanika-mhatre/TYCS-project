import requests

def split_text(text, max_words=500):
    """
    Splits a large text into smaller chunks of max_words words each.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])

def check_grammar(text):
    """
    Checks grammar using LanguageTool API by sending smaller text chunks.
    Returns list of grammar issues (matches).
    """
    all_matches = []

    for chunk in split_text(text):
        try:
            response = requests.post(
                "https://api.languagetoolplus.com/v2/check",
                data={
                    "text": chunk,
                    "language": "en-US"
                },
                timeout=15
            )
            if response.status_code == 200:
                matches = response.json().get("matches", [])
                all_matches.extend(matches)
            else:
                print(f"⚠️ Grammar check failed: LanguageTool API error {response.status_code}")
        except Exception as e:
            print("⚠️ Grammar check failed with exception:", str(e))

    return all_matches
