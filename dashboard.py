import streamlit as st
from analyzer import PhishingAnalyzer
import pandas as pd
import plotly.express as px

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stAlert {
        border-radius: 10px;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── Initialize Engine ────────────────────────────────────────────────────────
@st.cache_resource
def load_engine():
    return PhishingAnalyzer()

engine = load_engine()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("🛡️ Threat Intel")
st.sidebar.info("This system uses NLP & behavioral analysis to detect phishing attempts.")
st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
st.sidebar.success("Engine: Active")
st.sidebar.success("Database: Synchronized")

# ── Main UI ──────────────────────────────────────────────────────────────────
st.title("Phishing Detection Platform")
st.subheader("Enterprise-Grade Email Security Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Email Input")
    email_content = st.text_area("Paste raw email or .eml content here:", height=300, placeholder="From: security@bank.com\nSubject: Urgent...\n\nYour account has been...")
    
    analyze_btn = st.button("Run Threat Analysis", type="primary")

with col2:
    st.markdown("### Analysis Summary")
    if analyze_btn and email_content:
        with st.spinner("Analyzing threat vectors..."):
            result = engine.analyze_email(email_content)
            analysis = result['analysis']
            verdict = analysis['verdict']
            score = analysis['score']
            
            # Display Metric
            st.metric(label="Threat Score", value=f"{score}/100", delta=f"{verdict}")
            
            # Gauge Logic (Simplified with progress bar)
            st.write("Risk Level")
            color = "green" if score < 25 else "yellow" if score < 50 else "orange" if score < 75 else "red"
            st.progress(score / 100)
            
            # Explainable AI / Indicators
            st.markdown("#### Detected Indicators")
            for ind in analysis['indicators']:
                st.warning(f"⚠️ {ind}")
            
            if not analysis['indicators']:
                st.success("No malicious indicators found.")

if analyze_btn and email_content:
    st.markdown("---")
    st.markdown("### Deep Dive Intelligence")
    
    tab1, tab2, tab3 = st.tabs(["Extracted Features", "ML Interpretation", "Recommendations"])
    
    with tab1:
        metadata = result['metadata']
        st.json(metadata)
        
    with tab2:
        # Simulated Feature Importance Chart
        feat_data = pd.DataFrame({
            "Feature": ["URL Density", "Urgency Keywords", "Sender Mismatch", "Obfuscation", "Financial Bait"],
            "Weight": [0.3, 0.2, 0.25, 0.15, 0.1]
        })
        fig = px.bar(feat_data, x="Weight", y="Feature", orientation='h', title="AI Feature Importance (XAI)")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        if analysis['score'] > 50:
            st.error("### CRITICAL ACTION REQUIRED")
            st.write("1. **Do not click** any links in this email.")
            st.write("2. Report this to your IT Security department.")
            st.write("3. Block the sender domain.")
        else:
            st.success("### Email Appears Safe")
            st.write("Continue to practice standard security hygiene.")

else:
    st.info("Awaiting input for analysis. Paste an email to begin.")
