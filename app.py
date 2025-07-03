import streamlit as st
import joblib

# Load model
model = joblib.load("gene_classifier.pkl")

# Title and About
st.title("🧬 AutoNeuro: Cancer vs Neuro Gene Classifier")
st.markdown("""
Welcome to **AutoNeuro**, an AI-powered gene classifier that predicts whether a gene is associated with **cancer** or **neurological disorders** using simple VCF files.

**Built by Sayeda Rehmat**, this tool is designed for bioinformatics students, researchers, and healthcare professionals.

👉 Just upload your `.vcf` file below to get started.
""")

# Download Sample
with open("sample.vcf", "r") as f:
    st.download_button("📥 Download Sample VCF", f.read(), "sample.vcf", "text/plain")

# File upload
uploaded = st.file_uploader("📤 Upload your VCF file here", type="vcf")

# Prediction
if uploaded:
    lines = uploaded.read().decode("utf-8").splitlines()
    st.success("✅ File uploaded and processed.")
    
    st.subheader("🔬 Gene Predictions:")

    for line in lines:
        if line.startswith("#"):
            continue
        parts = line.strip().split('\t')
        if len(parts) < 8:
            continue
        info = parts[7]
        gene = None
        for entry in info.split(";"):
            if entry.startswith("GENE="):
                gene = entry.split("=")[1]
                break
        if gene:
            prediction = model.predict([gene])[0]
            st.markdown(f"- 🧬 **{gene}** → 🧠 **{prediction}**")
        else:
            st.warning("⚠️ Gene not found in INFO field.")
