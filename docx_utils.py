import docx
import os
import streamlit as st

def replace_words_in_docx(input_path, replacements, original_name):
    try:
        doc = docx.Document(input_path)
        
        for para in doc.paragraphs:
            for run in para.runs:
                text = run.text
                for old, new in replacements.items():
                    if old in text:
                        text = text.replace(old, new)
                run.text = text
        
        output_name = f"Corrected_{original_name}"
        output_path = os.path.join(os.path.dirname(input_path), output_name)
        doc.save(output_path)
        return output_path
    except Exception as e:
        st.error(f"Error replacing words: {str(e)}")
        return None
