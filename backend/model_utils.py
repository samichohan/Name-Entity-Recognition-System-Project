import spacy
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

ENTITY_COLORS = {
    "PERSON": "#4CAF50",
    "ORG":    "#2196F3",
    "GPE":    "#FF9800",
    "LOC":    "#FF9800",
    "DATE":   "#9C27B0",
    "MONEY":  "#F44336",
    "TIME":   "#00BCD4",
}

ENTITY_NAMES = {
    "PERSON": "Person",
    "ORG":    "Organization",
    "GPE":    "Location",
    "LOC":    "Location",
    "DATE":   "Date",
    "MONEY":  "Money",
    "TIME":   "Time",
}

def load_model_and_assets():
    print("🔄 spaCy model load ho raha hai...")
    nlp = spacy.load("en_core_web_sm")
    print("✅ Model loaded!")
    return nlp, None, None, None

def predict_ner(text: str, model, word2idx, idx2label, config):
    doc = model(text)
    
    words = text.split()
    results = []
    
    # Har word ke liye entity check karo
    for word in words:
        entity = "O"
        color = "#9E9E9E"
        
        for ent in doc.ents:
            ent_words = ent.text.split()
            if word in ent_words:
                entity = ent.label_
                color = ENTITY_COLORS.get(ent.label_, "#9E9E9E")
                break
        
        results.append({
            "word": word,
            "entity": entity,
            "color": color
        })
    
    return results

def get_entity_summary(predictions: list):
    summary = {name: [] for name in set(ENTITY_NAMES.values())}
    
    current_entity = None
    current_words = []
    
    for item in predictions:
        label = item["entity"]
        word = item["word"]
        
        if label != "O":
            entity_name = ENTITY_NAMES.get(label, label)
            if current_entity == entity_name:
                current_words.append(word)
            else:
                if current_entity and current_words:
                    if current_entity in summary:
                        summary[current_entity].append(" ".join(current_words))
                current_entity = entity_name
                current_words = [word]
        else:
            if current_entity and current_words:
                if current_entity in summary:
                    summary[current_entity].append(" ".join(current_words))
            current_entity = None
            current_words = []
    
    if current_entity and current_words:
        if current_entity in summary:
            summary[current_entity].append(" ".join(current_words))
    
    return summary