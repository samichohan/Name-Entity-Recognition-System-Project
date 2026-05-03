import streamlit as st
import re
 
st.set_page_config(page_title="NER System", page_icon="🏷️", layout="wide")
 
# ── Simple Rule-Based NER (No external ML library needed) ──
# Famous persons, organizations, locations database
 
PERSONS = [
    "Elon Musk", "Barack Obama", "Imran Khan", "Angela Merkel",
    "Larry Page", "Sergey Brin", "Bill Gates", "Sundar Pichai",
    "Jeff Bezos", "Mark Zuckerberg", "Steve Jobs", "Tim Cook",
    "Narendra Modi", "Vladimir Putin", "Joe Biden", "Donald Trump",
    "Malala Yousafzai", "Nawaz Sharif", "Asif Ali Zardari"
]
 
ORGANIZATIONS = [
    "Google", "Tesla", "SpaceX", "Microsoft", "Apple", "Amazon",
    "Facebook", "Meta", "Twitter", "Netflix", "NASA", "UN",
    "United Nations", "WHO", "World Health Organization", "NATO",
    "PTCL", "Jazz", "Telenor", "Ufone", "HBL", "MCB",
    "OpenAI", "Anthropic", "IBM", "Intel", "Samsung", "Sony",
    "Stanford University", "MIT", "Oxford University", "Harvard University",
    "PTI", "PML-N", "PPP", "Army", "Pakistan Army"
]
 
LOCATIONS = [
    "Pakistan", "Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta",
    "United States", "America", "USA", "California", "New York", "Washington",
    "United Kingdom", "London", "Paris", "Berlin", "Germany", "France",
    "China", "Beijing", "India", "New Delhi", "Russia", "Moscow",
    "Dubai", "UAE", "Saudi Arabia", "Turkey", "Iran", "Afghanistan",
    "Europe", "Asia", "Africa", "Middle East", "Silicon Valley",
    "Stanford", "Harvard", "Oxford"
]
 
ENTITY_COLORS = {
    "PERSON": "#4CAF50",
    "ORG":    "#2196F3",
    "LOC":    "#FF9800",
}
 
ENTITY_NAMES = {
    "PERSON": "Person 👤",
    "ORG":    "Organization 🏢",
    "LOC":    "Location 📍",
}
 
st.markdown("""
<style>
.main-title{font-size:2.5rem;font-weight:800;text-align:center;padding:1rem 0;color:#1a1a2e;}
.subtitle{text-align:center;color:#666;font-size:1.1rem;margin-bottom:2rem;}
</style>
""", unsafe_allow_html=True)
 
 
def analyze_text(text):
    results = []
    words = text.split()
    tagged = {}  # word index → entity type
 
    # Multi-word entities pehle check karo
    for entity_list, label in [(PERSONS, "PERSON"), (ORGANIZATIONS, "ORG"), (LOCATIONS, "LOC")]:
        for entity in entity_list:
            entity_words = entity.split()
            for i in range(len(words)):
                match = True
                for j, ew in enumerate(entity_words):
                    if i + j >= len(words):
                        match = False
                        break
                    if words[i + j].strip(".,!?;:").lower() != ew.lower():
                        match = False
                        break
                if match:
                    for j in range(len(entity_words)):
                        tagged[i + j] = label
 
    for i, word in enumerate(words):
        entity = tagged.get(i, "O")
        color = ENTITY_COLORS.get(entity, "#9E9E9E")
        results.append({"word": word, "entity": entity, "color": color})
 
    return results
 
 
def render_highlighted(results):
    html_parts = []
    for item in results:
        word = item["word"]
        entity = item["entity"]
        color = item["color"]
        if entity == "O":
            html_parts.append(f'<span style="margin:3px;font-size:1rem;">{word}</span>')
        else:
            label = ENTITY_NAMES.get(entity, entity)
            html_parts.append(
                f'<span style="background:{color};color:white;padding:3px 8px;'
                f'border-radius:5px;margin:3px;font-weight:bold;font-size:1rem;'
                f'display:inline-block;">'
                f'{word} <sup style="font-size:0.6rem;">{entity}</sup></span>'
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
        "Sundar Pichai represented Google at a conference in London."
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
        results = analyze_text(user_text)
        total = sum(1 for r in results if r["entity"] != "O")
 
        if total > 0:
            st.success(f"✅ {total} entity words mili!")
        else:
            st.info("ℹ️ Koi entity nahi mili. Famous names try karo!")
 
        st.markdown("**Highlighted Text:**")
        highlighted = render_highlighted(results)
        st.markdown(
            f'<div style="background:#f8f9fa;padding:15px;border-radius:10px;'
            f'line-height:2.8;">{highlighted}</div>',
            unsafe_allow_html=True
        )
 
        # Summary
        grouped = {}
        for r in results:
            if r["entity"] != "O":
                label = ENTITY_NAMES.get(r["entity"], r["entity"])
                color = r["color"]
                if label not in grouped:
                    grouped[label] = {"items": [], "color": color}
                grouped[label]["items"].append(r["word"])
 
        if grouped:
            st.markdown("**Entity Summary:**")
            for label, data in grouped.items():
                color = data["color"]
                items_html = "".join([
                    f'<code style="background:{color}20;border:1px solid {color};'
                    f'padding:2px 8px;border-radius:4px;margin:2px;'
                    f'display:inline-block;">{item}</code>'
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
            '<div>Left side mein text likho<br>aur button dabao</div>'
            '</div>',
            unsafe_allow_html=True
        )
 
# ── Legend ──
st.divider()
st.subheader("📚 Entity Types")
 
cols = st.columns(3)
legend = [
    ("👤 PERSON", "#4CAF50", "Imran Khan, Elon Musk, Barack Obama"),
    ("🏢 ORG",    "#2196F3", "Google, Tesla, United Nations, PTCL"),
    ("📍 LOC",    "#FF9800", "Pakistan, Karachi, California, London"),
]
for i, (name, color, example) in enumerate(legend):
    with cols[i]:
        st.markdown(
            f'<div style="background:{color}15;border:2px solid {color};'
            f'border-radius:8px;padding:15px;text-align:center;">'
            f'<div style="color:{color};font-weight:bold;font-size:1.1rem;">{name}</div>'
            f'<div style="color:#888;font-size:0.85rem;margin-top:5px;">{example}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
 
st.divider()
st.markdown(
    '<div style="text-align:center;color:#aaa;font-size:0.85rem;">'
    'NER System | Rule-Based + Deep Learning | Streamlit'
    '</div>',
    unsafe_allow_html=True
)
 
 
