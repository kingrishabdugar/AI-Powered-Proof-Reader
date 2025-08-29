import docx
import regex as re
from langdetect import detect, DetectorFactory
from collections import Counter
import streamlit as st

DetectorFactory.seed = 0  # For consistent detection

def extract_unique_hindi_words(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = ' '.join([para.text for para in doc.paragraphs])
        
        # Extract words in Devanagari script
        hindi_words = re.findall(r'[\u0900-\u097F]+', text)
        
        # Filter only Hindi
        unique_words = set()
        for word in hindi_words:
            try:
                if detect(word) == 'hi':
                    unique_words.add(word)
            except:
                pass
        
        return list(unique_words)
    except Exception as e:
        st.error(f"Error extracting words: {str(e)}")
        return []
