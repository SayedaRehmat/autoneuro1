import streamlit as st
import joblib

model = joblib.load("gene_classifier.pkl")

st.title("🧬 AutoNeuro: Cancer vs Neuro Gene Classifier")
st.write("Upload a `.vcf` file with `GENE=` entries to get predictions.")

uploaded = st.file_uploader("Upload VCF File", type="vcf")

if uploaded:
    lines = uploaded.read().decode("utf-8").splitlines()
    st.success("File uploaded!")

    st.subheader("🧠 Predictions:")
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
            st.write(f"🧬 Gene: **{gene}** → `{prediction}`")
        else:
            st.write("⚠️ Gene not found.")
