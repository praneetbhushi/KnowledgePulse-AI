import re


def calculate_quality_score(
    text: str,
    filename: str,
    file_size: int,
    is_duplicate: bool = False,
):
    score = 100

    if not text or not text.strip():
        return {
            "quality_score": 0,
            "quality_level": "Poor",
        }

    text = text.strip()

    # ========================================
    # 1. Content length
    # ========================================

    text_length = len(text)

    if text_length < 100:
        score -= 40

    elif text_length < 500:
        score -= 20

    elif text_length < 1000:
        score -= 10

    # ========================================
    # 2. Word count
    # ========================================

    words = text.split()
    word_count = len(words)

    if word_count < 20:
        score -= 20

    elif word_count < 100:
        score -= 10

    # ========================================
    # 3. Structure
    # ========================================

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) < 2:
        score -= 10

    # ========================================
    # 4. Sentence structure
    # ========================================

    sentences = re.split(
        r"[.!?]+",
        text,
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if len(sentences) < 2:
        score -= 10

    # ========================================
    # 5. Filename
    # ========================================

    if not filename:
        score -= 10

    # ========================================
    # 6. File size
    # ========================================

    if file_size <= 0:
        score -= 10

    # ========================================
    # 7. Duplicate
    # ========================================

    if is_duplicate:
        score -= 30

    # ========================================
    # Final score
    # ========================================

    score = max(
        0,
        min(score, 100),
    )

    # ========================================
    # Quality level
    # ========================================

    if score >= 90:
        quality_level = "Excellent"

    elif score >= 75:
        quality_level = "Good"

    elif score >= 50:
        quality_level = "Fair"

    else:
        quality_level = "Poor"

    return {
        "quality_score": round(score, 2),
        "quality_level": quality_level,
    }