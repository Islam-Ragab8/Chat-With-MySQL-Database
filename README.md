 # 💬 Chat With MySQL Database  
A simple and powerful application that lets you chat with your MySQL database using an AI LLM powered by LangChain and Groq.  
You can ask any question in natural language, and the AI will translate it into SQL, execute it, and return a clean natural-language answer! 🚀

---

## 📁 Project Structure
```bash
CHAT-WITH-MYSQL-DATABASE/
│── assets/
│ └── schema.py # Core logic (SQL chain + response chain)
│── Data/
│── app.py # Streamlit UI
│── .env # Environment variables (GROQ_API_KEY, DB credentials)
│── README.md
│── venv/
```


---

## 🧠 How It Works

### 🔹 1. **User Question → SQL Query (SQL Chain)**
The LLM (Groq + LLaMA model) generates a valid SQL query based on:
- User question  
- Database schema  
- Chat history  

---

### 🔹 2. **Execute SQL Query**
The generated SQL is executed using LangChain's `SQLDatabase`.

---

### 🔹 3. **SQL Results → Natural Language Response**
The SQL result is fed back into the LLM, which converts it into a human-friendly answer.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Islam-Ragab8/Chat-With-MySQL-Database.git
cd Chat-With-MySQL-Database
```

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

## 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

## 4️⃣ Create a .env File
```bash
GROQ_API_KEY=your_api_key_here
```

## ▶️ Running the App
```
streamlit run app.py
```