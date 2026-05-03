from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List,Dict,Any
import uvicorn

from model_utils import (
    load_model_and_assets,
    predict_ner,
    get_entity_summary
)

app = FastAPI(
    title="NER System API",
    description="Named Entity Recognition using Bidirectional LSTM",
    version="1.0.0"
)

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

model = None
word2idx = None
idx2label = None
config = None


@app.on_event("startup")
async def startup_event():
    global model, word2idx, idx2label, config
    try:
        model, word2idx, idx2label, config = load_model_and_assets()
        print("Server Ready!")
    except Exception as e:
        print(f" Error: {e}")


class PredictRequest(BaseModel):

    text: str


class EntityResult(BaseModel):
    word: str
    entity: str
    color: str


class PredictResponse(BaseModel):
    entities: list[EntityResult]
    summary: Dict[str,List[str]]
    total_entities_found: int


@app.get("/")
def root():
    return {
        "message": "Ner System API is Running",
        "docs": "http://localhost:8000/docs"

    }    

@app.get("/health")
def health_check():
    return {
        'status': "Healthy" if model is not None else "Model not Loaded",
        "model_loaded": model is not None
    }


@app.post("/predict",response_model=PredictResponse)
def Predict(request: PredictRequest):
    
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model Load Nhi Huwa!"
            )
    
    text = request.text.strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text Khali Nhi Hona Chahiye!"
        )
    
    if len(text) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Text bohot lamba hai! 1000 sai kam hona chahiye"
        )
    
    predictions = predict_ner(text,model,word2idx,idx2label,config)

    summary = get_entity_summary(predictions)

    total = sum(
        1 for p in predictions
        if p['entity'].startswith("B-")
    )

    return PredictResponse(
        entities=predictions,
        summary=summary,
        total_entities_found=total
    )

@app.get("/labels")
def get_labels():
    return {
        "Labels": {
            "B-PER / I-PER": "Person ka naam (Elon Musk, Imran Khan)",
            "B-ORG / I-ORG": "Organization (Google, PTCL, UN)",
            "B-LOC / I-LOC": "Location (Pakistan, Karachi, River Indus)",
            "B-MISC / I-MISC": "Miscellaneous (languages, nationalities)",
            "O": "Koi entity nahi (normal words)"
        }
    }

if __name__=="__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )