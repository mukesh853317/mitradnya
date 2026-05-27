import streamlit as st
import google.generativeai as genai

# १. पेज सेटिंग आणि कॉन्फिगरेशन
st.set_page_config(page_title="Mitradnya PaperGen", layout="wide")

# API Key सेट करणे
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# २. हेडर
st.title("Mitradnya PaperGen 🎓")
st.markdown("### Admin Dashboard - Question Paaper Generator")
st.markdown("---")

# ३. साइडबार
st.sidebar.header("Previous Year Question Papers")
st.sidebar.button("📄 TYBCOM GST Paper", key="h1")
st.sidebar.button("📄 TYBMS FA Paper", key="h2")

# ४. मुख्य फॉर्म (Inputs)
col1, col2, col3 = st.columns(3)
with col1: university = st.selectbox("University", ["Mumbai University", "Other"])
with col2: course = st.selectbox("Class", ["TYBCOM", "TYBMS", "MCOM"])
with col3: subject = st.selectbox("Subject", ["Indirect Tax (GST)", "Financial Accounting", "Economics"])

tab1, tab2, tab3 = st.tabs(["Topic", "Text Notes", "Upload PDF"])
with tab1: topic_input = st.text_input("टॉEnter Topic Name", key="t1")
with tab2: text_input = st.text_area("Paste Notes Here", key="t2")
with tab3: uploaded_file = st.file_uploader("Upload PDF", type="pdf")

col4, col5 = st.columns(2)
with col4: total_marks = st.selectbox("Total Marks", [20, 50, 75, 100])
with col5: difficulty = st.selectbox("Level", ["Easy", "Moderate", "Hard"])

# ५. AI जनरेशन लॉजिक (बटण क्लिक केल्यावर हे चालेल)
if st.button("✨ Generate Question Paper", type="primary", key="gen_btn"):
    
    # इनपुट तपासणी
    input_data = topic_input if topic_input else (text_input if text_input else "General")
    
    if input_data:
        with st.spinner('Generating Question Paper...'):
            try:
                # प्रॉम्प्ट तयार करणे
                prompt = f"""
                Act as a Professor. Create a {total_marks} marks question paper for {course}, {subject}.
                Topic: {input_data}. 
                Difficulty: {difficulty}.
                Include MCQs and Subjective questions.
                Format the output clearly.
                """
                
                # AI कॉल
                response = model.generate_content(prompt)
                
                # रिझल्ट दाखवणे
                st.markdown("### Generated Question Paper:")
                st.markdown(response.text)
                
                # भविष्यात येथे डाऊनलोड बटण जोडता येईल
            except Exception as e:
                st.error(f"Technical Error: {e}")
    else:
        st.error("Please Inseet Topic or Text!")
