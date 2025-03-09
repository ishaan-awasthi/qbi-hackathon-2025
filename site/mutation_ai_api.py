import pandas as pd
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load dataset
file_path = "./final_scoring_results.csv"
df = pd.read_csv(file_path)

# Set OpenAI API Key (Replace this with your actual API key)
openai.api_key = "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"

def query_gpt(prompt):
    """Query OpenAI's GPT model to extract the classification."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a protein mutation analysis assistant. Your task is to find the mutation in the provided CSV and return its classification. Do not say anything else but SIMULATIONS SAY: followed by whatever the classifcation is."},
            {"role": "user", "content": prompt},
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

def find_mutation(residue_location, current_residue, mutated_residue):
    """Construct mutation format and find relevant data in the CSV."""
    mutation_query = f"{current_residue}_{residue_location}"
    matching_row = df[df["Mutation"].str.contains(mutation_query, na=False)]
    if matching_row.empty:
        return None
    return matching_row.to_string(index=False)  # Convert row to string for GPT to read

def get_classification(residue_location, current_residue, mutated_residue):
    """Find mutation data and ask GPT to extract the classification column."""
    mutation_data = find_mutation(residue_location, current_residue, mutated_residue)
    if mutation_data is None:
        return "No relevant mutation data found."
    
    prompt = f"""
    Here is a CSV table containing mutation data:
    {mutation_data}
    
    Find and return the value in the 'Classification' column from the given data.
    """
    return query_gpt(prompt)

# Flask App
app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    """Receive user input, process mutation, and return classification."""
    data = request.json
    classification = get_classification(data["residue_location"], data["current_residue"], data["mutated_residue"])
    return jsonify({"classification": classification})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)