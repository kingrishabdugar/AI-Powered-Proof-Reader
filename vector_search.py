import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import streamlit as st

def get_embeddings(words, use_gemini=True, batch_size=10):
    try:
        if use_gemini:
            genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", os.environ.get('GEMINI_API_KEY')))
            embeddings = []
            for i in range(0, len(words), batch_size):
                batch = words[i:i+batch_size]
                result = genai.embed_content(model="models/embedding-001", content=batch, task_type="SEMANTIC_SIMILARITY")  # Latest free endpoint[9]
                embeddings.extend([np.array(emb) for emb in result['embedding']])
            return np.array(embeddings).astype('float32')
        else:
            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            return model.encode(words).astype('float32')
    except Exception as e:
        st.error(f"Embedding error: {str(e)}. Falling back to non-Gemini.")
        return get_embeddings(words, use_gemini=False)

def find_closest_matches(doubted_words, dictionary_words, threshold=0.8):
    if not dictionary_words or not doubted_words:
        return {}
    
    with st.spinner("Generating embeddings..."):
        dict_emb = get_embeddings(dictionary_words)
        doubted_emb = get_embeddings(doubted_words)
    
    dim = dict_emb.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(dict_emb)
    index.add(dict_emb)
    
    faiss.normalize_L2(doubted_emb)
    distances, indices = index.search(doubted_emb, 1)
    
    matches = {}
    for i, word in enumerate(doubted_words):
        if distances[i][0] >= threshold:
            matches[word] = dictionary_words[indices[i][0]]
    
    return matches
