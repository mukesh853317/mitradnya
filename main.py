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
st.markdown("---")

# २. फॉर्म इनपुट (Blueprint & Class Selection)
st.subheader("⚙️ प्रश्नपत्रिका आराखडा (Paper Blueprint)")
col1, col2, col3 = st.columns(3)
with col1: num_mcqs = st.number_input("MCQs संख्या", value=10)
with col2: num_short = st.number_input("Short Notes संख्या", value=4)
with col3: num_long = st.number_input("Long Questions संख्या", value=2)

col1, col2, col3 = st.columns(3)
with col1: university = st.selectbox("University", ["Mumbai University", "Other"])
with col2: course = st.selectbox("Class", ["FYBCOM", "SYBCOM", "TYBCOM", "TYBMS", "MCOM"])
with col3: subject = st.selectbox("Subject", ["Indirect Tax (GST)", "Financial Accounting", "Economics", "Financial Maths"])

# ३. कंटेंट इनपुट
tab1, tab2, tab3 = st.tabs(["Topic", "Text Notes", "Upload PDF"])
with tab1: topic_input = st.text_input("Enter Topic Name")
with tab2: text_input = st.text_area("Paste Notes Here")
with tab3: uploaded_file = st.file_uploader("Upload PDF", type="pdf")

col4, col5 = st.columns(2)
with col4: total_marks = st.selectbox("Total Marks", [20, 50, 75, 100])
with col5: difficulty = st.selectbox("Level", ["Easy", "Moderate", "Hard"])

# ४. AI जनरेशन आणि PDF वाचन
if st.button("✨ Generate Question Paper", type="primary"):
    
    # PDF किंवा टेक्स्ट मधून डेटा काढणे
    context = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            context += page.extract_text()
    elif text_input:
        context = text_input

    # इनपुट तपासणी
    if topic_input or context:
        with st.spinner('Generating Paper...'):
            try:
                prompt = f"""
                Act as an expert professor. Create a {total_marks} marks question paper for {course}, {subject}.
                Topic: {topic_input}. 
                Based on this Reference Material: {context[:5000]} (if provided).
                
                Strictly follow this structure:
                - {num_mcqs} Multiple Choice Questions (MCQs)
                - {num_short} Short Answer Questions
                - {num_long} Long/Practical Questions
                
                Difficulty Level: {difficulty}.
                Format it neatly with headers.
                """
                
                response = model.generate_content(prompt)
                st.markdown("### Generated Question Paper:")
                st.markdown(response.text)
                
                # डाउनलोड बटण
                st.download_button(
                    label="📥 Download Paper as Text",
                    data=response.text,
                    file_name="Question_Paper.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Technical Error: {e}")
    else:
        st.error("Please enter a Topic or Upload/Paste your study material!")
