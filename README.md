# Name-Entity-Recognition-System-Project
A complete end-to-end Named Entity Recognition system built with deep learning (Bidirectional LSTM), deployed via FastAPI backend and Streamlit frontend.


🔗 Live Links
ResourceLink🚀 Live App https://name-entity-recognition-system-project-1.streamlit.app
GitHub Repository https://github.com/samichohan/Name-Entity-Recognition-System-Project

📌 What is NER?
Named Entity Recognition (NER) is a Natural Language Processing (NLP) task that automatically identifies and classifies named entities in text into predefined categories such as:

👤 Person — Names of people (e.g., Elon Musk, Imran Khan)
🏢 Organization — Companies, institutions (e.g., Google, United Nations)
📍 Location — Cities, countries, places (e.g., Karachi, California)
📅 Date/Time — Temporal expressions (e.g., 2024, Monday)
💰 Money — Monetary values (e.g., $100, 500 rupees)


🎯 Project Overview
This project implements a complete NER pipeline:
User Input Text
      ↓
Streamlit Frontend (UI)
      ↓
FastAPI Backend (API Server)
      ↓
Bidirectional LSTM Model / spaCy
      ↓
Named Entities Extracted
      ↓
Results Displayed with Color Highlighting

🧠 Model Architecture
The deep learning model uses a Bidirectional LSTM architecture:
Input (Word Indices)
        ↓
Embedding Layer (64 dimensions)
        ↓
Bidirectional LSTM (128 units) ← reads sentence forward & backward
        ↓
Dropout (0.3) ← prevents overfitting
        ↓
Bidirectional LSTM (64 units)
        ↓
Dropout (0.3)
        ↓
TimeDistributed Dense (softmax) ← prediction per word
        ↓
Output (Entity Labels)
Why Bidirectional LSTM?

Normal LSTM reads text left to right only
Bidirectional LSTM reads both directions — better context understanding
Example: To identify "Musk" as a PERSON, the model uses "Elon" (before) AND the words after


📊 Dataset
PropertyDetailsNameCoNLL-2003SourceKaggle — CoNLL-2003 English VersionTrain Sentences~14,041Validation Sentences~3,250Test Sentences~3,453Entity TypesPER, ORG, LOC, MISC
Label Format (BIO Tagging)
B- = Beginning of entity
I- = Inside/continuation of entity  
O  = Outside (no entity)

Example:
"Imran  Khan   visited  Karachi"
 B-PER  I-PER  O        B-LOC

🏗️ Project Structure
Name-Entity-Recognition-System-Project/
│
├── 📓 notebooks/
│   └── train_model.py          # Google Colab training notebook
│
├── ⚙️ backend/
│   ├── main.py                 # FastAPI server & API endpoints
│   └── model_utils.py          # Model loading & prediction functions
│
├── 🎨 frontend/
│   └── app.py                  # Streamlit UI application
│
├── 🧠 model/
│   ├── ner_model.keras          # Trained LSTM model
│   ├── word2idx.pkl             # Word to index mapping
│   ├── idx2label.pkl            # Index to label mapping
│   └── config.json              # Model configuration
│
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation

🚀 How to Run Locally
Prerequisites
bashPython 3.12
Anaconda (recommended)
Step 1 — Create Environment
bashconda create -n ner_env python=3.12 -y
conda activate ner_env
Step 2 — Install Dependencies
bashpip install -r requirements.txt
Step 3 — Download spaCy Model
bashpython -m spacy download en_core_web_sm
Step 4 — Run Backend (FastAPI)
bashcd backend
uvicorn main:app --reload --port 8000
API docs available at: http://localhost:8000/docs
Step 5 — Run Frontend (Streamlit)
bashcd frontend
streamlit run app.py
App available at: http://localhost:8501

🔌 API Endpoints
MethodEndpointDescriptionGET/API status checkGET/healthHealth check & model statusPOST/predictNER predictionGET/labelsAvailable entity labels
Example API Request
jsonPOST /predict
{
  "text": "Elon Musk founded Tesla in California"
}
Example API Response
json{
  "entities": [
    {"word": "Elon",       "entity": "PERSON", "color": "#4CAF50"},
    {"word": "Musk",       "entity": "PERSON", "color": "#4CAF50"},
    {"word": "founded",    "entity": "O",       "color": "#9E9E9E"},
    {"word": "Tesla",      "entity": "ORG",     "color": "#2196F3"},
    {"word": "in",         "entity": "O",       "color": "#9E9E9E"},
    {"word": "California", "entity": "GPE",     "color": "#FF9800"}
  ],
  "summary": {
    "Person": ["Elon Musk"],
    "Organization": ["Tesla"],
    "Location": ["California"]
  },
  "total_entities_found": 3
}

🎨 Entity Color Coding
EntityColorExample👤 PERSON🟢 Green #4CAF50Elon Musk, Imran Khan🏢 ORG🔵 Blue #2196F3Google, United Nations📍 LOCATION🟠 Orange #FF9800Pakistan, California📅 DATE🟣 Purple #9C27B02024, January💰 MONEY🔴 Red #F44336$100, 500 rupees⏰ TIME🩵 Cyan #00BCD43pm, morning🌍 NORP🟤 Brown #795548Pakistani, American

🛠️ Tech Stack
ComponentTechnologyDeep Learning ModelTensorFlow / Keras — Bidirectional LSTMNLP LibraryspaCy (en_core_web_sm)Backend APIFastAPI + UvicornFrontend UIStreamlitDatasetCoNLL-2003 (Kaggle)Training EnvironmentGoogle Colab (GPU)DeploymentStreamlit CloudVersion ControlGitHub

📈 Model Training Details
ParameterValueEmbedding Dimension64LSTM Units (Layer 1)128 (Bidirectional)LSTM Units (Layer 2)64 (Bidirectional)Dropout Rate0.3Max Sequence Length50Batch Size32Epochs15 (Early Stopping)OptimizerAdamLoss FunctionCategorical Crossentropy

👤 Author
Sami Chohan

GitHub: @samichohan
Project: Name-Entity-Recognition-System-Project


📝 Assignment Info
FieldDetailsAssignmentAssignment 7 — Named Entity Recognition SystemCourseArtificial Intelligence / Machine LearningModelBidirectional LSTM + spaCyDatasetCoNLL-2003DeploymentStreamlit Cloud

Built with ❤️ using Python, TensorFlow, FastAPI, and Streamlit
