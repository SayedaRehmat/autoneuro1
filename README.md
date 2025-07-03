# autoneuro1# 🧬 AutoNeuro: AI-Powered Gene Classifier (Cancer vs Neuro)

AutoNeuro is an AI-based genomics tool that classifies genes as related to **cancer** or **neurological disorders** using simple `.vcf` files.

Built by **Sayeda Rehmat**, this tool combines machine learning and bioinformatics to help researchers, students, and the public understand gene impact more easily.

---

## 🌐 Live App

👉 [Click here to use the app](https://your-streamlit-url.streamlit.app)

---

## 📂 Upload Format: VCF File

Upload a `.vcf` file with `GENE=` tags in the INFO column.

**Example:**

```vcf
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	11178397	.	G	A	99	PASS	GENE=TP53
7	55191822	.	A	T	85	PASS	GENE=APP
