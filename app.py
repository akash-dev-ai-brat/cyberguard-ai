import os
import streamlit as st
import pandas as pd
import requests
import json
from PIL import Image

# Setup page config
st.set_page_config(page_title="CyberGuard AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for premium dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    :root {
        --primary-bg: #09090b;
        --secondary-bg: #18181b;
        --accent: #10B981;
        --accent-hover: #059669;
        --accent-blue: #3B82F6;
        --text-main: #FAFAFA;
        --text-muted: #A1A1AA;
        --danger: #ef4444;
        --warning: #f59e0b;
        --glass: rgba(24, 24, 27, 0.7);
    }
    
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-main);
        font-family: 'Outfit', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text-main) !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    h1 {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-blue) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Glassmorphism Cards for containers */
    div[data-testid="stMetric"], div[data-testid="stExpander"] {
        background: var(--glass);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover, div[data-testid="stExpander"]:hover {
        transform: translateY(-5px);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.23);
        background: linear-gradient(135deg, var(--accent-hover) 0%, var(--accent) 100%);
        color: white;
    }
    
    /* Forms */
    div[data-testid="stForm"] {
        background: var(--secondary-bg);
        border-radius: 16px;
        padding: 32px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Status styling */
    .status-normal { color: var(--accent); font-weight: 800; font-size: 2.5rem; text-shadow: 0 0 20px rgba(16,185,129,0.4); }
    .status-attack { color: var(--danger); font-weight: 800; font-size: 2.5rem; text-shadow: 0 0 20px rgba(239,68,68,0.4); }
    
    hr {
        border-color: rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.image(r"C:\Users\Akash\.gemini\antigravity\brain\ac22025d-e9ad-4c72-895e-940dc2a8b791\cyberguard_header_1781838624849.png", use_container_width=True)
    st.markdown("## 🛡️ CyberGuard AI")
    st.markdown("---")
    page = st.radio("Navigation", ["Overview", "Live Detection", "Model Comparison", "SHAP Explainability", "Batch Scan"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("Built with ♥ by Akash Nath")

API_URL = "http://localhost:8000"

def check_api_health():
    try:
        res = requests.get(f"{API_URL}/health")
        return res.status_code == 200 and res.json().get("status") == "healthy"
    except:
        return False

api_ready = check_api_health()

if page == "Overview":
    st.image(r"C:\Users\Akash\.gemini\antigravity\brain\ac22025d-e9ad-4c72-895e-940dc2a8b791\cyberguard_header_1781838624849.png", use_container_width=True)
    st.title("Network Intrusion Detection System")
    st.markdown("""
    <div style='font-size: 1.2rem; color: #A1A1AA; margin-bottom: 2rem;'>
    CyberGuard AI represents the next generation of network security. By leveraging advanced ensemble machine learning techniques (XGBoost) trained on the NSL-KDD dataset, it provides real-time, highly accurate, and fully explainable threat detection.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Threat Classification Categories")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Normal", "Benign", "0%")
    col2.metric("DoS", "Availability", "SYN floods")
    col3.metric("Probe", "Recon", "Port sweeps")
    col4.metric("R2L", "Auth Bypass", "Password guess")
    col5.metric("U2R", "Privilege Esc.", "Buffer overflow")
    
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("### 🎯 High Accuracy\n**77.62%** overall accuracy and **94.71%** ROC-AUC on entirely unseen data.")
    with col_b:
        st.success("### ⚡ Real-Time\nFastAPI backend processes network records with **sub-10ms** latency.")
    with col_c:
        st.warning("### 🔍 Explainable\nEvery alert is backed by game-theoretic **SHAP values** explaining the *why*.")

elif page == "Live Detection":
    st.title("Live Traffic Simulation")
    st.markdown("Inject simulated network connection payloads to test the model's zero-day inference capabilities.")
    
    if not api_ready:
        st.error("API Backend is offline or models are not loaded. Please start `uvicorn api:app --reload`.")
    else:
        with st.form("predict_form"):
            st.markdown("### 📡 Connection Features")
            col1, col2, col3, col4 = st.columns(4)
            duration = col1.number_input("Duration (s)", 0.0, step=1.0)
            protocol_type = col2.selectbox("Protocol", ["tcp", "udp", "icmp"])
            service = col3.selectbox("Service", ["http", "private", "domain_u", "smtp", "ftp_data", "eco_i"])
            flag = col4.selectbox("Flag", ["SF", "S0", "REJ", "RSTR", "SH"])
            
            src_bytes = col1.number_input("Source Bytes", 0, step=100)
            dst_bytes = col2.number_input("Dest Bytes", 0, step=100)
            count = col3.number_input("Count", 0, step=1)
            serror_rate = col4.slider("Serror Rate", 0.0, 1.0, 0.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🛡️ ANALYZE CONNECTION")
            
            if submitted:
                payload = {
                    'duration': duration, 'protocol_type': protocol_type, 'service': service, 'flag': flag,
                    'src_bytes': src_bytes, 'dst_bytes': dst_bytes, 'land': 0, 'wrong_fragment': 0, 'urgent': 0, 'hot': 0,
                    'num_failed_logins': 0, 'logged_in': 1 if service=='http' else 0, 'num_compromised': 0, 'root_shell': 0,
                    'su_attempted': 0, 'num_root': 0, 'num_file_creations': 0, 'num_shells': 0,
                    'num_access_files': 0, 'num_outbound_cmds': 0, 'is_host_login': 0, 'is_guest_login': 0, 
                    'count': count, 'srv_count': count, 'serror_rate': serror_rate,
                    'srv_serror_rate': serror_rate, 'rerror_rate': 0.0, 'srv_rerror_rate': 0.0, 'same_srv_rate': 1.0,
                    'diff_srv_rate': 0.0, 'srv_diff_host_rate': 0.0, 'dst_host_count': count,
                    'dst_host_srv_count': count, 'dst_host_same_srv_rate': 1.0, 'dst_host_diff_srv_rate': 0.0,
                    'dst_host_same_src_port_rate': 0.0, 'dst_host_srv_diff_host_rate': 0.0,
                    'dst_host_serror_rate': serror_rate, 'dst_host_srv_serror_rate': serror_rate, 'dst_host_rerror_rate': 0.0,
                    'dst_host_srv_rerror_rate': 0.0
                }
                
                with st.spinner("Processing through neural pathways..."):
                    res = requests.post(f"{API_URL}/predict", json={"data": payload})
                    
                if res.status_code == 200:
                    data = res.json()
                    st.markdown("---")
                    st.markdown("### Analysis Results")
                    pred = data['prediction']
                    conf = data['confidence']
                    
                    if pred == "Normal":
                        st.markdown(f"<div class='status-normal'>✅ Normal Traffic</div>", unsafe_allow_html=True)
                        st.markdown(f"**Confidence:** {conf*100:.2f}%")
                    else:
                        st.markdown(f"<div class='status-attack'>🚨 ATTACK DETECTED: {pred}</div>", unsafe_allow_html=True)
                        st.markdown(f"**Confidence:** {conf*100:.2f}%")
                        
                    st.markdown("<br>### Threat Explanation (SHAP Attribution)", unsafe_allow_html=True)
                    st.markdown("The AI made this decision based on the following feature contributions:")
                    
                    for feat in data['top_features']:
                        color = "red" if feat['contribution'] > 0 else "green"
                        dir_str = "increased suspicion" if feat['contribution'] > 0 else "decreased suspicion"
                        st.markdown(f"- 🔸 **{feat['feature']}**: {feat['contribution']:+.3f} ({dir_str})")
                else:
                    st.error(f"API Error: {res.text}")

elif page == "Model Comparison":
    st.title("Architecture & Model Comparison")
    
    metrics_path = "models/metrics.json"
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
        st.markdown("### Evaluated on Held-Out Test Set")
        df = pd.DataFrame(metrics).T
        
        for col in ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC']:
            if col in df.columns:
                df[col] = (df[col] * 100).map("{:.2f}%".format)
        
        st.dataframe(df, width=1000)
        
        st.markdown("""
        <div style='background: var(--glass); padding: 20px; border-radius: 12px; margin-top: 20px;'>
        <h3>Why XGBoost?</h3>
        <p>XGBoost's gradient boosting sequentially corrects errors made by previous trees, giving it higher precision on the minority classes (R2L, U2R) that are hardest to detect.</p>
        <p>It also natively supports exact SHAP TreeExplainer computations, which is crucial for delivering SOC-ready, auditable alert justifications.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Metrics not found. Run `train.py` first.")

elif page == "SHAP Explainability":
    st.title("Global Threat Intelligence (SHAP)")
    st.markdown("What behaviors is the AI actively hunting for across the network?")
    
    shap_path = "assets/shap_summary.png"
    if os.path.exists(shap_path):
        try:
            image = Image.open(shap_path)
            st.image(image, caption="Global SHAP Summary", use_container_width=True)
        except Exception as e:
            st.error(f"Could not load image: {e}")
    else:
        st.info("SHAP plot not found. Run `train.py` to generate it.")

elif page == "Batch Scan":
    st.title("Batch Data Ingestion")
    st.markdown("Upload bulk network logs (CSV) for asynchronous threat scanning.")
    
    uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"])
    if uploaded_file is not None:
        if not api_ready:
            st.error("API is offline.")
        else:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(df)} records into the ingestion queue.")
            if st.button("🚀 Initialize Batch Scan"):
                st.info("Batch scanning is mocked in this portfolio version. In a production scenario, this would stream events through Kafka, process via FastAPI, and return a comprehensive incident report.")
