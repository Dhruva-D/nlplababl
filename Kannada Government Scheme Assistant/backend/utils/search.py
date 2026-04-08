import math

def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculates the cosine similarity between two AI vectors.
    Produces a value between -1.0 (completely opposite) to 1.0 (exact match).
    """
    # Safety check: they must be valid and the exact same length
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    # Step 1: Calculate the Dot Product
    # We multiply the corresponding dimensions together and sum the results.
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Step 2: Calculate Vector Magnitudes
    # The magnitude is the geometric "length" of the vector. 
    # Calculated using the Pythagorean theorem: sqrt(x^2 + y^2 + ... z^2)
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Step 3: Cosine Similarity Formula
    return dot_product / (magnitude1 * magnitude2)


# ---------------------------------------------------------------
# Configurable threshold: change this one number to raise/lower
# the minimum quality bar for a result to be shown.
# Value is a percentage (0–100). Default: 40.0 means 40%.
# ---------------------------------------------------------------
MIN_CONFIDENCE_THRESHOLD = 40.0


def find_top_matching_schemes(
    query_embedding: list[float],
    stored_schemes: list[dict],
    top_n: int = 3,
    threshold: float = MIN_CONFIDENCE_THRESHOLD
) -> list[dict]:
    """
    1. Scores every scheme against the user query using cosine similarity.
    2. Filters out any scheme whose score is below `threshold` percent.
    3. Sorts remaining schemes highest-score-first.
    4. Returns the top N, or an empty list if nothing passes the threshold.
    """
    if not stored_schemes:
        return []

    scored_schemes = []

    for scheme in stored_schemes:
        scheme_embedding = scheme.get("embedding", [])

        # Skip schemes not yet embedded
        if not scheme_embedding:
            continue

        score = calculate_cosine_similarity(query_embedding, scheme_embedding)

        # Convert ObjectId to string for JSON serialization
        scheme["_id"] = str(scheme["_id"])

        # Express score as a clean percentage rounded to 2 decimal places
        scheme["ai_confidence_score"] = round(score * 100, 2)

        scored_schemes.append(scheme)

    # Sort highest confidence first
    sorted_schemes = sorted(scored_schemes, key=lambda x: x["ai_confidence_score"], reverse=True)

    # If the very best match is still below the threshold, nothing is relevant enough
    if not sorted_schemes or sorted_schemes[0]["ai_confidence_score"] < threshold:
        return []

    # Filter out individual results that fall below threshold, then cap at top_n
    above_threshold = [s for s in sorted_schemes if s["ai_confidence_score"] >= threshold]
    return above_threshold[:top_n]
