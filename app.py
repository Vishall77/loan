from flask import Flask, render_template, request, redirect, session, url_for
import pickle
import warnings as w
w.filterwarnings('ignore')
import hashlib

from db import Database

app = Flask(__name__)
app.secret_key = "supersecretkey"
obj = Database()

with open('svm.pkl', 'rb') as f:
    pipe = pickle.load(f)

def hash_pin(pin):
    pin = hashlib.sha256(str(pin).encode()).hexdigest()
    return pin

@app.route("/")
def home():
    if "user" in session:
        return redirect("/predict")
    return redirect("/login")
    

# Here are register route
@app.route("/register", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email_id = request.form.get('email_id')
        phone_no = request.form.get('phone_no')
        password = hash_pin(request.form.get('password'))

        # Check status from database
        status = obj.save_users(name, email_id, phone_no, password)

        if status == "exists":
            # Agar pehle se hai toh error message
            return render_template('register.html', error_msg='Email or Phone Number already registered!')
        elif status == "success":
            # Agar naya hai toh success message
            return render_template('register.html', msg='Account Created Successfully!')
        else:
            return render_template('register.html', error_msg='Something went wrong. Try again.')

    return render_template('register.html')

# Here are login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = request.form.get('email_id')
        password = hash_pin(request.form.get('password'))

        user = obj.check_user(email_id, password)

        if user:
            # user user ka 'name' hai jo hum session mein save kar rahe hain
            session['user'] = user 
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', msg="Invalid Credentials")

    return render_template('login.html')

# Here are dashboard route 
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # Dictionary cursor use karein taaki data {'column_name': value} format mein mile
        dict_cursor = obj.conn.cursor(dictionary=True)
        
        # Predictions fetch karein
        dict_cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
        history = dict_cursor.fetchall()
        
        dict_cursor.close() # Cursor close karna na bhoolein
        
        return render_template('dashboard.html', user=session['user'], history=history)
    
    return redirect(url_for('login'))

# Here are predict route
@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    if "user" not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # 1. Sabse pehle data collect karein
            payload = {
                'Gender': request.form.get('Gender'),
                'Married': request.form.get('Married'),
                'Dependents': request.form.get('Dependents'),
                'Education': request.form.get('Education'),
                'Self_Employed': request.form.get('Self_Employed'),
                'LoanAmount': float(request.form.get('LoanAmount', 0)),
                'Loan_Amount_Term': float(request.form.get('Loan_Amount_Term', 0)),
                'Credit_History': float(request.form.get('Credit_History', 0)),
                'Property_Area': request.form.get('Property_Area'),
                'Family_Income': float(request.form.get('Family_Income', 0))
            }

            # 2. Model se predict karwayein
            # ML model ko list of lists chahiye hota hai
            features = [list(payload.values())]
            prediction_result = pipe.predict(features) 
            
            # Prediction ko payload mein add karein
            payload['Loan_Status'] = str(prediction_result)

            # 3. DB mein save karein (Dictionary bhej rahe hain)
            obj.save_predictions(payload)

            # 4. UI variables
            prob_val = 80 if prediction_result == 'Y' else 30
            
            return render_template('predict.html', 
                                 pred=prediction_result, 
                                 prob=prob_val, 
                                 summary="AI Analysis Successful", 
                                 reasons=["Verified via ML Model"])

        except Exception as e:
            # Agar error aaye toh terminal mein check karein
            print(f">>> APP ERROR: {e}")
            return f"Error in prediction: {e}"

    return render_template('predict.html')


# here are logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
    
