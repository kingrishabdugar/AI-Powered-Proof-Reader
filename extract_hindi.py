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
        
        # Extract potential Hindi words (Devanagari script)
        potential_words = re.findall(r'[\u0900-\u097F]+[\d०-९]*|[\d०-९]*[\u0900-\u097F]+', text)  # Capture words with possible digits
        
        # Clean each word: Remove leading/trailing punctuation, digits (Hindi/English), spaces, special chars
        cleaned_words = []
        for word in potential_words:
            # Strip leading/trailing digits (0-9, ०-९), punctuation, etc.
            cleaned = re.sub(r'^[\d०-९\s।\.?!,]+|[\d०-९\s।\.?!,]+$', '', word.strip())
            # Skip if empty or too short after cleaning
            if cleaned and len(cleaned) > 1:
                cleaned_words.append(cleaned)
        
        # Filter only Hindi words using langdetect
        unique_words = set()
        for word in cleaned_words:
            try:
                if detect(word) == 'hi':
                    unique_words.add(word)
            except:
                pass  # Skip if detection fails
        
        return list(unique_words)
    except Exception as e:
        st.error(f"Error extracting words: {str(e)}")
        return []
