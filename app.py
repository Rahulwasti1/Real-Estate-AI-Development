from flask import Flask, render_template, url_for, redirect, request, jsonify
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from markupsafe import Markup

app = Flask(__name__)

data = ('Notebook/Cleaned_Dataset.csv')

# Load the cleaned dataset
try:
    data = pd.read_csv('Notebook/Cleaned_Dataset.csv')
    print("Data loaded successfully")
except Exception as e:
    print(f"Error loading CSV file: {e}")


try:
    scaler = pickle.load(open('Notebook/scaler.pkl', 'rb'))
    xgb_model = pickle.load(open('Notebook/xgb_model.pkl', 'rb'))
    print("Model and scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model or scaler: {e}")

print(type(xgb_model))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
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

@app.route('/model')
def model():
    return render_template("model.html")

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = xgb_model.predict(new_data)
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    selected_Property_Type = int(request.form.get('propertyType'))
    selected_Listing_Type = int(request.form.get('listingType'))
    selected_City = int(request.form.get('city'))
    selected_Address = int(request.form.get('address'))
    Area = float(request.form.get('areaInAana'))
    Bedroom = int(request.form.get('bedroom'))
    Bathroom = int(request.form.get('bathroom'))
    Floors = int(request.form.get('floors'))
    Parking = int(request.form.get('parking'))
    Selected_Road_Type = int(request.form.get('roadType'))
    Garden = int(request.form.get('garden'))

    input_data = np.array([
        selected_Property_Type,
        selected_Listing_Type,
        selected_City,
        selected_Address,
        Area,
        Bedroom,
        Bathroom,
        Floors,
        Parking,
        Selected_Road_Type,
        Garden
    ]).reshape(1, -1)

    scaled_data = scaler.transform(input_data)
    output = xgb_model.predict(scaled_data)[0]

    print("Scaled Data:", scaled_data)
    print("Shape of Scaled Data:", scaled_data.shape)
    output = xgb_model.predict(scaled_data)[0]

    output = abs(output)

    return render_template('model.html', output=output)

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


@app.route('/past-data', methods=['GET', 'POST'])
def visualization():
    selected_question = request.form.get('question', 'city_sales')  # Default to 'city_sales'
    
    # Define different visualizations based on the question selected
    if selected_question == 'city_sales':
        # Count sales per city
        city_sales = data['City'].value_counts().reset_index()
        city_sales.columns = ['City', 'Sales Count']
        fig = px.bar(city_sales, x='City', y='Sales Count', title="Sales Count by City",
                     color='Sales Count', color_continuous_scale='Viridis')
    
    elif selected_question == 'year_sales':
        # Proportion of sales per year
        year_sales = data['Year'].value_counts().reset_index()
        year_sales.columns = ['Year', 'Sales Count']
        fig = px.pie(year_sales, names='Year', values='Sales Count', title='Proportion of Sales by Year')
    
    elif selected_question == 'road_type_sales':
        # Road type distribution
        road_type_sales = data['Road Type'].value_counts().reset_index()
        road_type_sales.columns = ['Road Type', 'Sales Count']
        fig = px.pie(road_type_sales, names='Road Type', values='Sales Count', hole=0.4,
                     color_discrete_sequence=['#A1B5D8', '#D9C2BA', '#F1DCA7', '#B8A79E', '#A0A8A8', '#D1D5DE'],
                     title="Sales Distribution by Road Type")
    
    elif selected_question == 'address_sales':
        # Count sales by address
        address_sales = data['Address'].value_counts().reset_index()
        address_sales.columns = ['Address', 'Sales Count']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=address_sales['Address'], y=address_sales['Sales Count'], mode='markers', marker=dict(size=10, color='#008080')))
        fig.add_trace(go.Scatter(x=address_sales['Address'], y=address_sales['Sales Count'], mode='lines', line=dict(color='#008080')))
        fig.update_layout(title="Sales by Address", xaxis_title="Address", yaxis_title="Sales Count")
    
    elif selected_question == 'property_sales':
        # Property type distribution
        property_sales = data['Property_Type'].value_counts().reset_index()
        property_sales.columns = ['Property_Type', 'Sales Count']
        fig = px.scatter(property_sales, x="Sales Count", y="Sales Count", size="Sales Count", color="Property_Type",
                         title="Property Type Distribution", hover_name="Property_Type", size_max=60)
        fig.update_layout(showlegend=False)

    # Convert the figure to HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('historical_data.html', graph_html=graph_html, selected_question=selected_question)


if __name__ == "__main__":
    app.run(debug=True, port=4000)