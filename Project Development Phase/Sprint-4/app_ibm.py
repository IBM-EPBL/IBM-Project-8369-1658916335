import numpy as np
import os
from flask import Flask, request, jsonify, render_template,json,redirect,url_for,flash
import pickle
import requests
import sqlite3

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "lOTEkqckZ_QiOKlE6ppPzOcQDEG4voYOn7G3Ci9fAbBf"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
app.secret_key="21433253"
model = pickle.load(open('rfmodel.pkl', 'rb'))
conn=sqlite3.connect("database1.db")
conn.execute("CREATE TABLE IF NOT EXISTS login(email TEXT PRIMARY KEY,password TEXT)")
conn.close()

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        try:
            print("request1")
            fv=[x for x in request.form.values()]
            print(fv)
            print([x for x in request.form.values()])
            print(request.form["email"])
            email=request.form["email"]
            pswd=request.form["pswd"]
            print("request2")
            conn=sqlite3.connect("database1.db")
            cur=conn.cursor()
            print(email,pswd)
            cur.execute("SELECT password FROM login WHERE email=?;",(str(email),))
            print("select")
            
            result=cur.fetchone()
            cur.execute("SELECT * FROM login")
            print(cur.fetchall())
            print("fetch")
            if result:
                print("login successfully success")
                print(result)
                if result[0]==pswd:
                    flash("login successfully",'success')
                    return redirect('/home')
                else:
                    return render_template("login.html", error="please enter correct password")
                
            else:
                print("register")
                flash("please Register",'danger')
                
                return redirect('/reg')
            
        except Exception as e:
            print(e)
            print('danger-----------------------------------------------------------------')
            return "hello error" 
    else:
        return render_template("login.html")
#    return render_template('login.html')
@app.route('/reg')
def reg():
    return render_template("register.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        try:
            print("request1")
            fv=[x for x in request.form.values()]
            print(fv)
            print([x for x in request.form.values()])
            print(request.form["email"])
            email=request.form["email"]
            print(request.form["pswd"])
            pswd=request.form["pswd"]
            conn=sqlite3.connect("database1.db")
            print("database")
            cur=conn.cursor()
            print("cursor")
            cur.execute("SELECT * FROM login WHERE email=?;",(str(email),))
            print("fetch")
            result=cur.fetchone()
            if result:
                print("already")
                flash("user already exist,please login",'danger')
                return redirect('/')
            else:
                print("insert")
                cur.execute("INSERT INTO  login(email,password)values(?,?)",(str(email),str(pswd)))
                conn.commit()
                cur.execute("SELECT * FROM login")
                print(cur.fetchall())
                flash("Registered successfully",'success')
                return render_template('login.html')
            
        except Exception as e:
            print(e)
            #flash(e,'danger')
            return "hello error1"
        
            
                #return redirect('/')
   # return render_template('login.html')
@app.route('/home')
def home():
    return render_template('mainpage.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    farr = [int(x) for x in request.form.values()]
    print(farr)
    if farr[7] == 1:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 8:
                farr.append(1)
                continue
            farr.append(0)

    elif farr[7] == 2:
        for i in range(8):
            farr.pop()
            j = 8
            if j == 8:
                farr.append(1)
                continue
            farr.append(0)
    elif farr[7] == 3:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 10:
                farr.append(1)
                continue
            farr.append(0)
    elif farr[7] == 4:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 11:
                farr.append(1)
                continue
            farr.append(0)
    elif farr[7] == 5:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 12:
                farr.append(1)
                continue
            farr.append(0)
    elif farr[7] == 6:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 13:
                farr.append(1)
                continue
            farr.append(0)
    elif farr[7] == 8:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 15:
                farr.append(1)
                continue
            farr.append(0)
    else:
        farr.pop()
        for i in range(8):
            j = 8
            if j == 14:
                farr.append(1)
                continue
            farr.append(0)
    print(farr)
    final_features = [int(x) for x in farr]
    prediction = model.predict([np.array(final_features)])

    output = prediction[0]
    output = round(prediction[0])

    return render_template('result.html', output=output)


if __name__ == "__main__":
    os.environ.setdefault('FLASK_ENV', 'development')
    app.run(debug=False)