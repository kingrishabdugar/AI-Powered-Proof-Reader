import streamlit as st
import tempfile
import os
from extract_hindi import extract_unique_hindi_words
from vector_search import find_closest_matches
from docx_utils import replace_words_in_docx

@st.cache_data
def cached_extract(docx_path):
    return extract_unique_hindi_words(docx_path)

@st.cache_data
def load_dictionary(dict_path):
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        st.error(f"Dictionary error: {str(e)}")
        return []

st.title("Interactive Hindi Spell Checker App")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.approved = {}
    st.session_state.matches = {}
    st.session_state.doubted = []

# Step 0: Upload
if st.session_state.step == 0:
    uploaded_docx = st.file_uploader("Upload DOCX file", type="docx", help="File must contain Hindi text.")
    uploaded_dict = st.file_uploader("Upload Hindi Dictionary (TXT)", type="txt", help="One word per line.")
    
    if uploaded_docx and uploaded_dict:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx.write(uploaded_docx.getvalue())
            docx_path = tmp_docx.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_dict:
            tmp_dict.write(uploaded_dict.getvalue())
            dict_path = tmp_dict.name
        
        st.session_state.docx_path = docx_path
        st.session_state.original_name = uploaded_docx.name
        st.session_state.dict_path = dict_path
        st.session_state.step = 1
        st.rerun()

# Step 1: Extract and Identify
if st.session_state.step == 1:
    dictionary = load_dictionary(st.session_state.dict_path)
    if not dictionary:
        st.error("Dictionary is empty. Please upload a valid file.")
        st.session_state.step = 0
        st.rerun()
    
    with st.spinner("Extracting unique Hindi words..."):
        unique_hindi = cached_extract(st.session_state.docx_path)
    
    st.session_state.doubted = [word for word in unique_hindi if word not in dictionary]
    
    if st.session_state.doubted:
        st.success(f"Found {len(st.session_state.doubted)} potentially misspelled words.")
        if st.button("Proceed to Suggestions"):
            st.session_state.step = 2
            st.rerun()
    else:
        st.success("No spelling issues detected.")
        if st.button("Restart"):
            st.session_state.step = 0
            st.rerun()

# Step 2: Generate Suggestions
if st.session_state.step == 2:
    dictionary = load_dictionary(st.session_state.dict_path)
    st.session_state.matches = find_closest_matches(st.session_state.doubted, dictionary)
    
    if st.session_state.matches:
        st.success("Suggestions generated!")
        st.session_state.step = 3
        st.rerun()
    else:
        st.info("No close matches found. Adjust threshold or dictionary?")
        if st.button("Back to Upload"):
            st.session_state.step = 0
            st.rerun()

# Step 3: Review and Approve
if st.session_state.step == 3:
    st.subheader("Review Suggestions")
    approve_all = st.checkbox("Approve All Suggestions", help="Select to auto-approve everything.")
    
    for wrong, correct in st.session_state.matches.items():
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{wrong} → {correct}")
        with col2:
            if approve_all or st.checkbox(f"Approve '{wrong}'?", key=wrong):
                st.session_state.approved[wrong] = correct
    
    if st.button("Apply Changes"):
        if st.session_state.approved:
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("No approvals selected.")

    if st.button("Reset Approvals"):
        st.session_state.approved = {}
        st.rerun()

# Step 4: Download
if st.session_state.step == 4:
    with st.spinner("Applying corrections..."):
        output_path = replace_words_in_docx(st.session_state.docx_path, st.session_state.approved, st.session_state.original_name)
    
    if output_path:
        st.success("Corrections applied!")
        with open(output_path, "rb") as f:
            st.download_button("Download Corrected File", f, file_name=f"Corrected_{st.session_state.original_name}")
        
        if st.button("Start Over"):
            # Clean up temp files
            os.unlink(st.session_state.docx_path)
            os.unlink(st.session_state.dict_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            st.session_state.clear()
            st.rerun()
    else:
        st.error("Failed to generate output. Please try again.")
        st.session_state.step = 3
        st.rerun()
