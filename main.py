import streamlit as st
import google.generativeai as genai

# स्ट्रीमलीट सीक्रेट्स मधून की मिळवा
api_key = st.secrets["GOOGLE_API_KEY"]

# AI मॉडेल कॉन्फिगर करा
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# ॲक्शन बटणच्या आत आता AI ला प्रश्न विचारा
if st.button("✨ Generate Question Paper", type="primary"):
    if topic_input:
        with st.spinner('प्रश्नपत्रिका तयार करत आहे...'):
            # प्रॉम्प्ट तयार करणे
            prompt = f"Create a {total_marks} marks question paper for {subject} on the topic: {topic_input}. Include MCQs and short notes."
            
            # AI कडून रिस्पॉन्स मिळवणे
            response = model.generate_content(prompt)
            
            # रिझल्ट दाखवणे
            st.markdown("### जनरेट केलेली प्रश्नपत्रिका:")
            st.write(response.text)
    else:
        st.error("कृपया टॉपिकचे नाव टाका!")

# १. पेजची प्राथमिक सेटिंग (Page Configuration)
st.set_page_config(page_title="Mitradnya PaperGen", layout="wide")

# २. हेडर (Header)
st.title("Mitradnya PaperGen 🎓")
st.markdown("### शिक्षक डॅशबोर्ड (Teacher Dashboard) - प्रश्नपत्रिका निर्मिती")
st.markdown("---")

# ३. डावीकडील बाजू (Sidebar - History & Templates)
st.sidebar.header("मागील प्रश्नपत्रिका")
st.sidebar.button("📄 TYBCOM GST Paper (May 26)")
st.sidebar.button("📄 TYBMS FA Paper (May 20)")

st.sidebar.markdown("---")
st.sidebar.header("क्विक टेम्पलेट्स")
st.sidebar.button("⚡ 20-Mark Unit Test")
st.sidebar.button("⚡ 75-Mark Final Exam (MU)")

# ४. मुख्य भाग - फॉर्म (Main Form)
st.subheader("१. शैक्षणिक स्तर निवडा")
col1, col2, col3 = st.columns(3)

with col1:
    university = st.selectbox("विद्यापीठ/बोर्ड", ["Mumbai University", "Other"])
with col2:
    course = st.selectbox("वर्ग/कोर्स", ["TYBCOM", "TYBMS", "MCOM"])
with col3:
    subject = st.selectbox("विषय", ["Indirect Tax (GST)", "Financial Accounting", "Economics"])

st.markdown("---")

st.subheader("२. कंटेंटचा स्रोत (Source)")
tab1, tab2, tab3 = st.tabs(["पर्याय A (Topics)", "पर्याय B (Text Notes)", "पर्याय C (Upload PDF)"])

with tab1:
    topic_input = st.text_input("टॉपिकचे नाव टाका (उदा. Partnership Final Accounts, Input Tax Credit)")
with tab2:
    text_input = st.text_area("तुमच्या स्वतःच्या नोट्सचा मजकूर येथे पेस्ट करा")
with tab3:
    uploaded_file = st.file_uploader("तुमच्या नोट्स किंवा पुस्तकाची PDF फाईल अपलोड करा", type="pdf")

st.markdown("---")

st.subheader("३. पेपरचा फॉरमॅट आणि पॅटर्न")
col4, col5 = st.columns(2)

with col4:
    total_marks = st.selectbox("एकूण गुण", [20, 50, 75, 100])
with col5:
    difficulty = st.selectbox("काठिण्य पातळी", ["Easy", "Moderate", "Hard"])

st.write("**प्रश्नांचे प्रकार निवडा:**")
mcq = st.checkbox("बहुपर्यायी प्रश्न (MCQs)", value=True)
short_notes = st.checkbox("थोडक्यात टिपा (Short Notes)", value=True)
long_q = st.checkbox("सविस्तर उत्तरे / प्रॅक्टिकल प्रॉब्लेम्स (Long Questions)", value=True)

# उत्तरतालिका हवी की नको यासाठी पर्याय
include_answer_key = st.checkbox("✔️ उत्तरतालिका (Answer Key) सोबत जनरेट करा", value=True)

st.markdown("---")

# ५. ॲक्शन बटन (Generate Button)
if st.button("✨ Generate Question Paper", type="primary"):
    if topic_input or text_input or uploaded_file:
        st.success("तुमची प्रश्नपत्रिका तयार होत आहे... कृपया प्रतीक्षा करा.")
        st.info("*(भविष्यात या ठिकाणी Google Gemini API चा वापर करून थेट प्रश्न तयार करण्याचा कोड जोडला जाईल)*")
    else:
        st.error("कृपया पेपर तयार करण्यासाठी एखादा टॉपिक, मजकूर किंवा PDF अपलोड करा!")
