from flask import Flask, render_template, request, redirect, session
import pickle
import warnings as w
w.filterwarnings('ignore')

from db import Database

app = Flask(__name__)
app.secret_key = "supersecretkey"
obj = Database()

with open('svm.pkl', 'rb') as f:
    pipe = pickle.load(f)


@app.route("/")
def home():
    if "user" in session:
        return redirect("/predict")
    return redirect("/login")
    

# Here are register route
@app.route("/register", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        print("Form Data:", request.form)

        name = request.form.get('name')
        email_id = request.form.get('email_id')
        phone_no = request.form.get('phone_no')
        password = request.form.get('password')

        obj.save_users(name, email_id, phone_no, password)

        msg = 'Your Account is Created Successfully'
        return render_template('register.html', msg=msg)

    return render_template('register.html')

# Here are login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = request.form.get('email_id')
        password = request.form.get('password')

        user = obj.check_user(email_id, password)

        if user:
            session['user'] = user[1]
            return redirect('/predict')
        else:
            return render_template('login.html', msg="Invalid Credentials")

    return render_template('login.html')

# Here are dashboard route 
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')


# Here are predict route
@app.route('/predict', methods=['GET', 'POST'])
def prediction():

    if "user" not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        print("Prediction Form:", request.form)

        try:
            Gender = request.form.get('Gender')
            Married = request.form.get('Married')
            Dependents = request.form.get('Dependents')
            Education = request.form.get('Education')
            Self_Employed = request.form.get('Self_Employed')

            LoanAmount = float(request.form.get('LoanAmount'))
            Loan_Amount_Term = float(request.form.get('Loan_Amount_Term'))
            Credit_History = float(request.form.get('Credit_History'))
            Property_Area = request.form.get('Property_Area')
            Family_Income = float(request.form.get('Family_Income'))

            Loan_Status = pipe.predict([[
                Gender, Married, Dependents, Education,
                Self_Employed, LoanAmount, Loan_Amount_Term,
                Credit_History, Property_Area, Family_Income
            ]])[0]

            obj.save_predictions(
                Gender, Married, Dependents, Education,
                Self_Employed, LoanAmount, Loan_Amount_Term,
                Credit_History, Property_Area, Family_Income, Loan_Status
            )

            return render_template('home.html', pred=Loan_Status)

        except Exception as e:
            print("Prediction ERROR:", e)
            return "Error in prediction"

    return render_template('predict.html')


# here are logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
    
