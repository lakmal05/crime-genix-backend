# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# import joblib

# def train_and_save_model():
#     # Load dataset
#     df = pd.read_csv('data/dna_dataset.csv')

#     # Check for missing values
#     df = df.dropna()  # or use other strategies to fill missing values

#     # Categorical columns to encode
#     categorical_columns = [
#         "Gender", "Ethnicity", "Skin_Color", "Sickness", "Eye_Color", "Hair_Color",
#         "Sleep_Pattern", "Body_Odor", "Alcohol_Consumption", "Depression_Level",
#         "Handedness", "Reaction_Time", "Sugar_Level", "Diabetic_Level",
#         "Heart_Disease_Rate", "Violent_Behavior_Level", "ASPD_Psychopathy_Level",
#         "Nose_Shape", "Nose_Size", "Face_Shape", "Ear_Shape"
#     ]

#     # Encode categorical columns
#     encoder = LabelEncoder()
#     for col in categorical_columns:
#         df[col] = encoder.fit_transform(df[col])

#     # Define features (X) and target (y)
#     X = df.drop(columns=['DNA_Sequence'])  # Drop DNA sequence column if it's not the target
#     y = df['Gender']  # Example target, modify this for your needs

#     # Feature scaling (standardization)
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)

#     # Split the data into train and test sets
#     X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#     # Initialize and train the model
#     rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
#     rf_model.fit(X_train, y_train)

#     # Save the model, encoder, and scaler
#     joblib.dump(rf_model, 'models/rf_model.pkl')
#     joblib.dump(scaler, 'models/scaler.pkl')
#     joblib.dump(encoder, 'models/encoder.pkl')
