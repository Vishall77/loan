# 🏦 Loan Approval Prediction System

A Full-Stack Machine Learning Web Application that predicts whether a user's loan will be approved based on financial and personal details.

This project combines **Machine Learning + Flask + MySQL + Authentication System** to simulate a real-world fintech application.

---

# 🚀 Features

✅ User Registration & Login Authentication
✅ Secure Password Hashing using bcrypt
✅ Loan Approval Prediction using Machine Learning
✅ Prediction Results Stored in MySQL Database
✅ Responsive & Interactive Banking UI
✅ Session Management
✅ Mobile-Friendly Design
✅ Real-Time Loan Eligibility Check
✅ Explanation Logic for Loan Approval/Rejection

---

# 🧠 Machine Learning Model

The prediction system uses a trained **Support Vector Machine (SVM)** model for classification.

### Features Used:

* Gender
* Marital Status
* Dependents
* Education
* Employment Status
* Loan Amount
* Loan Term
* Credit History
* Property Area
* Family Income

---

# 🛠️ Tech Stack

## Frontend

* HTML5
* CSS3

## Backend

* Python
* Flask

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Database

* MySQL

## Authentication

* bcrypt
* Flask Sessions

---

# 📂 Project Structure

```bash
LOAN_APPROVAL_SYSTEM/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── predict.html
│   ├── home.html
│   └── dashboard.html
│
├── src/
│   └── db.py
│
├── svm.pkl
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

---

## 2️⃣ Move into Project Folder

```bash
cd LOAN_APPROVAL_SYSTEM
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Setup

Create a MySQL database.

Example:

```sql
CREATE DATABASE loan_db;
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
DB_NAME=loan_db
```

---

# ▶️ Run Application

```bash
python app.py
```

Server will run on:

```bash
http://127.0.0.1:5000
```

---

# 📸 Application Screens

## 🔐 Login Page

* Secure login system
* Session handling

## 📝 Registration Page

* User account creation
* Duplicate email protection

## 🤖 Prediction Page

* Loan eligibility prediction
* Interactive UI

---

# 🔒 Security Features

✅ Password Hashing using bcrypt
✅ Session-Based Authentication
✅ Duplicate User Handling
✅ Protected Routes

---

# 💡 Future Improvements

* SHAP Explainable AI
* Admin Dashboard
* Email Notifications
* Prediction Analytics
* REST API Integration
* React Frontend
* Cloud Deployment

---

# 🌐 Deployment

This project can be deployed using:

* Render
* Railway
* PythonAnywhere

---

# 👨‍💻 Author

### Vishal Baghel

Aspiring Data Scientist & Python Developer passionate about building Machine Learning and Full-Stack Applications.

---

# 📌 GitHub Repository

Add your repository link here:

```bash
https://github.com/YOUR_USERNAME/YOUR_REPOSITORY
```

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub.
