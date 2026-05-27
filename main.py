import streamlit as st
import google.generativeai as genai

# १. पेज सेटिंग आणि कॉन्फिगरेशन
st.set_page_config(page_title="Mitradnya PaperGen", layout="wide")

# API Key सेट करणे
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# २. हेडर
st.title("Mitradnya PaperGen 🎓")
st.markdown("### शिक्षक डॅशबोर्ड - प्रश्नपत्रिका निर्मिती")
st.markdown("---")

# ३. साइडबार
st.sidebar.header("मागील प्रश्नपत्रिका")
st.sidebar.button("📄 TYBCOM GST Paper", key="h1")
st.sidebar.button("📄 TYBMS FA Paper", key="h2")

# ४. मुख्य फॉर्म (Inputs)
col1, col2, col3 = st.columns(3)
with col1: university = st.selectbox("विद्यापीठ", ["Mumbai University", "Other"])
with col2: course = st.selectbox("वर्ग", ["TYBCOM", "TYBMS", "MCOM"])
with col3: subject = st.selectbox("विषय", ["Indirect Tax (GST)", "Financial Accounting", "Economics"])

tab1, tab2, tab3 = st.tabs(["टॉपिक", "टेक्स्ट नोट्स", "PDF अपलोड"])
with tab1: topic_input = st.text_input("टॉपिकचे नाव टाका", key="t1")
with tab2: text_input = st.text_area("नोट्स पेस्ट करा", key="t2")
with tab3: uploaded_file = st.file_uploader("PDF अपलोड करा", type="pdf")

col4, col5 = st.columns(2)
with col4: total_marks = st.selectbox("एकूण गुण", [20, 50, 75, 100])
with col5: difficulty = st.selectbox("पातळी", ["Easy", "Moderate", "Hard"])

# ५. AI जनरेशन लॉजिक (बटण क्लिक केल्यावर हे चालेल)
if st.button("✨ Generate Question Paper", type="primary", key="gen_btn"):
    
    # इनपुट तपासणी
    input_data = topic_input if topic_input else (text_input if text_input else "General")
    
    if input_data:
        with st.spinner('AI प्रश्नपत्रिका तयार करत आहे...'):
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
                st.markdown("### जनरेट केलेली प्रश्नपत्रिका:")
                st.markdown(response.text)
                
                # भविष्यात येथे डाऊनलोड बटण जोडता येईल
            except Exception as e:
                st.error(f"काहीतरी तांत्रिक अडचण आली: {e}")
    else:
        st.error("कृपया टॉपिक किंवा मजकूर द्या!")
