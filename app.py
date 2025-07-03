import streamlit as st
import joblib
import pandas as pd
import requests
from fpdf import FPDF

# Load model
model = joblib.load("gene_classifier.pkl")

# App Header
st.title("🧬 AutoNeuro: Cancer vs Neuro Gene Classifier")
st.markdown("""
Welcome to **AutoNeuro**, an AI-powered gene classifier that predicts whether a gene is associated with **cancer** or **neurological disorders** using simple VCF files.

**Built by Sayeda Rehmat**, this tool is designed for bioinformatics students, researchers, and healthcare professionals.

👉 Just upload your `.vcf` file below to get started.
""")

# Sample VCF download
with open("sample.vcf", "r") as f:
    st.download_button("📥 Download Sample VCF", f.read(), "sample.vcf", "text/plain")

# Upload VCF file
uploaded = st.file_uploader("📤 Upload your VCF file", type="vcf")

# Prediction logic
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
                gene = entry.split("=")[1].strip()
                break

        if gene and len(gene) > 1:
            try:
                pred = model.predict([gene])[0]
            except Exception:
                pred = "Unknown"

            # Lookup gene info
            try:
                query_url = f"https://mygene.info/v3/query?q=symbol:{gene}&species=human&fields=name,summary"
                response = requests.get(query_url, timeout=5)
                info_data = response.json()
                if info_data.get("hits") and len(info_data["hits"]) > 0:
                    hit = info_data["hits"][0]
                    fullname = hit.get("name", "Not available")
                    desc = hit.get("summary", "No description available.")
                else:
                    fullname = "Not available"
                    desc = "No description found in gene database."
            except Exception:
                fullname = "Unavailable"
                desc = "⚠️ Error fetching gene information."

            # Show results in app
            st.markdown(f"""
**🧬 Gene:** `{gene}`  
- **Prediction:** 🧠 `{pred}`  
- **Full Name:** {fullname}  
- **Description:** {desc}
""")

            predictions.append({
                "Gene": gene,
                "Prediction": pred,
                "Full Name": fullname,
                "Description": desc
            })

    # Generate CSV
    if predictions:
        df = pd.DataFrame(predictions)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download Results as CSV",
            data=csv,
            file_name="autoneuro_predictions.csv",
            mime="text/csv"
        )

        # Generate PDF
        def generate_pdf(data):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="AutoNeuro Gene Classification Report", ln=True, align="C")
            pdf.ln(10)

            for row in data:
                pdf.set_font("Arial", "B", size=11)
                pdf.cell(200, 8, txt=f"Gene: {row['Gene']} — Prediction: {row['Prediction']}", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 6, f"Full Name: {row['Full Name']}\nDescription: {row['Description']}", border=0)
                pdf.ln(4)

            return pdf.output(dest='S').encode('latin1')

        pdf_data = generate_pdf(predictions)
        st.download_button(
            label="📑 Download PDF Report",
            data=pdf_data,
            file_name="autoneuro_report.pdf",
            mime="application/pdf"
        )
