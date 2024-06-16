from flask import Flask, request, jsonify, render_template
import json
import spacy
import csv

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("xx_ent_wiki_sm")

# Load policies
with open('library_policies.json', 'r') as f:
    policies = json.load(f)

# Read synonyms from CSV
def load_synonyms(csv_file):
    synonyms = {}
    with open(csv_file, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for rows in reader:
            key = rows[0]
            values = rows[1:]
            synonyms[key] = values
    return synonyms

# Load synonyms
synonyms = load_synonyms('synonyms.csv')

def get_response(user_input):
    user_input = user_input.lower().split()
    print(f"Input Pengguna: {' '.join(user_input)}")  # Logging input pengguna

    for word in user_input:
        for key, values in synonyms.items():
            if word in values:
                print(f"Cocok: {word} -> {key}")  # Logging kecocokan
                # Return the appropriate response from policies
                return policies.get(key, "Informasi tidak tersedia")

    return "Maaf, saya tidak mengerti pertanyaan Anda."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
