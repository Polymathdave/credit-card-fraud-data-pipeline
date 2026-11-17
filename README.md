# Credit Card Fraud Detection: Exploratory Data Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

An in-depth exploratory analysis of a credit card transaction dataset, done to prepare for a fraud detection model. The aim is to understand the data well enough to make sound pre-processing and modelling decisions.

## 🔍 What the analysis covers
- **Data inspection & quality**: schema, descriptive statistics and missing-value checks.
- **Class imbalance**: how rare fraud is compared with legitimate transactions, and why this calls for imbalance-handling techniques (SMOTE, undersampling or cost-sensitive learning).
- **Time patterns**: transaction volume and fraud by hour across the 48-hour window.
- **Transaction amounts**: histograms, boxplots and violin plots comparing fraud and legitimate amounts, plus a Mann-Whitney U test.
- **Feature analysis**: distributions of the anonymised PCA features (V1–V28), a correlation matrix, and the features most correlated with fraud.
- **Findings**: each section ends with written findings that feed into the modelling and pre-processing choices.

## 📁 Repository structure
```
├── implementation.ipynb   # Full EDA notebook with charts and findings
└── README.md
```

## ▶️ How to run
```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl jupyter
jupyter notebook implementation.ipynb
```
> The notebook expects the dataset as `creditcard.xlsx` in the project folder.

## 🧰 Skills demonstrated
Exploratory data analysis · Imbalanced data · Statistical testing · Feature analysis · Data visualisation
