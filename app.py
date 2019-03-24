from flask import (Flask, render_template, redirect, abort,
                   url_for, request, make_response, session, make_response)
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = b'qA9#J[^JAK9&{YATBWVG4&W-|!CF'

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html") 

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if password == "test" and username == "test":
        session['username'] = request.form.get('username')
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if 'username' in session:
        data = []
        if not request.cookies.get('foods'):
            return render_template("dashboard.html", data = data)
        data = json.loads(request.cookies.get('foods'))
        total = 0
        for x in data:
            total += float(x['score'])
        return render_template("dashboard.html", data = data, avgscore = total/len(data))
    else:
        abort(401)

@app.route("/search", methods=['POST'])
def search():
    if 'username' in session:
        query = request.form.get('query').lower()
        with open("output.json") as f: # Use file to refer to the file object
            data = json.loads(f.read())
        for d in data:
            response = make_response(redirect(url_for('dashboard')))
            if query in d['name'].lower():
                if not request.cookies.get('foods'): 
                    foods = [d]
                else:
                    foods = json.loads(request.cookies.get('foods')) + [d]
                print("Foods", foods)
                response.set_cookie('foods', json.dumps(foods))
                return response
        return response
    else:
        abort(401)

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)