from flask import Flask, render_template, url_for, redirect
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from markupsafe import Markup

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

@app.route('/home-loan-eligibility-calculator')
def eligibility():
    return render_template("eligibilitycalc.html")

@app.route('/contact')
def contact():
    return render_template("about.html")

@app.route('/house-listings')
def house_listings():
    return render_template("listings.html")

@app.route('/house1')
def house1():
    return render_template("house1.html")

@app.route('/lending-procedure')
def lending_procedure():
    return render_template("LoanProcessByBank.html")

# Visualizations
@app.route('/market-trends')
def marketTrends():
    df = pd.read_csv("Notebook/RealEstate_dataset.csv")
    table_html = df.to_html(classes='data', index=True)

    # Data
    years = [
        "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", 
        "2025", "2026", "2027", "2028", "2029"
    ]
    commercial_real_estate = [
        24.28, 27.87, 32.20, 35.99, 39.11, 43.70, 48.85, 59.77, 
        63.59, 66.41, 68.39, 69.72, 70.58
    ]
    residential_real_estate = [
        266.00, 316.10, 309.30, 331.00, 330.50, 353.60, 359.30, 377.40, 
        390.30, 403.30, 416.40, 429.50, 442.70
    ]
    total = [
        290.30, 344.00, 341.50, 367.00, 369.60, 397.30, 408.20, 437.20, 
        453.90, 469.70, 484.80, 499.20, 513.30
    ]

    fig = go.Figure()

    # Add traces for each category
    fig.add_trace(go.Bar(x=years, y=commercial_real_estate,  name='Commercial Real Estate'))
    fig.add_trace(go.Bar(x=years, y=residential_real_estate, name='Residential Real Estate'))
    fig.add_trace(go.Bar(x=years, y=total, name='Total'))

    fig.update_layout(
        title="Real Estate Market of Nepal in Billion USD (US$)",
        xaxis_title="Year",
        yaxis_title="Value (Billion USD)",
        legend_title="Category",
        template="plotly_white",
        height=600,
        width=1500
    )

    plot = fig.to_html(full_html=True)

    return render_template("marketTrends.html", table=table_html, graph_html=Markup(plot))

























if __name__ == "__main__":
    app.run(debug=True, port=4000)