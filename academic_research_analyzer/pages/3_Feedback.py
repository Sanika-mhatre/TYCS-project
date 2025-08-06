import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Feedback", layout="wide")

st.markdown("<h2 style='color:#4A7EBB;'>🗣️ Feedback</h2>", unsafe_allow_html=True)
st.write("We'd love to hear your thoughts about this assistant!")

# Feedback input
rating = st.slider("⭐ Rate your experience", 1, 5, 3)
comment = st.text_area("💬 Your suggestions / feedback (optional)", height=150)
submit = st.button("Submit Feedback")

# Handle submission
if submit:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_data = pd.DataFrame([{
        "timestamp": timestamp,
        "rating": rating,
        "comment": comment
    }])

    # Append to CSV
    file_path = "data/feedback.csv"
    if os.path.exists(file_path):
        existing = pd.read_csv(file_path)
        feedback_data = pd.concat([existing, feedback_data], ignore_index=True)

    feedback_data.to_csv(file_path, index=False)
    st.success("✅ Thank you for your feedback!")

# Show summary if feedback exists
if os.path.exists("data/feedback.csv"):
    df = pd.read_csv("data/feedback.csv")
    st.markdown("---")
    st.markdown("### 📊 Feedback Summary")

    # Pie chart of ratings
    fig = px.pie(df, names='rating', title='User Ratings', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # Optional: show comment history
    with st.expander("📝 View all feedback comments"):
        st.dataframe(df[["timestamp", "rating", "comment"]])
 
