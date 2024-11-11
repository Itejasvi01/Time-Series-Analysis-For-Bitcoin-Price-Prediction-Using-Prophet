from flask import Flask,render_template,url_for,redirect,request,jsonify,render_template_string
app = Flask(name)
import pandas as pd
import os
from prophet import Prophet
import matplotlib.pyplot as plt
import mysql.connector
mydb = mysql.connector.connect(
host='localhost',
port=3307,
user='root',
passwd='',
database='Bitcoin'
)
mycur = mydb.cursor()
df = pd.read_csv('bitcoin_2017_to_2023.csv')
## fbprophet
# Example: Resampling to daily data if your data is minute-level
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.resample('D', on='timestamp').mean().reset_index()
# Rename columns for Prophet
df_prophet = df.rename(columns={'timestamp': 'ds', 'close': 'y'})
# Initialize the Prophet model with fewer components
model = Prophet(changepoint_prior_scale=0.01)
# Fit the model
model.fit(df_prophet)
@app.route('/')
def index():
return render_template('index.html')
@app.route('/about')
def about():
return render_template('about.html')
@app.route('/registration', methods=['POST', 'GET'])
def registration():
if request.method == 'POST':
name = request.form['name']
email = request.form['email']
password = request.form['password']
confirmpassword = request.form['confirmpassword']
address = request.form['Address']
if password == confirmpassword:
# Check if user already exists
sql = 'SELECT * FROM users WHERE email = %s'
val = (email,)
mycur.execute(sql, val)
data = mycur.fetchone()
if data is not None:
msg = 'User already registered!'
return render_template('registration.html', msg=msg)
else:
# Insert new user without hashing password
sql = 'INSERT INTO users (name, email, password, Address) VALUES (%s, %s, %s, %s)'
val = (name, email, password, address)
mycur.execute(sql, val)
mydb.commit()
msg = 'User registered successfully!'
return render_template('registration.html', msg=msg)
else:
msg = 'Passwords do not match!'
return render_template('registration.html', msg=msg)
return render_template('registration.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
email = request.form['email']
password = request.form['password']
sql = 'SELECT * FROM users WHERE email=%s'
val = (email,)
mycur.execute(sql, val)
data = mycur.fetchone()
if data:
stored_password = data[2]
# Check if the password matches the stored password
if password == stored_password:
return redirect('/viewdata')
else:
msg = 'Password does not match!'
return render_template('login.html', msg=msg)
else:
msg = 'User with this email does not exist. Please register.'
return render_template('login.html', msg=msg)
return render_template('login.html')
@app.route('/viewdata')
def viewdata():
global df
# Load the dataset
df = pd.read_csv('bitcoin_2017_to_2023.csv')
dummy = df.head(100)
table_html = dummy.to_html(classes='table table-striped table-hover', index=False)
return render_template('viewdata.html', table=table_html)
# Ensure you have a directory to save the plots
GRAPH_DIR = 'static/graphs'
os.makedirs(GRAPH_DIR, exist_ok=True)
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
if request.method == 'POST':
a = int(request.form['year'])
b = int(request.form['month'])
c = int(request.form['day'])
inp = [[60882.90, 62338.43, 60666.19, a, b, c]]
rf = RandomForestRegressor()
rf.fit(x_train, y_train)
result = rf.predict(inp)
return render_template('prediction.html', msg=result)
return render_template('prediction.html')
if name == 'main':
app.run(debug=True)
