from flask import Flask,render_template,url_for # Import Flask object

app = Flask(__name__)   # Instance of Flask

@app.route('/')         # Route to Home
def home():             # Home Function
    return render_template('home.html')

@app.route('/about/')
def about(): # About Function
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

