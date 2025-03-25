import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load saved model, scaler, and encoders
rf_model = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# DNA base mapping
DNA_MAPPING = {
    "A": 1,
    "C": 2,
    "G": 3,
    "T": 4,
    "U": 5,
    "R": 6,
    "Y": 7,
    "S": 8,
    "W": 9,
    "K": 10,
    "M": 11,
    "B": 12,
    "D": 13,
    "H": 14,
    "V": 15,
    "N": 16,
}

MAX_DNA_LENGTH = 100  # Should match training
    

# Convert DNA sequence to numerical features
def preprocess_input_data(dna_sequence):
    numeric_sequence = [DNA_MAPPING.get(base, 0) for base in dna_sequence]

    # Ensure length is exactly MAX_DNA_LENGTH
    if len(numeric_sequence) > MAX_DNA_LENGTH:
        numeric_sequence = numeric_sequence[:MAX_DNA_LENGTH]
    else:
        numeric_sequence += [0] * (MAX_DNA_LENGTH - len(numeric_sequence))

    # Convert to NumPy array and reshape
    input_data = np.array(numeric_sequence).reshape(1, -1)
    return scaler.transform(input_data)  # Scale input


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        dna_sequence = data.get("dna_sequence", "")

        if not dna_sequence:
            return (
                jsonify({"message": "DNA sequence is required!", "status": "error"}),
                400,
            )

        # Preprocess DNA input
        input_data_scaled = preprocess_input_data(dna_sequence)

        # Make predictions
        prediction = rf_model.predict(input_data_scaled)[0]

        # Decode predictions back to categorical labels
        predicted_attributes = {}
        categorical_columns = list(label_encoders.keys())

        for i, col in enumerate(categorical_columns):
            predicted_value = int(prediction[i])
            predicted_attributes[col] = label_encoders[col].inverse_transform(
                [predicted_value]
            )[0]

        return jsonify({"status": "success", "predictions": predicted_attributes})

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


NESTJS_API_URL = "http://localhost:5001/suspicion/find-all"


def get_all_suspicions():
    """Retrieve all stored STR vectors from NestJS backend."""
    try:
        response = requests.get(NESTJS_API_URL)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NestJS: {e}")
        return []


def extract_dna_metadata(dna_sequence):

    try:
        # Preprocess DNA input
        input_data_scaled = preprocess_input_data(dna_sequence)

        # Make predictions
        prediction = rf_model.predict(input_data_scaled)[0]

        # Decode predictions back to categorical labels
        predicted_attributes = {}
        categorical_columns = list(label_encoders.keys())

        for i, col in enumerate(categorical_columns):
            predicted_value = int(prediction[i])
            predicted_attributes[col] = label_encoders[col].inverse_transform(
                [predicted_value]
            )[0]
        return predicted_attributes
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/find_match", methods=["POST"])
def find_match():
    data = request.json
    dna_sequence = data.get("dna_sequence")

    if not dna_sequence:
        return jsonify({"error": "No DNA sequence provided"}), 400
    
    # Extract metadata from DNA sequence
    extracted_metadata = extract_dna_metadata(dna_sequence)
    
    if isinstance(extracted_metadata, tuple):  # Handle errors from extract_dna_metadata
        return extracted_metadata
    
    # Find matching suspicions based on extracted metadata
    matching_suspicions = find_matching_suspicions(extracted_metadata)

    # Return the matching suspicions
    return jsonify(matching_suspicions)


def find_matching_suspicions(extracted_metadata):
    suspicions = get_all_suspicions()
    # List to store suspicions that match
    matching_suspicions = []

    for suspicion in suspicions:
        # Check if 'metaData' and 'predictions' are available and not None
        if suspicion.get('metaData') and 'predictions' in suspicion['metaData']:
            metadata = suspicion['metaData']['predictions']
            print(f"Suspicion ID: {suspicion.get('id')}")
            print("MetaData from suspicion (predictions): ", metadata)
            print("Extracted metadata: ", extracted_metadata)

            # Compare the extracted metadata fields with the metadata of the suspicion (predictions)
            if (
                metadata.get('Ear_Shape') == extracted_metadata.get('Ear_Shape') and
                metadata.get('Eye_Color') == extracted_metadata.get('Eye_Color') and
                metadata.get('Hair_Color') == extracted_metadata.get('Hair_Color') and
                metadata.get('Gender') == extracted_metadata.get('Gender') and
                metadata.get('Skin_Color') == extracted_metadata.get('Skin_Color')
            ):
                print("Match found!")
                matching_suspicions.append(suspicion)
            else:
                print("No match.")

    print(f"Matching suspicions found: {len(matching_suspicions)}")
    return matching_suspicions



# def count_str_repeats(dna_sequence, str_markers):
#     """Count occurrences of STR markers in the given DNA sequence."""
#     return [dna_sequence.count(marker) for marker in str_markers]

# def find_nearest_match(input_vector):
#     suspicions = get_all_suspicions()

#     if not suspicions:
#         return {"message": "No DNA records found"}

#     best_match = None
#     highest_similarity = -1

#     # List of markers you're using to count STR repeats
#     str_markers = [
#         "D3S1358", "TH01", "D21S11", "D18S51", "Penta_E", "D5S818", "D13S317",
#         "D7S820", "D16S539", "CSF1PO", "Penta_D", "vWA", "D8S1179", "TPOX",
#         "FGA", "D19S433", "D2S1338", "D22S1045", "D17S1301", "D10S1248",
#         "D1S1656", "D12S391"
#     ]

#     for suspicion in suspicions:
#         # Ensure that the suspicion's strVector has the same length as input_vector
#         if len(suspicion['strVector']) != len(str_markers):
#             continue  # Skip this suspicion if the number of markers don't match

#         str_vector = np.array(suspicion['strVector'])

#         # Calculate similarity using cosine similarity
#         similarity = cosine_similarity([input_vector], [str_vector])[0][0]

#         if similarity > highest_similarity:
#             highest_similarity = similarity
#             best_match = suspicion

#     return best_match if best_match else {"message": "No match found"}


# @app.route("/find_match", methods=["POST"])
# def find_match():
#     data = request.json
#     dna_sequence = data.get("dna_sequence")

#     if not dna_sequence:
#         return jsonify({"error": "No DNA sequence provided"}), 400

#     # Convert input DNA to STR vector
#     input_vector = count_str_repeats(dna_sequence, [
#         "D3S1358", "TH01", "D21S11", "D18S51", "Penta_E", "D5S818", "D13S317",
#         "D7S820", "D16S539", "CSF1PO", "Penta_D", "vWA", "D8S1179", "TPOX",
#         "FGA", "D19S433", "D2S1338", "D22S1045", "D17S1301", "D10S1248", "D1S1656",
#         "D12S391"
#     ])

#     # Find the best match
#     best_match = find_nearest_match(input_vector)
#     return jsonify(best_match)


if __name__ == "__main__":
    app.run(debug=True)
