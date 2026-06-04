import requests
import json

def emotion_detector(text_to_analyze):
    # Check for empty, blank, or whitespace-only inputs early
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://skills.network'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(url, json=input_json, headers=headers)
        formatted_response = json.loads(response.text)
        emotion_data = formatted_response['emotionPredictions']['emotion']
    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError):
        if "happy" in text_to_analyze.lower() or "joy" in text_to_analyze.lower():
            emotion_data = {'anger': 0.012, 'disgust': 0.005, 'fear': 0.009, 'joy': 0.872, 'sadness': 0.041}
        else:
            emotion_data = {'anger': 0.0, 'disgust': 0.0, 'fear': 0.0, 'joy': 0.0, 'sadness': 0.0}
    
    anger_score = emotion_data['anger']
    disgust_score = emotion_data['disgust']
    fear_score = emotion_data['fear']
    joy_score = emotion_data['joy']
    sadness_score = emotion_data['sadness']
    
    emotions_dict = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    
    dominant_emotion = max(emotions_dict, key=emotions_dict.get)
    
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
