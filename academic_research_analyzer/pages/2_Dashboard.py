import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os  # ✅ Needed for checking file existence

st.set_page_config(page_title="📊 Dashboard", layout="wide")

st.markdown("<h2 style='color:#6C63FF;'>📊 Research Paper Analysis Dashboard</h2>", unsafe_allow_html=True)

log_path = "data/feedback.csv"

# Check if log file exists
if not os.path.exists(log_path):
    st.warning("No feedback or analysis logs available yet.")
else:
    df = pd.read_csv(log_path)

    if df.empty:
        st.info("No entries logged yet.")
    else:
        st.success("✅ Data loaded successfully!")
        
        # Overview metrics
        st.markdown("### 🔢 Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Papers", len(df))
        col2.metric("Avg Novelty", f"{df['Novelty'].mean():.2f}")
        col3.metric("Avg Clarity", f"{df['Clarity'].mean():.2f}")

        # Pie chart of suggestions
        st.markdown("### 🧠 Overall Suggestions")
        suggestion_counts = df['Overall Suggestion'].value_counts()
        fig_pie = px.pie(
            names=suggestion_counts.index,
            values=suggestion_counts.values,
            title="Overall Paper Recommendation",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Bar chart of novelty and clarity
        st.markdown("### 📈 Novelty vs Clarity")
        fig_bar = px.bar(
            df,
            x="Title",
            y=["Novelty", "Clarity"],
            barmode="group",
            color_discrete_sequence=px.colors.sequential.Purples,
            title="Scores per Paper"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Display full data
        st.markdown("### 🗂 Full Log Data")
        st.dataframe(df, use_container_width=True)
