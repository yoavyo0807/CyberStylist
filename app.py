import os
import pandas as pd
import streamlit as st
import plotly.express as px
from extractor import AdvancedStylometricExtractor

# Streamlit page configuration
st.set_page_config(page_title="CyberStylist - Linguistic Threat Attribution", layout="wide")

st.title("🕵️‍♂️ CyberStylist: Linguistic Profiling & Authorship Attribution")
st.markdown("""
A stylometric and linguistic tool designed for threat actor profiling, authorship attribution, 
and detecting L1 transfer markers (such as Russian vs. Persian native speakers) in suspicious texts and cyber incidents.
""")

# Path to the CSV file in the data directory
CSV_PATH = "data/dataset.csv"

@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(columns=["text_id", "author_id", "native_language", "text"])

df = load_data()

# Sidebar: Select analysis mode
st.sidebar.header("Select Analysis Mode")
mode = st.sidebar.radio("Choose input method:", ["Free Text Comparison", "Analyze from Local CSV Database"])

if mode == "Free Text Comparison":
    st.subheader("Stylometric Comparison Between Suspicious Text (e.g., Ransomware Note) and Reference Text")
    
    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area("Text A (e.g., Attack Message / Ransomware Note)", 
                            "I went to store yesterday and bought new car because old was broken.")
    with col2:
        text2 = st.text_area("Text B (Suspect Reference Text)", 
                            "Director said that project must be finished in end of week.")
        
    if st.button("Run Linguistic Analysis"):
        if text1 and text2:
            extractor1 = AdvancedStylometricExtractor(text1)
            extractor2 = AdvancedStylometricExtractor(text2)
            
            p1 = extractor1.get_profile()
            p2 = extractor2.get_profile()
            
            # Display metrics in a comparative table
            comparison_df = pd.DataFrame([p1, p2], index=["Text A", "Text B"]).T
            comparison_df.columns = ["Text 1", "Text 2"]
            comparison_df["Difference"] = abs(comparison_df["Text 1"] - comparison_df["Text 2"])
            
            st.markdown("### 📊 Linguistic Metrics Comparison (L1 & Structural Features)")
            st.dataframe(comparison_df)
            
            # Visual comparison chart using Plotly
            fig = px.bar(
                comparison_df.reset_index(), 
                x="index", 
                y=["Text 1", "Text 2"], 
                barmode="group",
                title="Stylometric Profile Comparison Between Texts",
                labels={"index": "Linguistic Metric", "value": "Relative Value", "variable": "Text"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Automated linguistic insights
            st.markdown("### 🔍 Intelligence Insights & L1 Diagnosis")
            art_1, art_2 = p1["article_ratio"], p2["article_ratio"]
            coord_1, coord_2 = p1["coordination_ratio"], p2["coordination_ratio"]
            
            if art_1 < 0.03 and art_2 < 0.03:
                st.info("💡 **Potential Match:** Both texts show very low determiner usage, which may indicate influence from a Slavic native language (such as Russian) lacking articles.")
            if coord_1 > 0.05 or coord_2 > 0.05:
                st.info("💡 **Potential Match:** High over-coordination level in the texts, characteristic of Persian native speakers writing in English.")
        else:
            st.warning("Please enter text in both boxes.")

else:
    st.subheader("📂 Text Analysis from Local CSV Database")
    if not df.empty:
        st.dataframe(df)
        
        selected_id = st.selectbox("Select text_id for deep analysis:", df["text_id"].tolist())
        selected_row = df[df["text_id"] == selected_id].iloc[0]
        
        st.write(f"**Selected Text:** {selected_row['text']}")
        st.write(f"**Known Native Language (Label):** {selected_row['native_language']}")
        
        if st.button("Extract Linguistic Profile"):
            ext = AdvancedStylometricExtractor(selected_row['text'])
            profile = ext.get_profile()
            st.json(profile)
    else:
        st.error("The CSV file is empty or missing from the path `data/dataset.csv`.")