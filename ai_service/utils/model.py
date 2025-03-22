import joblib
import numpy as np


# Load saved model, scaler, and encoder
def load_model():
    rf_model = joblib.load("models/rf_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    encoder = joblib.load("models/encoder.pkl")
    return rf_model, scaler, encoder

 
# Preprocess input DNA sequence (convert to numerical data, scale, etc.)
def preprocess_input_data(dna_sequence):
    """
    Convert DNA sequence into numerical representation.
    Example: "AGCT" → [1, 3, 2, 4]  
    """
    # Define mapping for DNA bases to numerical values
    DNA_MAPPING = {
    'A': 1,  # Adenine
    'C': 2,  # Cytosine
    'G': 3,  # Guanine
    'T': 4,  # Thymine (DNA only)
    'U': 5,  # Uracil (RNA only)
    
    # Ambiguous bases (IUPAC codes)
    'R': 6,  # Purine (A or G)
    'Y': 7,  # Pyrimidine (C or T)
    'S': 8,  # Strong (G or C)
    'W': 9,  # Weak (A or T)
    'K': 10, # Keto (G or T)
    'M': 11, # Amino (A or C)
    
    'B': 12, # Not A (C, G, or T)
    'D': 13, # Not C (A, G, or T)
    'H': 14, # Not G (A, C, or T)
    'V': 15, # Not T (A, C, or G)
    
    'N': 16  # Any base (A, C, G, or T)
}


    # Convert each DNA character to a number
    try:
        numeric_sequence = [DNA_MAPPING[base] for base in dna_sequence]
    except KeyError:
        raise ValueError("Invalid DNA sequence. Only 'A', 'C', 'G', and 'T' are allowed.")

    # Convert to NumPy array and reshape to match model input
    input_data = np.array(numeric_sequence).reshape(1, -1)

    return input_data


def predict_all_attributes(dna_sequence):
    model, scaler, encoder = load_model()

    # Preprocess the input DNA sequence
    input_data = preprocess_input_data(dna_sequence)

    # Scale the input data (ensure correct shape)
    input_data_scaled = scaler.transform(input_data)

    # Make predictions
    prediction = model.predict(input_data_scaled)

    # Map predictions to actual attribute names
    predicted_attributes = {
        "Age": prediction[0][0],
        "Ethnicity": prediction[0][1],
        "Skin_Color": prediction[0][2],
        "Sickness": prediction[0][3],
        "Weight": prediction[0][4],
        "Height": prediction[0][5],
        "Eye_Color": prediction[0][6],
        "Hair_Color": prediction[0][7],
        "Sleep_Pattern": prediction[0][8],
        "Body_Odor": prediction[0][9],
        "Alcohol_Consumption": prediction[0][10],
        "Depression_Level": prediction[0][11],
        "IQ_Level": prediction[0][12],
        "Handedness": prediction[0][13],
        "Reaction_Time": prediction[0][14],
        "Sugar_Level": prediction[0][15],
        "Diabetic_Level": prediction[0][16],
        "Heart_Disease_Rate": prediction[0][17],
        "Violent_Behavior_Level": prediction[0][18],
        "ASPD_Psychopathy_Level": prediction[0][19],
        "Nose_Shape": prediction[0][20],
        "Nose_Size": prediction[0][21],
        "Face_Shape": prediction[0][22],
        "Ear_Shape": prediction[0][23],
    }

    return predicted_attributes
