from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from scipy import stats
import random

app = Flask(__name__)

# load pre-trained model here in real app
# for this prototype, a simple statistical mock analysis is used

def mock_dyslexia_analysis(gaze_data):
    """
    A mock analysis function that simulates the ViT model.
    In reality, this would be a complex deep learning model.
    For now, we just calculate some simple statistics and invent a score.
    """
    if not gaze_data:
        return 0.5  # default uncertainty

    x_coords = [point['x'] for point in gaze_data]
    y_coords = [point['y'] for point in gaze_data]

    # Calculate basic metrics mentioned in the paper
    total_distance = 0
    for i in range(1, len(x_coords)):
        dx = x_coords[i] - x_coords[i-1]
        dy = y_coords[i] - y_coords[i-1]
        total_distance += np.sqrt(dx**2 + dy**2)

    avg_distance = total_distance / len(x_coords) if len(x_coords) > 1 else 0

    # Calculate "regressions" - movements to the left (for a left-to-right language)
    regressions = 0
    for i in range(1, len(x_coords)):
        if x_coords[i] < x_coords[i-1]:
            regressions += 1

    regression_ratio = regressions / len(x_coords) if len(x_coords) > 0 else 0

    # Mock "AI" logic: More regressions and erratic movement (high avg distance) -> higher risk score
    # This is a gross oversimplification for the prototype.
    risk_score = (regression_ratio * 0.6) + (min(avg_distance / 100, 1) * 0.4)

    # Add some randomness to make it feel more real, then clamp between 0 and 1.
    risk_score += random.uniform(-0.1, 0.1)
    return max(0.0, min(1.0, risk_score))

def get_recommendation(risk_score):
    """A mock recommender system based on the risk score."""
    if risk_score < 0.3:
        return "Low risk detected. Recommended: Advanced phonics and fluency games."
    elif risk_score < 0.7:
        return "Medium risk detected. Recommended: Focused phonological awareness and decoding exercises."
    else:
        return "High risk detected. Recommended: Intensive, multi-sensory literacy intervention. Consider professional assessment."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        gaze_data = data.get('gazeData', [])
        
        # Mock AI analysis
        risk_score = mock_dyslexia_analysis(gaze_data)
        
        # Get a mock personalized recommendation
        recommendation = get_recommendation(risk_score)
        
        response = {
            'success': True,
            'risk_score': round(risk_score, 2),
            'recommendation': recommendation
        }
        
    except Exception as e:
        response = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
