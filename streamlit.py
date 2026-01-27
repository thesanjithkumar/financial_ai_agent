import streamlit as st
from driver import run_financial_system

st.title("🤖 Personal Financial AI Agent Assistant")

with st.form("my_form"):
    text = st.text_area(
        "💬 What financial query do you have today?",
        placeholder="e.g., How should I plan my retirement savings?",
        height=100
    )
    submitted = st.form_submit_button("Submit")
    
    if submitted and text.strip():
        try:
            with st.spinner("🔄 Processing your query..."):
                results = run_financial_system(text)
            
            st.success("✅ Analysis Complete!")
            st.markdown("### Final Verified Plan")
            st.markdown(results)
            
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                st.error("⚠️ The AI model is currently overloaded. Please try again in a few moments.")
            elif "429" in error_msg:
                st.error("⚠️ Rate limit exceeded. Please wait a moment before trying again.")
            else:
                st.error(f"❌ An error occurred: {error_msg}")
                
    elif submitted:
        st.error("❌ Query cannot be empty!")
