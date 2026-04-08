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


def find_most_relevant_scheme(query_embedding: list[float], stored_schemes: list[dict]) -> dict | None:
    """
    1. Compares the Math Vector of a User's Query to every Scheme Vector in our Database.
    2. Identifies the highest score, representing the most conceptually similar scheme.
    3. Returns the winning scheme dictionary.
    """
    if not stored_schemes:
        return None

    best_scheme = None
    # Start at the absolute lowest possible score (-1.0)
    highest_score = -1.0 

    for scheme in stored_schemes:
        scheme_embedding = scheme.get("embedding", [])
        
        # Skip schemes that haven't been seeded properly with an embedding
        if not scheme_embedding:
            continue

        # Calculate semantic similarity
        score = calculate_cosine_similarity(query_embedding, scheme_embedding)
        
        # If this scheme's score beats our previous highest score, we have a new winner!
        if score > highest_score:
            highest_score = score
            best_scheme = scheme
            
    # Attach a confidence score so the frontend (or logs) knows how strong the match was
    if best_scheme:
        best_scheme["ai_confidence_score"] = highest_score

    return best_scheme
