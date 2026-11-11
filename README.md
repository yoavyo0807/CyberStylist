# 🕵️‍♂️ CyberStylist: Linguistic Profiling & Threat Attribution Engine

`CyberStylist` is a specialized computational linguistics tool designed for **Cyber Threat Intelligence (CTI)**, authorship attribution, and linguistic profiling of threat actors. 

While traditional data science approaches rely heavily on surface-level embeddings, CyberStylist bridges the gap by extracting deep **linguistic feature matrices** (such as syntax patterns, function word distributions, structural metrics, and L1 transfer markers) to link suspicious texts—such as ransomware notes or phishing campaigns—to specific threat actor profiles.

---

## 🚀 Key Features

1. **L1 Transfer & Substrate Analysis (Native Language Identification):**
   - **Slavic / Russian L1 Markers:** Detects systematic determiner omission (absence of articles like `the` or `a`) resulting from L1 interference.
   - **Persian L1 Markers:** Identifies over-coordination patterns (high frequency of coordinating conjunctions such as `and` / `that`) and pronoun redundancies reflecting Persian syntactic structures.
2. **Structural & Stylometric Metrics:** Evaluates sentence-length variance, lexical density, and punctuation ratios.
3. **Interactive Streamlit Dashboard:** Provides side-by-side comparative profiling and automated intelligence insights for security analysts.

---

## 🛠️ Project Architecture

```text
CyberStylist/
│
├── data/
│   └── dataset.csv       # Corpus of baseline and threat texts with L1 labels
├── extractor.py          # Core NLP linguistic feature extractor (spaCy-based)
├── app.py                # Streamlit interactive web application
└── README.md             # Project documentation