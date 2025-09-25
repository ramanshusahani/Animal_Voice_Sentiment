from flask import Flask, render_template, jsonify, request
import csv
import os

app = Flask(__name__)

# Load the CSV data when the application starts
# Load the CSV data when the application starts
def load_data():
    animal_sounds_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'animal_sounds.csv')
    
    # Try multiple possible locations
    possible_paths = [
        'animal_sounds.csv',
        csv_path,
        os.path.join(os.getcwd(), 'animal_sounds.csv')
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"CSV file found at: {path}")
                print(f"First 200 characters: {content[:200]}")
                
                file.seek(0)  # Reset file pointer
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    if 'Animal' not in row or 'Sound' not in row or 'Call_For' not in row:
                        print(f"Row {row_num} missing required columns: {row.keys()}")
                        continue
                        
                    animal_sounds_data.append({
                        'Animal': row['Animal'].strip(),
                        'Sound': row['Sound'].strip(),
                        'Call_For': row['Call_For'].strip()
                    })
                
                print(f"Successfully loaded {len(animal_sounds_data)} records from {path}")
                return animal_sounds_data
                
        except FileNotFoundError:
            print(f"CSV file not found at: {path}")
            continue
        except Exception as e:
            print(f"Error loading data from {path}: {e}")
            continue
    
    print("No CSV file found in any location!")
    return []

# Initialize the data
animal_data = load_data()

@app.route('/')
def home():
    """Main route that displays the home page with unique animal names"""
    if not animal_data:
        unique_animals = []
    else:
        unique_animals = sorted(list(set([item['Animal'] for item in animal_data])))
    
    return render_template('index.html', animals=unique_animals)

@app.route('/get_sounds/<animal_name>')
def get_sounds(animal_name):
    """Route to fetch sounds for a selected animal"""
    if not animal_data:
        return jsonify({'sounds': []})
    
    # Get sounds for the selected animal
    animal_sounds = list(set([
        item['Sound'] for item in animal_data 
        if item['Animal'] == animal_name
    ]))
    
    return jsonify({'sounds': sorted(animal_sounds)})

@app.route('/get_call_for', methods=['POST'])
def get_call_for():
    """Route to get the reason (Call_For) for a specific animal sound"""
    if not animal_data:
        return jsonify({'call_for': 'No data available'})
    
    # Get the JSON data from the POST request
    data = request.get_json()
    selected_animal = data.get('animal')
    selected_sound = data.get('sound')
    
    # Find the matching entry
    for item in animal_data:
        if item['Animal'] == selected_animal and item['Sound'] == selected_sound:
            return jsonify({'call_for': item['Call_For']})
    
    return jsonify({'call_for': 'No information found for this combination'})

# Health check endpoint for monitoring
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'data_loaded': len(animal_data) > 0,
        'total_records': len(animal_data)
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
