import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="AI Report Generator", layout="centered")

# === Header with image and title ===
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=80)  # Make sure logo.png exists in the same folder
with col2:
    st.markdown("## 🧠 AI-Powered SQL Report Generator")
    st.caption("Natural language to SQL to PDF – powered by multi-agent framework  architecture")

# === Input form ===
st.write("Enter your query and get a report PDF generated from the database.")
with st.form("query_form"):
    user_prompt = st.text_area("🔍 Query", height=100, placeholder="e.g., List all Groceries transactions ,Total amount spend by Alice,On what date did Alice went for Groceries ")
    submitted = st.form_submit_button("Go")

# === Handle submission ===
if submitted and user_prompt:
    with st.spinner("⏳ Thinking..."):
        try:
            response = requests.post(
                "http://localhost:7073/interpret",
                json={"prompt": user_prompt}
            )

            if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("application/pdf"):
                st.success("✅ PDF generated successfully!")

                st.download_button(
                    label="📄 Download Report",
                    data=response.content,
                    file_name="query_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("❌ Error from agent:")
                st.code(response.text, language="json")

        except Exception as e:
            st.error("⚠️ Failed to connect to the interpreter agent.")
            st.exception(e)
