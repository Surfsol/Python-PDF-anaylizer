# Python-PDF-anaylizer
# PDF Data Extraction and Analysis App

## Project Goal

This application allows users to:
- Upload PDF files
- Extract tables and text from the PDFs
- Organize and store the extracted data into a SQL database
- Analyze and visualize the data through an interactive web app

The app is designed to simplify the workflow of handling PDF data by automating extraction, storage, analysis, and visualization.

---

## Technology Stack

| Purpose | Tool |
|:---|:---|
| Code Editor | VS Code |
| Language | Python |
| PDF Reading | pdfplumber |
| Data Handling | pandas |
| Database | sqlite3 (or SQLAlchemy) |
| Data Visualization | matplotlib, seaborn, plotly |
| Web App Dashboard | Streamlit |

---

## Folder Structure

```bash
pdf-data-analyzer/
│
├── extractor.py        # Extracts data from PDFs
├── db.py               # Handles saving and querying SQLite database
├── app.py              # Streamlit app to interact with users
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
├── data/               # Folder for input PDFs
├── database/           # SQLite database files
└── outputs/            # Exported CSVs or processed data


To start project:
create virtual Environment:
python -m venv venv
venv\Scripts\activate


## 🚀 To Start the Project

1. **Create a Virtual Environment**

   Open your terminal and run:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - On **Mac/Linux**:

     ```bash
     source venv/bin/activate
     ```

3. **Install Project Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**

   ```bash
   python -m streamlit run app.py
   ```
5. **If get error ModuleNotFoundError: No module named 'fitz'**
   pip install PyMuPDF