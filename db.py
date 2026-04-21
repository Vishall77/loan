import mysql.connector as sql
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class Database:
    def __init__(self):
        # Establish connection using environment variables
        self.conn = sql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv('DB_NAME'),
        )
        self.cursor = self.conn.cursor()

        # Create table for storing model predictions
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            id INT PRIMARY KEY AUTO_INCREMENT,
            Gender VARCHAR(10),
            Married VARCHAR(10),
            Dependents VARCHAR(10),
            Education VARCHAR(20),
            Self_Employed VARCHAR(10),
            LoanAmount FLOAT,
            Loan_Amount_Term FLOAT,
            Credit_History FLOAT,
            Property_Area VARCHAR(20),
            Family_Income FLOAT,
            Loan_Status VARCHAR(10),
            prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create table for user accounts
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data(
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            email_id VARCHAR(100) UNIQUE,
            phone_no VARCHAR(15) UNIQUE,
            password VARCHAR(255)
        )
        """)
        self.conn.commit()

    def save_predictions(self, data):
        """Expects a dictionary 'data' with all form fields and Loan_Status"""
        try:
            query = """
            INSERT INTO predictions (
                Gender, Married, Dependents, Education, Self_Employed,
                LoanAmount, Loan_Amount_Term, Credit_History,
                Property_Area, Family_Income, Loan_Status
            )
            VALUES (
                %(Gender)s, %(Married)s, %(Dependents)s, %(Education)s, %(Self_Employed)s,
                %(LoanAmount)s, %(Loan_Amount_Term)s, %(Credit_History)s,
                %(Property_Area)s, %(Family_Income)s, %(Loan_Status)s
            )
            """
            self.cursor.execute(query, data)
            self.conn.commit()
            print(">>> SUCCESS: Prediction saved to Database")
            return True
        except Exception as e:
            print(f">>> DATABASE ERROR: {e}")
            return False

    def save_users(self, name, email_id, phone_no, password):
        """Hashes password and saves new user after checking duplicates"""
        try:
            # 1. Check if email or phone already exists
            check_query = "SELECT * FROM user_data WHERE email_id = %s OR phone_no = %s"
            self.cursor.execute(check_query, (email_id, phone_no))
            existing_user = self.cursor.fetchone()
            
            if existing_user:
                return "exists"  # Agar user mil gaya toh 'exists' return karo

            # 2. Agar nahi mila toh insert karo
            # hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = "INSERT INTO user_data (name, email_id, phone_no, password) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (name, email_id, phone_no, password))
            self.conn.commit()
            return "success"

        except Exception as e:
            print(f"Database Error: {e}")
            return "error"

    def check_user(self, email_id, password):
        try:
            # 1. User ko email ke basis par fetch karein
            query = "SELECT * FROM user_data WHERE email_id = %s"
            self.cursor.execute(query, (email_id,)) 
            user = self.cursor.fetchone()

            if user:
                # Index 4 par password hota hai
                stored_password = user

                # Agar stored password string hai, toh use bytes mein convert karein
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')

                # User ke entered password ko hash ke saath match karein
                if password:
                    return user  # Success: User data return karein
            
            return None  # Failure: User nahi mila ya password galat hai

        except Exception as e:
            print(f"Login Error: {e}")
            return None
