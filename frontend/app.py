import streamlit as st
import spacy
 
st.set_page_config(page_title="NER System", page_icon="🏷️", layout="wide")
 
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")
 
nlp = load_model()
 
ENTITY_COLORS = {
    "PERSON": "#4CAF50",
    "ORG":    "#2196F3",
    "GPE":    "#FF9800",
    "LOC":    "#FF9800",
    "DATE":   "#9C27B0",
    "MONEY":  "#F44336",
    "TIME":   "#00BCD4",
    "NORP":   "#795548",
    "FAC":    "#607D8B",
    "PRODUCT":"#E91E63",
}
 
ENTITY_NAMES = {
    "PERSON": "Person 👤",
    "ORG":    "Organization 🏢",
    "GPE":    "Location 📍",
    "LOC":    "Location 📍",
    "DATE":   "Date 📅",
    "MONEY":  "Money 💰",
    "TIME":   "Time ⏰",
    "NORP":   "Nationality 🌍",
    "FAC":    "Facility 🏛️",
    "PRODUCT":"Product 📦",
}
 
st.markdown("""
<style>
    .main-title { font-size:2.5rem; font-weight:800; text-align:center; padding:1rem 0; color:#1a1a2e; }
    .subtitle   { text-align:center; color:#666; font-size:1.1rem; margin-bottom:2rem; }
</style>
""", unsafe_allow_html=True)
 
def analyze_text(text):
    doc = nlp(text)
    words = text.split()
    results = []
    for word in words:
        entity = "O"
        color = "#9E9E9E"
        for ent in doc.ents:
            if word in ent.text.split():
                entity = ent.label_
                color = ENTITY_COLORS.get(ent.label_, "#9E9E9E")
                break
        results.append({"word": word, "entity": entity, "color": color})
    return results, doc.ents
 
def render_highlighted_text(results):
    html_parts = []
    for item in results:
        word = item["word"]
        entity = item["entity"]
        color = item["color"]
        if entity == "O":
            html_parts.append(f'<span style="margin:3px;font-size:1rem;">{word}</span>')
        else:
            html_parts.append(
                f'<span style="background:{color};color:white;padding:3px 8px;'
                f'border-radius:5px;margin:3px;font-weight:bold;font-size:1rem;display:inline-block;">'
                f'{word} <sup style="font-size:0.65rem;">{entity}</sup></span>'
            )
    return " ".join(html_parts)
 
# ── UI ──
st.markdown('<div class="main-title">🏷️ Named Entity Recognition System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Text mein se automatically Person, Organization, Location dhoondta hai</div>', unsafe_allow_html=True)
st.divider()
 
left_col, right_col = st.columns([1, 1], gap="large")
 
with left_col:
    st.subheader("📝 Input")
    st.caption("Quick Examples:")
 
    examples = [
        "Elon Musk founded Tesla and SpaceX in California.",
        "Barack Obama was the President of the United States.",
        "Imran Khan visited Karachi and met UN officials.",
        "Google was founded by Larry Page and Sergey Brin at Stanford University."
    ]
 
    col1, col2 = st.columns(2)
    selected = None
    for i, ex in enumerate(examples):
        with (col1 if i % 2 == 0 else col2):
            if st.button(f"Example {i+1}", key=f"ex{i}", use_container_width=True):
                selected = ex
 
    user_text = st.text_area(
        "Apna text yahan likho:",
        value=selected if selected else "",
        height=150,
        placeholder="Koi bhi sentence likho...",
        max_chars=1000
    )
    st.caption(f"Characters: {len(user_text)}/1000")
 
    analyze_btn = st.button(
        "🔍 Entities Dhoondo",
        type="primary",
        use_container_width=True,
        disabled=not user_text.strip()
    )
 
with right_col:
    st.subheader("🎯 Results")
 
    if analyze_btn and user_text.strip():
        with st.spinner("🧠 Analyzing..."):
            results, ents = analyze_text(user_text)
 
        total = len(ents)
        if total > 0:
            st.success(f"✅ {total} entities mili!")
        else:
            st.info("ℹ️ Koi entity nahi mili.")
 
        st.markdown("**Highlighted Text:**")
        highlighted = render_highlighted_text(results)
        st.markdown(
            f'<div style="background:#f8f9fa;padding:15px;border-radius:10px;line-height:2.8;">{highlighted}</div>',
            unsafe_allow_html=True
        )
 
        if ents:
            st.markdown("**Entity Summary:**")
            grouped = {}
            for ent in ents:
                label = ENTITY_NAMES.get(ent.label_, ent.label_)
                color = ENTITY_COLORS.get(ent.label_, "#333")
                if label not in grouped:
                    grouped[label] = {"items": [], "color": color}
                if ent.text not in grouped[label]["items"]:
                    grouped[label]["items"].append(ent.text)
 
            for label, data in grouped.items():
                color = data["color"]
                items_html = "".join([
                    f'<code style="background:{color}20;border:1px solid {color};'
                    f'padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;">{item}</code>'
                    for item in data["items"]
                ])
                st.markdown(
                    f'<div style="background:#f8f9fa;border-left:4px solid {color};'
                    f'padding:10px 15px;border-radius:5px;margin:8px 0;">'
                    f'<strong style="color:{color};">{label}</strong><br>{items_html}</div>',
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            '<div style="text-align:center;padding:60px;color:#aaa;">'
            '<div style="font-size:4rem;">🏷️</div>'
            '<div style="font-size:1.1rem;">Left side mein text likho<br>aur button dabao</div>'
            '</div>',
            unsafe_allow_html=True
        )
 
# ── Legend ──
st.divider()
st.subheader("📚 Entity Types")
 
legend_data = [
    ("👤 PERSON",  "#4CAF50", "Imran Khan, Elon Musk"),
    ("🏢 ORG",     "#2196F3", "Google, United Nations"),
    ("📍 LOCATION","#FF9800", "Pakistan, Karachi, Berlin"),
    ("📅 DATE",    "#9C27B0", "2024, January, yesterday"),
    ("💰 MONEY",   "#F44336", "$100, 500 rupees"),
    ("⏰ TIME",    "#00BCD4", "3pm, morning, tonight"),
    ("🌍 NORP",    "#795548", "Pakistani, American"),
    ("📦 PRODUCT", "#E91E63", "iPhone, Tesla Model S"),
]
 
cols = st.columns(4)
for i, (name, color, example) in enumerate(legend_data):
    with cols[i % 4]:
        st.markdown(
            f'<div style="background:{color}15;border:2px solid {color};'
            f'border-radius:8px;padding:10px;text-align:center;margin:5px 0;">'
            f'<div style="color:{color};font-weight:bold;">{name}</div>'
            f'<div style="color:#888;font-size:0.8rem;">{example}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
 
st.divider()
st.markdown(
    '<div style="text-align:center;color:#aaa;font-size:0.85rem;">'
    'NER System | spaCy en_core_web_sm | Streamlit'
    '</div>',
    unsafe_allow_html=True
)
 