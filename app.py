 import streamlit as st
import joblib
import pandas as pd
import io

# Load model
model = joblib.load("gene_classifier.pkl")

# Title and About
st.title("🧬 AutoNeuro: Cancer vs Neuro Gene Classifier")
st.markdown("""
Welcome to **AutoNeuro**, an AI-powered gene classifier that predicts whether a gene is associated with **cancer** or **neurological disorders** using simple VCF files.

**Built by Zisha Maryam**, this tool is designed for bioinformatics students, researchers, and healthcare professionals.

👉 Just upload your `.vcf` file below to get started.
""")

# Sample VCF download
with open("sample.vcf", "r") as f:
    st.download_button("📥 Download Sample VCF", f.read(), "sample.vcf", "text/plain")

# Upload VCF file
uploaded = st.file_uploader("📤 Upload your VCF file", type="vcf")

# Predict and Export
if uploaded:
    lines = uploaded.read().decode("utf-8").splitlines()
    st.success("✅ File uploaded and processed.")
    st.subheader("🔬 Gene Predictions:")

    predictions = []

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
            pred = model.predict([gene])[0]
            predictions.append({"Gene": gene, "Prediction": pred})
            st.markdown(f"- 🧬 **{gene}** → 🧠 **{pred}**")
        else:
            st.warning("⚠️ Gene not found in INFO field.")

    # Export CSV
    if predictions:
        df = pd.DataFrame(predictions)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download Results as CSV",
            data=csv,
            file_name="autoneuro_predictions.csv",
            mime="text/csv"
        )
