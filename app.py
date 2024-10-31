from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/model')
def model():
    return render_template("about.html")

@app.route('/tools')
def tools():
    return render_template("about.html")

@app.route('/info')
def info():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("about.html")

@app.route('/house-listings')
def house_listings():
    return render_template("listings.html")

@app.route('/house1')
def house1():
    return render_template("house1.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)