import streamlit as st
import PyPDF2
from fpdf import FPDF
import google.generativeai as genai

# १. पेज सेटअप
st.set_page_config(page_title="Mitradnya PaperGen", layout="wide")

# API Configuration
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("Mitradnya PaperGen 🎓")

# २. फॉर्म इनपुट
col1, col2, col3 = st.columns(3)
with col1: num_mcqs = st.number_input("MCQs", value=10)
with col2: num_short = st.number_input("Short Notes", value=4)
with col3: num_long = st.number_input("Long Questions", value=2)

course = st.selectbox("Class", ["FYBCOM", "SYBCOM", "TYBCOM", "TYBMS"])
subject = st.selectbox("Subject", ["GST", "Accounting", "Economics"])
topic_input = st.text_input("Topic Name")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# ३. जनरेशन लॉजिक (सर्व कोड या बटणच्या आत ठेवा)
if st.button("✨ Generate Question Paper", type="primary"):
    
    # PDF मजकूर काढणे
    context = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            context += page.extract_text() or ""
            
    if topic_input or context:
        with st.spinner('Generating...'):
            # Prompt आता इथेच तयार होतोय
            prompt = f"""
            Create a question paper for {course} - {subject}.
            Topic: {topic_input}. 
            Ref Material: {context[:4000]}
            Structure: {num_mcqs} MCQs, {num_short} Short, {num_long} Long.
            """
            
            try:
                response = model.generate_content(prompt)
                paper_text = response.text
                
                st.markdown("### Generated Paper:")
                st.markdown(paper_text)
                
                # PDF तयार करणे
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                # मराठी मजकूर नसल्यास ही ओळ चालते
                pdf.multi_cell(0, 10, txt=paper_text.encode('latin-1', 'replace').decode('latin-1'))
                
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf.output(dest='S'),
                    file_name="Question_Paper.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter Topic or Upload PDF!")
