from utils.model import predict_all_attributes

# Function to handle prediction request
def handle_predict_request(dna_sequence):
    try:
        # Get the predictions for all attributes
        predicted_attributes = predict_all_attributes(dna_sequence)
        return {
            "status": "success",
            "predicted_attributes": predicted_attributes
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
