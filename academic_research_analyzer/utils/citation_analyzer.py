import re

def analyze_citations(text):
    """
    Simple citation detection by common academic formats:
    - [1], [2]
    - (Author, Year)
    - Author (Year)
    """
    square_bracket_citations = re.findall(r'\[\d+\]', text)
    author_year_citations = re.findall(r'\([A-Z][a-z]+, \d{4}\)', text)

    total = len(square_bracket_citations) + len(author_year_citations)

    return {
        "count": total,
        "bracket_style": len(square_bracket_citations),
        "author_year_style": len(author_year_citations)
    }

