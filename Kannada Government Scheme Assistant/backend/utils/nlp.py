import re
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------
# Load our Multilingual Model
# ---------------------------------------------------------
# 'paraphrase-multilingual-MiniLM-L12-v2' is a lightweight, widely-used AI model 
# that understands 50+ languages, including Kannada! It converts sentences into 
# a 384-dimensional mathematical space (vector embedding).
try:
    print("Loading multilingual AI model (this may take a few seconds on first run)...")
    # This automatically downloads the model the very first time you run it.
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
except Exception as e:
    print(f"Warning: Could not load the model. Error: {e}")
    model = None


def clean_kannada_text(text: str) -> str:
    """
    1. Removes English/general punctuation (like !, ?, , .)
    2. Keeps Kannada characters, Standard English alphanumeric, and spaces.
    """
    if not text:
        return ""
        
    # The regex r'[^\w\s\u0C80-\u0CFF]' means:
    # Remove anything that is NOT a Word (\w), Space (\s), or Kannada Character (\u0C80-\u0CFF)
    cleaned_text = re.sub(r'[^\w\s\u0C80-\u0CFF]', '', text)
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def tokenize_text(cleaned_text: str) -> list:
    """
    1. Splits the cleaned sentence into individual words (tokens).
    2. For a simple academic project, splitting by empty spaces works perfectly for Kannada.
    """
    if not cleaned_text:
        return []
    
    tokens = cleaned_text.split(' ')
    # Filter out any completely empty strings just in case
    tokens = [word for word in tokens if word]
    
    return tokens


def generate_embedding(text: str) -> list[float]:
    """
    1. Takes raw Kannada sentence
    2. Cleans it using our `clean_kannada_text` function
    3. Converts it into AI Vector Embeddings.
    """
    if model is None:
        raise RuntimeError("Cannot generate embedding because the AI model failed to load.")
        
    # Step 1: Preprocess the input
    cleaned_sentence = clean_kannada_text(text)
    
    # Step 2: Feed the cleaned Kannada text to our multilingual model
    # model.encode() spits out a Numpy Array containing numbers like [0.12, -0.45, 0.99...]
    embedding_array = model.encode(cleaned_sentence)
    
    # Step 3: Convert the Numpy array to a standard Python List so MongoDB can save it easily
    return embedding_array.tolist()
