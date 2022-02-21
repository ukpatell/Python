from flask import Flask # Import Flask object

app = Flask(__name__)   # Instance of Flask

@app.route('/home/')         # Route to Home
def home():             # Home Function
    return "Home Page"

@app.route('/about/')
def about(): # About Function
    return "About Page"

if __name__ == '__main__':
    app.run(debug=True)

