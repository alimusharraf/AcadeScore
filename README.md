# 📊 AcadeScore

## 🎓 *A Random Forest Machine Learning Framework for Tracking Student Performance Based on Lifestyle Factors*

AcadeScore is a web-based intelligent system that predicts and tracks student academic performance by analyzing both academic and lifestyle factors. The system uses a **Random Forest Machine Learning model** to provide early performance insights, helping students improve their outcomes through data-driven feedback.

---

## 🚀 Features

* 🔐 Secure User Authentication (Login/Register)
* 📥 Daily Lifestyle & Academic Data Entry
* 🤖 Machine Learning-Based Score Prediction
* 📊 Interactive Performance Dashboard
* 📈 Weekly & Monthly Performance Analysis
* 📉 Consistency Score Calculation
* 🔄 Improvement Tracking
* 💡 Personalized Suggestions for Improvement
* 🗂 History with Filtering & Pagination
* ✏ Edit & Delete Records
* 📤 Export Data to CSV

---

## 🧠 Machine Learning Model

* **Algorithm:** Random Forest
* **Model File:** `Random_Forest.pkl`
* **Input Features:**

  * Study Hours per Day
  * Social Media Usage
  * Part-time Job Status
  * Attendance Percentage
  * Sleep Hours
  * Mental Health Rating

The model predicts a student's **expected academic score**, enabling proactive improvement.

---

## 🏗 System Architecture

1. User inputs data through web interface
2. Flask backend processes the input
3. Data is passed to the trained ML model
4. Model generates prediction
5. Results displayed with insights & suggestions

(See project presentation for detailed architecture) 

---

## 🛠 Tech Stack

### 🔹 Backend

* Python
* Flask 
* SQLAlchemy
* Flask-Login

### 🔹 Frontend

* HTML
* CSS (Glassmorphism UI Design) 

### 🔹 Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

---

## 📂 Project Structure

```
AcadeScore/
│
├── app.py                # Main Flask application
├── Random_Forest.pkl     # Trained ML model
├── templates/            # HTML templates
├── static/
│   └── style.css         # UI styling
├── acadescore.db         # SQLite database
├── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/alimusharraf/acadescore.git
cd acadescore
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📊 Dashboard Insights

* 📌 Latest Performance Score
* 📅 Weekly & Monthly Averages
* 📉 Consistency Score (based on standard deviation)
* 🔄 Improvement Tracker
* 💡 Smart Suggestions

---

## 🔐 Authentication

* Password hashing for security
* Session-based login
* User-specific data isolation

---

## 📤 Data Export

Users can download their performance data in CSV format for analysis.

---

## 🎯 Objectives

* Predict student performance before exams
* Analyze impact of lifestyle factors
* Provide actionable feedback
* Support data-driven academic improvement

(Aligned with project presentation) 

---

## 🧩 Future Enhancements

* 📱 Mobile Application
* 📊 Advanced Data Visualization
* 🤖 Deep Learning Integration
* 🎯 Personalized Study Recommendations
* ☁ Cloud Deployment

---

## 👨‍💻 Authors

* Musharraf Ali
* Lavanya G ( Contributor)
* Jayalakshmi T H

---

## 🙏 Acknowledgment

Guided by **Mrs. Shylaja D N**, Assistant Professor, Dept. of CSE.

---

## 📌 License

This project is developed for academic and educational purposes.
