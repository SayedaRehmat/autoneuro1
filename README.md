 # 🧬 AutoNeuro: AI-Powered Gene Classifier (Cancer vs Neuro)

AutoNeuro is an AI-based genomics tool that classifies genes as related to **cancer** or **neurological disorders** using simple `.vcf` files.

Built by ** Sayeda Rehmat**, this tool combines machine learning and bioinformatics to help researchers, students, and the public understand gene impact easily and quickly.

---

## 🌐 Live App

👉 [Click here to try the app](https://your-streamlit-app-link.streamlit.app)

> Upload a `.vcf` file and see instant predictions for each gene.

---

## 📂 Input Format: VCF File

Upload a `.vcf` file with `GENE=` tags in the INFO field.

### 🧾 Sample VCF:

```vcf
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	11178397	.	G	A	99	PASS	GENE=TP53
7	55191822	.	A	T	85	PASS	GENE=APP
16	89920138	.	G	C	70	PASS	GENE=HTT
```

Or use the built-in **"📥 Download Sample VCF"** button in the app.

---

## 🧠 How It Works

- The model is trained on labeled gene data using **scikit-learn**
- VCF files are parsed directly using pure Python (no external VCF parser)
- Predictions: `"cancer"` or `"neuro"` for each gene
- Instantly view predictions in a user-friendly interface

---

## 🧪 Tech Stack

| Tool        | Purpose                    |
|-------------|----------------------------|
| Streamlit   | Web UI                     |
| Scikit-learn| Gene classification model  |
| Joblib      | Model saving/loading       |
| Pandas      | Optional data handling     |
| Python      | VCF parsing + logic        |

---

## 🚀 Features

- Upload your own `.vcf` files
- See predictions for each gene
- Sample VCF download included
- Simple, clean UI for researchers and students
- 100% free and public

---

## 🤝 Want to Contribute?

- Add gene-disease lookup APIs
- Improve the classifier with new data
- Integrate with NCBI or Ensembl
- Build new visualizations

Pull requests are welcome!

---

## 👩‍💻 About the Creator

**Sayeda Rehmat** — aspiring bioinformatics innovator  
📧 [your-email@example.com]  
🌐 [github.com/your-profile]  
🔬 Passionate about AI, Genomics & Impactful Tech

---

## 📄 License

Free for **educational and research purposes**.  
Contact for commercial or institutional use.

---

## 💬 Citation

If you use this tool in your research, please cite it as:

```
Sayeda Rehmat, AutoNeuro: AI-Based Classifier for Cancer and Neuro Genes (2025)
```

---

### 🙏 Thank you for using AutoNeuro!

> "The future of medicine is written in code — and in our DNA."
