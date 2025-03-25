import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Define DNA to numerical mapping
DNA_MAPPING = {
    'A': 1, 'C': 2, 'G': 3, 'T': 4, 'U': 5,
    'R': 6, 'Y': 7, 'S': 8, 'W': 9, 'K': 10, 'M': 11,
    'B': 12, 'D': 13, 'H': 14, 'V': 15, 'N': 16
}

MAX_DNA_LENGTH = 100 

# Function to convert DNA sequence to numerical values
def encode_dna_sequence(sequence):
    numeric_sequence = [DNA_MAPPING.get(base, 0) for base in sequence]
    
    # Ensure fixed-length input (pad or truncate)
    if len(numeric_sequence) > MAX_DNA_LENGTH:
        numeric_sequence = numeric_sequence[:MAX_DNA_LENGTH]
    else:
        numeric_sequence += [0] * (MAX_DNA_LENGTH - len(numeric_sequence))

    return numeric_sequence  

def train_and_save_model():
    # Load dataset
    df = pd.read_csv('../data/dna_dataset.csv')

    # Drop rows with missing values
    df = df.dropna()

    # Convert DNA sequences to numerical features
    df['DNA_Encoded'] = df['DNA_Sequence'].apply(encode_dna_sequence)

    # Define categorical columns to encode
    categorical_columns = [
        "Gender", "Ethnicity", "Skin_Color", "Sickness", "Eye_Color", "Hair_Color",
        "Sleep_Pattern", "Body_Odor", "Alcohol_Consumption", "Depression_Level",
        "Handedness", "Reaction_Time", "Sugar_Level", "Diabetic_Level",
        "Heart_Disease_Rate", "Violent_Behavior_Level", "ASPD_Psychopathy_Level",
        "Nose_Shape", "Nose_Size", "Face_Shape", "Ear_Shape"
    ]

    # Encode categorical columns
    label_encoders = {}
    for col in categorical_columns:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        label_encoders[col] = encoder

    # Define features (X) and targets (y)
    X = np.stack(df['DNA_Encoded'].values)  # Use processed DNA sequences
    y = df[categorical_columns].values  # Multi-label classification

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Save model, scaler, and encoders
    joblib.dump(rf_model, '../models/rf_model.pkl')
    joblib.dump(scaler, '../models/scaler.pkl')
    joblib.dump(label_encoders, '../models/label_encoders.pkl')

if __name__ == "__main__":
    train_and_save_model()
    print("✅ Model trained and saved!")
