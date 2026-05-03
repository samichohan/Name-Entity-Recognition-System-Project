import streamlit as st
import requests
import json
 
# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
# FastAPI ka address
# Local development mein localhost:8000
# Production mein apna server URL
 
API_URL = "http://localhost:8000"
 
# Entity colors (FastAPI se same)
ENTITY_COLORS = {
    "B-PER": "#4CAF50", "I-PER": "#4CAF50",
    "B-ORG": "#2196F3", "I-ORG": "#2196F3",
    "B-LOC": "#FF9800", "I-LOC": "#FF9800",
    "B-MISC": "#9C27B0","I-MISC": "#9C27B0",
    "O": None
}
 
# ─────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────
# Streamlit mein pehle page config set karo
st.set_page_config(
    page_title="NER System",
    page_icon="🏷️",
    layout="wide"  # Wide layout — zyada space
)
 
# ─────────────────────────────────────────
# CUSTOM CSS (Styling)
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* Main heading style */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a2e;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* Entity highlight boxes */
    .entity-box {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        margin: 2px;
        font-weight: 600;
        color: white;
        font-size: 1rem;
    }
    
    /* Normal word style */
    .normal-word {
        display: inline-block;
        padding: 2px 4px;
        margin: 2px;
        font-size: 1rem;
        color: #333;
    }
    
    /* Entity label badge */
    .entity-label {
        font-size: 0.65rem;
        vertical-align: super;
        font-weight: 700;
        opacity: 0.9;
    }
    
    /* Summary card */
    .summary-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid;
    }
    
    /* Status indicator */
    .status-ok  { color: #4CAF50; font-weight: bold; }
    .status-err { color: #f44336; font-weight: bold; }
</style>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
 
def check_api_health():
    """
    FastAPI server chal raha hai ya nahi check karo.
    Returns: True agar server up hai
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200 and response.json().get("model_loaded", False)
    except:
        return False
 
 
def call_predict_api(text: str):
    """
    FastAPI ke /predict endpoint ko call karo.
    
    Ye function:
    1. Text ko JSON mein wrap karta hai
    2. POST request FastAPI ko bhejta hai
    3. Response return karta hai
    
    Example:
        Input:  "Elon Musk founded Tesla"
        Output: {"entities": [...], "summary": {...}, "total_entities_found": 2}
    """
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},  # JSON format mein bhejo
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error = response.json().get("detail", "Unknown error")
            return None, f"API Error: {error}"
            
    except requests.ConnectionError:
        return None, "❌ Backend se connect nahi ho pa raha! FastAPI server chalao."
    except requests.Timeout:
        return None, "⏳ Request timeout ho gayi. Dobara try karo."
    except Exception as e:
        return None, f"Error: {str(e)}"
 
 
def render_highlighted_text(entities: list):
    """
    Words ko colored HTML mein convert karo.
    
    Example:
        Input:  [{"word": "Elon", "entity": "B-PER", "color": "#4CAF50"}, ...]
        Output: HTML string with colored spans
    """
    html_parts = []
    
    for item in entities:
        word = item["word"]
        entity = item["entity"]
        color = item["color"]
        
        if entity == "O":
            # Normal word — koi color nahi
            html_parts.append(f'<span class="normal-word">{word}</span>')
        else:
            # Entity word — colored box
            # Entity type short form (B-PER → PER)
            short_label = entity[2:] if entity.startswith(("B-", "I-")) else entity
            html_parts.append(
                f'<span class="entity-box" style="background-color: {color};">'
                f'{word} <span class="entity-label">{short_label}</span>'
                f'</span>'
            )
    
    return " ".join(html_parts)
 
 
# ─────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────
 
# Title
st.markdown('<div class="main-title">🏷️ Named Entity Recognition System</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#666; font-size:1.1rem;'>"
    "Text mein se automatically Person, Organization, Location dhoondta hai"
    "</p>",
    unsafe_allow_html=True
)
 
st.divider()
 
# ─── Server Status ───
col_status, col_empty = st.columns([1, 3])
with col_status:
    if check_api_health():
        st.markdown("🟢 <span class='status-ok'>Backend Connected</span>", unsafe_allow_html=True)
    else:
        st.markdown("🔴 <span class='status-err'>Backend Disconnected</span>", unsafe_allow_html=True)
        st.warning("FastAPI server chalao: `uvicorn main:app --reload`")
 
 
# ─── Two Column Layout ───
left_col, right_col = st.columns([1, 1], gap="large")
 
with left_col:
    st.subheader("📝 Input")
    
    # Example sentences
    st.caption("Quick examples:")
    
    example_texts = [
        "Elon Musk founded Tesla in California in 2003.",
        "Imran Khan visited Karachi and met with PTI leaders.",
        "Google was founded by Larry Page and Sergey Brin at Stanford University.",
        "The United Nations headquarters is located in New York City."
    ]
    
    # Example buttons
    cols = st.columns(2)
    selected_example = None
    for i, example in enumerate(example_texts):
        with cols[i % 2]:
            if st.button(f"Example {i+1}", key=f"ex_{i}", use_container_width=True):
                selected_example = example
    
    # Text input area
    default_text = selected_example if selected_example else ""
    user_text = st.text_area(
        "Apna text yahan likho:",
        value=default_text,
        height=150,
        placeholder="Koi bhi sentence likho jisme names, places, organizations hon...",
        max_chars=1000
    )
    
    # Character count
    st.caption(f"Characters: {len(user_text)}/1000")
    
    # Analyze button
    analyze_btn = st.button(
        "🔍 Entities Dhoondo",
        type="primary",
        use_container_width=True,
        disabled=not user_text.strip()
    )
 
 
# ─── Results Column ───
with right_col:
    st.subheader("🎯 Results")
    
    if analyze_btn and user_text.strip():
        
        with st.spinner("🧠 Model analyze kar raha hai..."):
            result, error = call_predict_api(user_text)
        
        if error:
            st.error(error)
        
        elif result:
            entities = result["entities"]
            summary = result["summary"]
            total = result["total_entities_found"]
            
            # Total entities found
            if total > 0:
                st.success(f"✅ {total} entities mili!")
            else:
                st.info("ℹ️ Koi entity nahi mili. Aur kuch try karo.")
            
            # Highlighted text
            st.markdown("**Highlighted Text:**")
            highlighted_html = render_highlighted_text(entities)
            st.markdown(
                f'<div style="background:#f8f9fa; padding:15px; border-radius:8px; '
                f'line-height:2.2; font-size:1.05rem;">{highlighted_html}</div>',
                unsafe_allow_html=True
            )
            
            # Entity Summary
            st.markdown("**Entity Summary:**")
            
            color_map = {
                "Person 👤":       ("#4CAF50", "🟢"),
                "Organization 🏢": ("#2196F3", "🔵"),
                "Location 📍":    ("#FF9800", "🟠"),
                "Miscellaneous 🔖":("#9C27B0", "🟣"),
            }
            
            found_any = False
            for entity_type, items in summary.items():
                if items:
                    found_any = True
                    color, emoji = color_map.get(entity_type, ("#333", "⚪"))
                    st.markdown(
                        f'<div class="summary-card" style="border-color:{color};">'
                        f'<strong>{emoji} {entity_type}</strong><br>'
                        f'{", ".join(f"<code>{item}</code>" for item in items)}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            
            if not found_any:
                st.markdown("_Koi named entity nahi mili._")
            
            # Raw JSON (expandable)
            with st.expander("🔧 Raw API Response dekho (debugging ke liye)"):
                st.json(result)
    
    else:
        # Placeholder jab koi input nahi
        st.markdown(
            '<div style="text-align:center; padding:40px; color:#aaa;">'
            '<div style="font-size:3rem;">🏷️</div>'
            '<div>Left side mein text likho aur<br>"Entities Dhoondo" press karo</div>'
            '</div>',
            unsafe_allow_html=True
        )
 
 
# ─────────────────────────────────────────
# LEGEND / GUIDE
# ─────────────────────────────────────────
st.divider()
st.subheader("📚 Entity Types Guide")
 
legend_cols = st.columns(4)
legend_data = [
    ("👤 PERSON",       "#4CAF50", "Insaan ka naam", "Elon Musk, Imran Khan"),
    ("🏢 ORGANIZATION", "#2196F3", "Company, team, govt", "Google, UN, Pakistan Army"),
    ("📍 LOCATION",     "#FF9800", "Jagah, city, country", "Karachi, Pakistan, River Indus"),
    ("🔖 MISC",         "#9C27B0", "Languages, nationalities", "Pakistani, English, European"),
]
 
for col, (name, color, desc, examples) in zip(legend_cols, legend_data):
    with col:
        st.markdown(
            f'<div style="background:{color}20; border:2px solid {color}; '
            f'border-radius:8px; padding:12px; text-align:center;">'
            f'<div style="color:{color}; font-weight:bold; font-size:1rem;">{name}</div>'
            f'<div style="color:#555; font-size:0.85rem; margin:5px 0;">{desc}</div>'
            f'<div style="color:#888; font-size:0.75rem;"><em>{examples}</em></div>'
            f'</div>',
            unsafe_allow_html=True
        )
 
# Footer
st.divider()
st.markdown(
    '<div style="text-align:center; color:#aaa; font-size:0.85rem;">'
    'NER System | Bidirectional LSTM | CoNLL-2003 Dataset | FastAPI + Streamlit'
    '</div>',
    unsafe_allow_html=True
)