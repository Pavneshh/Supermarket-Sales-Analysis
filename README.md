# Supermarket Sales Analysis Dashboard

An end-to-end Data Analytics project focused on analyzing supermarket sales data and building an interactive business dashboard using Python and Streamlit.

---

## Project Overview

This project analyzes supermarket sales transactions to uncover business insights such as:

* Monthly Revenue Trends
* Peak Shopping Hours
* Category-wise Performance
* Discount Impact on Sales
* Product-level Analysis
* Customer Purchase Patterns

The raw data was collected from multiple CSV files, cleaned, transformed, and merged into a single analytical dataset for visualization and reporting.

---

## Objectives

* Perform Exploratory Data Analysis (EDA)
* Clean and preprocess large datasets
* Generate business insights
* Build an interactive dashboard
* Practice real-world Data Analytics workflow
* Create a portfolio-ready project

---

## Dataset Information

The project uses four datasets:

| File       | Description         |
| ---------- | ------------------- |
| annex1.csv | Product Information |
| annex2.csv | Sales Transactions  |
| annex3.csv | Wholesale Prices    |
| annex4.csv | Product Loss Rate   |

After preprocessing, all datasets were merged into a unified analytical dataset.

---

## Data Processing Steps

### Data Cleaning

* Removed missing values
* Checked duplicate records
* Corrected data types
* Converted Date and Time columns

### Feature Engineering

Created new features:

* Total_Sales
* Month
* Day
* Weekday
* Hour

Formula used:

Total_Sales = Quantity Sold × Unit Selling Price

---

## Exploratory Data Analysis

The analysis includes:

### Monthly Sales Trend

Understanding revenue fluctuations across months.

### Hourly Sales Pattern

Identifying peak shopping hours.

### Discount Impact Analysis

Comparing sales generated through discounts and regular sales.

### Category Performance

Finding the highest-performing product categories.

### Product Analysis

Identifying top-selling products.

---

## Dashboard Features

Interactive Streamlit Dashboard:

* Revenue KPIs
* Monthly Trend Analysis
* Hourly Sales Visualization
* Category Performance Charts
* Discount Impact Visualization
* Data Preview Section
* Interactive Filters

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Plotly
* Streamlit

### Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## Project Structure

```text
Supermarket-Sales-Analysis/
│
├── assets/
│
├── data/
│   ├── annex1.csv
│   ├── annex2.csv
│   ├── annex3.csv
│   └── annex4.csv
│
├── notebooks/
│   └── eda.ipynb
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Pavneshh/Supermarket-Sales-Analysis.git
```

Move into the project directory:

```bash
cd Supermarket-Sales-Analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## Key Insights

* Revenue varies significantly across months.
* Certain product categories contribute a large share of total sales.
* Peak sales occur during specific shopping hours.
* Discounts influence overall sales performance.
* Product-level analysis helps identify high-revenue items.

---

## Skills Demonstrated

* Data Cleaning
* Data Wrangling
* Exploratory Data Analysis
* Data Visualization
* Dashboard Development
* Business Intelligence
* Python Programming
* Git & GitHub

---

## 👨‍💻 Author

**Pavnesh Bhatt**

Aspiring Data Analyst | Python Enthusiast | Dashboard Developer

GitHub:
https://github.com/Pavneshh

---

⭐ If you found this project useful, consider giving it a star.
