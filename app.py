 import streamlit as st
import joblib
import pandas as pd
import requests
from fpdf import FPDF
import streamlit_authenticator as stauth

# Pre-hashed passwords
hashed_pw = {
    "sayeda": "$2b$12$BhkxFP8QKm2CO6EVNvCmUuJ8nQih1nC1wU/M0vN2zyP4cyYbveCEi",  # autoneuro123
    "user1": "$2b$12$fH0vlSw/4GG3XhnTTx3pzeLUZivN.gJDL7Zctyi9ARmjMRdCmh6Vi"    # testpass
}

# Auth config
config = {
    'credentials': {
        'usernames': {
            'sayeda': {
                'name': "Sayeda Rehmat",
                'password': hashed_pw["sayeda"]
            },
            'user1': {
                'name': "Pro User",
                'password': hashed_pw["user1"]
            }
        }
    },
    'cookie': {
        'name': 'auto_cookie',
        'key': '123456',
        'expiry_days': 1
    },
    'preauthorized': {
        'emails': []
    }
}

# Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Login
name, auth_status, username = authenticator.login("Login", location="main")

# Login response
if auth_status:
    st.sidebar.success(f"Welcome, {name}")
    authenticator.logout("Logout", "sidebar")

    # Load the model
    model = joblib.load("gene_classifier.pkl")

    # Track session results
    if "user_results" not in st.session_state:
        st.session_state.user_results = []

    st.title("🧬 AutoNeuro Pro — Cancer vs Neuro Classifier")
    st.markdown(f"""
Hello, **{name}** 👋 — welcome to your private gene prediction portal.

Upload a `.vcf` file to classify genes as **Cancer** or **Neuro**-related.  
Your results are stored in your private session dashboard.
""")

    # Sample file
    with open("sample.vcf", "r") as f:
        st.download_button("📥 Download Sample VCF", f.read(), "sample.vcf", "text/plain")

    # File uploader
    uploaded = st.file_uploader("📤 Upload your VCF file", type="vcf")

    if uploaded:
        lines = uploaded.read().decode("utf-8").splitlines()
        st.success("✅ File uploaded and processed.")
        st.subheader("🔬 Gene Predictions")

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
                except:
                    pred = "Unknown"

                # Gene lookup
                try:
                    url = f"https://mygene.info/v3/query?q=symbol:{gene}&species=human&fields=name,summary"
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    if data.get("hits") and len(data["hits"]) > 0:
                        hit = data["hits"][0]
                        fullname = hit.get("name", "Not available")
                        desc = hit.get("summary", "No description available.")
                    else:
                        fullname = "Not available"
                        desc = "No description found."
                except:
                    fullname = "Unavailable"
                    desc = "Error fetching gene info."

                st.markdown(f"""
**Gene:** `{gene}`  
- **Prediction:** `{pred}`  
- **Full Name:** {fullname}  
- **Description:** {desc}
""")

                predictions.append({
                    "Gene": gene,
                    "Prediction": pred,
                    "Full Name": fullname,
                    "Description": desc
                })

        if predictions:
            df = pd.DataFrame(predictions)
            st.session_state.user_results.extend(predictions)

            # CSV
            st.download_button("📄 Download CSV", df.to_csv(index=False), "autoneuro_results.csv", "text/csv")

            # PDF
            def generate_pdf(data):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="AutoNeuro Report", ln=True, align="C")
                pdf.ln(10)
                for row in data:
                    g = f"Gene: {row['Gene']} — Prediction: {row['Prediction']}"
                    fn = f"Full Name: {row['Full Name']}"
                    d = f"Description: {row['Description']}"
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(200, 8, txt=g.encode('latin-1', 'replace').decode('latin-1'), ln=True)
                    pdf.set_font("Arial", 10)
                    pdf.multi_cell(0, 6, txt=fn.encode('latin-1', 'replace').decode('latin-1'))
                    pdf.multi_cell(0, 6, txt=d.encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln(4)
                return pdf.output(dest='S').encode('latin-1')

            pdf_data = generate_pdf(predictions)
            st.download_button("📑 Download PDF Report", data=pdf_data, file_name="autoneuro_report.pdf", mime="application/pdf")

    # Dashboard
    if st.checkbox("📊 Show My Dashboard"):
        if st.session_state.user_results:
            dashboard_df = pd.DataFrame(st.session_state.user_results)
            st.dataframe(dashboard_df)
            st.download_button("📥 Export Dashboard", dashboard_df.to_csv(index=False), "dashboard.csv", "text/csv")
        else:
            st.info("No results yet.")
else:
    st.warning("Please log in to access AutoNeuro.")
