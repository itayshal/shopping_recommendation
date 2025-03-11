# 🛍 Smart Shopping Assistant

A **Conversational AI Shopping Assistant** that helps users find the best products based on their queries. The system integrates **Flask** (backend API) with **Streamlit** (frontend UI), and includes a **recommendation system** powered by **OpenAI** and **semantic search**.

---

## 📌 Features
✔ **Multi-turn dialogue** – Understands user preferences over time.  
✔ **AI-powered recommendations** – Uses OpenAI API and embeddings for semantic similarity.  
✔ **Cold Start Handling** – Provides fallback recommendations when no matching products exist.  
✔ **Persistent Search History** – Saves past queries and results in `recommendations.json`.  
✔ **User-Friendly UI** – Built with **Streamlit** for easy interaction.  

---

## 📂 Project Structure
```
shopping_recommendation/
│── venv-tolstoy/         # Virtual environment (local dependencies)
│── .env                  # API key storage (not committed)
│── app.py                # Flask backend (API)
│── app_ui.py             # Streamlit frontend (UI)
│── products.json         # Product dataset
│── recommendations.json  # Saved user search history
│── cleaned_products.json # Processed product data
│── requirements.txt      # Project dependencies
│── README.md             # Project documentation
```

---

## 🚀 Setup & Installation

### 1️⃣ Install Git & Clone the Repository
```bash
# If Git is not installed, download & install it first
git clone https://github.com/itayshal/shopping_recommendation.git
cd shopping_recommendation
```

### 2️⃣ Set Up Virtual Environment
```bash
# If using Python 3.9+, create and activate a virtual environment
python -m venv venv-tolstoy
source venv-tolstoy/bin/activate  # On macOS/Linux
venv-tolstoy\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up API Key
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your-api-key-here
```

---

## 🖥 Running the Project

### 1️⃣ Start Flask Backend (API)
```bash
python app.py
```
Runs on `http://127.0.0.1:5000/`

### 2️⃣ Start Streamlit Frontend (UI)
```bash
streamlit run app_ui.py
```
Runs on `http://127.0.0.1:8501/`

---

## 🔍 How It Works
1️⃣ **User enters a query** (e.g., "Find me a gaming laptop under $1500").  
2️⃣ **Flask API processes the request**, extracts structured details using OpenAI.  
3️⃣ **Product recommendations are retrieved** based on semantic similarity, rating, and review count.  
4️⃣ **Cold Start Handling** – If no good results exist, popular products are suggested.  
5️⃣ **Recommendations are stored** in `recommendations.json` for future reference.  
6️⃣ **User can view search history** and past recommendations.

---

## 📌 How to View Search History?
👉 **All past queries and recommendations are stored in `recommendations.json`**  
👉 **Click the "Show Search History" button in Streamlit UI**  

---

## 🔄 Updating the Project
To save changes and push to GitHub:
```bash
git add .
git commit -m "Updated recommendation system & UI improvements"
git push origin main
```

---

## 🛠 Future Improvements
🔹 Improve **multi-turn conversation** and user profiling.  
🔹 Enhance **product filtering** by adding more attributes.  
🔹 Implement **database storage** instead of JSON files.  
🔹 Deploy on **AWS/GCP** for public use.  

---

## 📢 Final Notes
✔ **This project is for ML Test Assignment**.  
✔ **Designed for interactive product recommendations**.  
✔ **Fully documented & ready for submission**.  

---
🔗 **GitHub Repository:** [shopping_recommendation](https://github.com/itayshal/shopping_recommendation)  

---

### ✅ Ready to Submit! 🚀  
📌 **Upload your code to GitHub and send the repository link.** Let me know if you need any modifications! 💪
