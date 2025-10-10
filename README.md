# CerebroGuard: The Context-Aware Phishing Shield 🧠

CerebroGuard is an intelligent security system designed to combat sophisticated spear-phishing attacks by moving beyond traditional keyword filtering. It analyzes the underlying context, relationships, and behavioral patterns within communications to identify threats that would otherwise go unnoticed.

## 🚀 Live Demo

The fully functional prototype is deployed on Render and is accessible at:

**[https://cerebroguard-ankitb.onrender.com](https://cerebroguard-ankitb.onrender.com)** ---

## 📸 Screenshot
https://github.com/ANKITB032/CerebroGuard/issues/1#issue-3503332844

## 🛠️ Built With

* **Backend:** Python, Flask, Gunicorn
* **Data & AI/ML:** Pandas, NetworkX, spaCy
* **Frontend:** HTML5, CSS3, JavaScript (ES6)
* **Deployment:** Git, GitHub, Render

## ✨ Key Features

* **Dual-Engine Analysis:** Combines historical communication graph analysis with universal NLP-based threat detection.
* **Evidence-Based Scoring:** Provides a nuanced risk score and clear evidence factors instead of a simple binary verdict.
* **Context-Aware:** Understands relationships to spot anomalies that traditional tools miss.
* **Extensible Design:** New analysis modules can be easily added to counter evolving threats.


## ⚙️ Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.10+
* pip & venv

### Installation

1.  **Clone the repo:**
    ```sh
    git clone [https://github.com/ANKITB032/CerebroGuard.git](https://github.com/ANKITB032/CerebroGuard.git)
    cd CerebroGuard
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Download the spaCy model:**
    ```sh
    python3 -m spacy download en_core_web_sm
    ```
5.  **Run the Flask application:**
    ```sh
    python3 app.py
    ```
6.  Open your browser and navigate to `http://127.0.0.1:5000`.

**(Note: This setup uses the pre-computed `enron_graph.gpickle`. To regenerate this file, you would first need to download the Enron dataset and run the `parser.py` and `graph_builder.py` scripts.)**