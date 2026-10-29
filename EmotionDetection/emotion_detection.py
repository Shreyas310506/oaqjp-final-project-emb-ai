"""Emotion detection using the Watson NLP library."""
import json
import requests

URL = ("https://sn-watson-emotion.labs.skills.network/v1/"
       "watson.runtime.nlp.v1/NlpService/EmotionPredict")
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the given text."""
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=30)

    if response.status_code == 400:
        return {"anger": None, "disgust": None, "fear": None,
                "joy": None, "sadness": None, "dominant_emotion": None}

    emotions = json.loads(response.text)["emotionPredictions"][0]["emotion"]
    result = {k: emotions[k] for k in ("anger", "disgust", "fear", "joy", "sadness")}
    result["dominant_emotion"] = max(result, key=result.get)
    return result