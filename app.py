from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Load the CSV data when the application starts
def load_data():
    try:
        df = pd.read_csv('animal_sounds.csv')
        return df
    except FileNotFoundError:
        print("Error: animal_sounds.csv file not found!")
        return pd.DataFrame()

# Initialize the DataFrame
animal_data = load_data()

@app.route('/')
def home():
    """Main route that displays the home page with unique animal names"""
    if animal_data.empty:
        unique_animals = []
    else:
        unique_animals = sorted(animal_data['Animal'].unique().tolist())
    
    return render_template('index.html', animals=unique_animals)

@app.route('/get_sounds/<animal_name>')
def get_sounds(animal_name):
    """Route to fetch sounds for a selected animal"""
    if animal_data.empty:
        return jsonify({'sounds': []})
    
    # Filter DataFrame to get sounds for the selected animal
    animal_sounds = animal_data[animal_data['Animal'] == animal_name]['Sound'].unique().tolist()
    
    return jsonify({'sounds': sorted(animal_sounds)})

@app.route('/get_call_for', methods=['POST'])
def get_call_for():
    """Route to get the reason (Call_For) for a specific animal sound"""
    if animal_data.empty:
        return jsonify({'call_for': 'No data available'})
    
    # Get the JSON data from the POST request
    data = request.get_json()
    selected_animal = data.get('animal')
    selected_sound = data.get('sound')
    
    # Filter DataFrame to find the matching row
    matching_row = animal_data[
        (animal_data['Animal'] == selected_animal) & 
        (animal_data['Sound'] == selected_sound)
    ]
    
    if not matching_row.empty:
        call_for = matching_row.iloc[0]['Call_For']
        return jsonify({'call_for': call_for})
    else:
        return jsonify({'call_for': 'No information found for this combination'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)