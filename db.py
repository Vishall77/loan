import mysql.connector as sql
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class Database:
    def __init__(self):
        self.conn = sql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv('DB_NAME'),
        )
        print("Connected DB:", os.getenv("DB_NAME"))

        self.cursor = self.conn.cursor()
        print("Connection Built to Aiven Successfully")

        # Create tables
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
            Loan_Status VARCHAR(10)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data(
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            email_id VARCHAR(100) UNIQUE,
            phone_no VARCHAR(15) UNIQUE,
            password VARCHAR(200)
        )
        """)

        self.conn.commit()
        print("Tables Created")

    def save_predictions(self, Gender, Married, Dependents, Education,
                         Self_Employed, LoanAmount, Loan_Amount_Term,
                         Credit_History, Property_Area, Family_Income, Loan_Status):
        try:
            query = """
            INSERT INTO predictions(
                Gender, Married, Dependents, Education, Self_Employed,
                LoanAmount, Loan_Amount_Term, Credit_History,
                Property_Area, Family_Income, Loan_Status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(query, (
                Gender, Married, Dependents, Education,
                Self_Employed, LoanAmount, Loan_Amount_Term,
                Credit_History, Property_Area, Family_Income, Loan_Status
            ))

            self.conn.commit()
            print("Prediction saved successfully")

        except Exception as e:
            print("Prediction DB ERROR:", e)

    def save_users(self, name, email_id, phone_no, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query = """
            INSERT INTO user_data (name, email_id, phone_no, password)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email_id, phone_no, hashed_password))
            self.conn.commit()

            print("User saved successfully")

        except Exception as e:
            print("User DB ERROR:", e)

    # This is for checking users from database to login
    def check_user(self, email_id, password):
        try:
            query = "SELECT * FROM user_data WHERE email_id = %s"
            self.cursor.execute(query, (email_id,))   

            user = self.cursor.fetchone()

            if user:
                stored_password = user[4]

                # convert to bytes if stored as string
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')

                print("Entered:", password)
                print("Stored:", stored_password)

                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    return user

            return None

        except Exception as e:
            print("Login ERROR:", e)
            return None


    # def show_users(self):
    #     self.cursor.execute("SELECT * FROM user_data")
    #     self.conn.commit()


# obj = Database()
# obj.show_users()
