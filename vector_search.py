import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_embeddings(words, embedding_choice='sentence_transformers', batch_size=20):  # Increased batch size for optimization
    try:
        if embedding_choice == 'gemini':
            logger.info("Using Gemini embeddings.")
            st.info("Generating embeddings with Gemini...")
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except KeyError:
                api_key = os.environ.get('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not found.")
            
            genai.configure(api_key=api_key)
            embeddings = []
            for i in range(0, len(words), batch_size):
                batch = words[i:i+batch_size]
                result = genai.embed_content(model="models/embedding-001", content=batch, task_type="SEMANTIC_SIMILARITY")
                embeddings.extend([np.array(emb) for emb in result['embedding']])
            return np.array(embeddings).astype('float32')
        else:
            logger.info("Using Sentence Transformers embeddings.")
            st.info("Generating embeddings with Sentence Transformers (optimized for Hindi)...")
            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            return model.encode(words).astype('float32')
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        st.error(f"Embedding failed: {str(e)}. Try the other option.")
        return np.zeros((len(words), 384)).astype('float32')  # Fallback zero embeddings for robustness

def find_closest_matches(doubted_words, dictionary_words, embedding_choice, threshold=0.7):
    if not dictionary_words or not doubted_words:
        logger.warning("No dictionary or doubted words provided.")
        st.warning("No words to match.")
        return {}
    
    with st.spinner("Generating embeddings..."):
        dict_emb = get_embeddings(dictionary_words, embedding_choice)
        doubted_emb = get_embeddings(doubted_words, embedding_choice)
    
    dim = dict_emb.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(dict_emb)
    index.add(dict_emb)
    
    faiss.normalize_L2(doubted_emb)
    distances, indices = index.search(doubted_emb, 5)  # Top-5 matches
    
    matches = {}
    for i, word in enumerate(doubted_words):
        word_matches = []
        for j in range(5):
            if distances[i][j] >= threshold:
                word_matches.append(dictionary_words[indices[i][j]])
        if word_matches:
            matches[word] = word_matches
        else:
            logger.info(f"No matches for '{word}' above threshold.")
    
    logger.info(f"Found matches for {len(matches)} words.")
    return matches
