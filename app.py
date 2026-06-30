import streamlit as st
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn as nn
import json, os, io, time

st.set_page_config(
    page_title="FasalGuard 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: #060d06 !important; color: #e8f0e8 !important; font-family: 'Inter', sans-serif; }
.stApp > header { display: none; }
[data-testid="stSidebar"] { display: none; }

.hero-section {
    background: linear-gradient(160deg, #060d06 0%, #0a1a0a 50%, #060d06 100%);
    border-bottom: 1px solid #1a3a1a;
    padding: 3.5rem 2rem 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -30%; left: -20%;
    width: 140%; height: 160%;
    background: radial-gradient(ellipse at 50% 40%, rgba(34,197,94,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    color: #4ade80;
    padding: 7px 20px;
    border-radius: 30px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 800;
    color: #f0faf0;
    line-height: 1.05;
    margin-bottom: 0.8rem;
    letter-spacing: -1px;
}
.hero-title span { color: #4ade80; }
.hero-subtitle {
    font-size: 1.05rem;
    color: #5a8f5a;
    max-width: 520px;
    margin: 0 auto 0.5rem;
    line-height: 1.7;
    font-weight: 400;
}
.hero-urdu {
    font-size: 1.1rem;
    color: #4ade80;
    opacity: 0.7;
    margin-bottom: 2.5rem;
    font-weight: 300;
    letter-spacing: 0.3px;
}
.stats-row {
    display: flex;
    justify-content: center;
    gap: 0;
    margin-top: 2rem;
    flex-wrap: wrap;
    background: rgba(255,255,255,0.02);
    border: 1px solid #1a3a1a;
    border-radius: 14px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    overflow: hidden;
}
.stat-item {
    text-align: center;
    padding: 1rem 1.5rem;
    flex: 1;
    border-right: 1px solid #1a3a1a;
    min-width: 80px;
}
.stat-item:last-child { border-right: none; }
.stat-num { display: block; font-size: 1.4rem; font-weight: 800; color: #4ade80; line-height: 1; }
.stat-label { display: block; font-size: 0.62rem; color: #4a6f4a; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 5px; font-weight: 600; }

.main-container { max-width: 980px; margin: 0 auto; padding: 2.5rem 1.5rem; }
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: #4ade80;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.7rem;
    display: block;
}

.how-card {
    background: #0a150a;
    border: 1px solid #1a3a1a;
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
}
.how-step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 1.1rem;
}
.step-num {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: rgba(34,197,94,0.12);
    border: 1.5px solid rgba(34,197,94,0.35);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 800; color: #4ade80; flex-shrink: 0;
}
.step-en { font-size: 0.88rem; color: #c8e6c8; font-weight: 600; }
.step-ur { font-size: 0.76rem; color: #4a6f4a; margin-top: 3px; }
.photo-tips {
    margin-top: 1.2rem; padding: 1rem;
    background: rgba(34,197,94,0.04);
    border-radius: 10px;
    border: 1px solid #1a3a1a;
}
.tips-title { font-size: 0.7rem; color: #4ade80; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px; }
.tips-text { font-size: 0.76rem; color: #4a6f4a; line-height: 1.8; }

/* Result Card */
.result-card {
    background: #0a150a;
    border: 1px solid #1a3a1a;
    border-radius: 18px;
    overflow: hidden;
    margin-top: 1.8rem;
    box-shadow: 0 4px 40px rgba(0,0,0,0.4);
}
.result-header {
    background: linear-gradient(135deg, #0d1f0d, #111f11);
    padding: 1.6rem;
    border-bottom: 1px solid #1a3a1a;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.result-body { padding: 1.6rem; }

.severity-badge {
    padding: 5px 16px;
    border-radius: 30px;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    white-space: nowrap;
}
.sev-high { background: rgba(239,68,68,0.12); border: 1.5px solid rgba(239,68,68,0.35); color: #f87171; }
.sev-medium { background: rgba(245,158,11,0.12); border: 1.5px solid rgba(245,158,11,0.35); color: #fbbf24; }
.sev-low { background: rgba(34,197,94,0.12); border: 1.5px solid rgba(34,197,94,0.35); color: #4ade80; }
.sev-none { background: rgba(34,197,94,0.12); border: 1.5px solid rgba(34,197,94,0.35); color: #4ade80; }

.conf-bar-wrap { margin: 1.2rem 0; }
.conf-row { display: flex; justify-content: space-between; margin-bottom: 7px; }
.conf-label { font-size: 0.7rem; color: #4a6f4a; font-weight: 600; letter-spacing: 0.5px; }
.conf-val { font-size: 0.7rem; color: #4ade80; font-weight: 800; }
.conf-bg { background: #0f1f0f; border-radius: 8px; height: 8px; overflow: hidden; }
.conf-fill { height: 100%; background: linear-gradient(90deg, #15803d, #4ade80); border-radius: 8px; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin: 1.2rem 0; }
.info-block {
    background: #060d06;
    border: 1px solid #1a3a1a;
    border-radius: 12px;
    padding: 1rem;
}
.ib-label { font-size: 0.62rem; color: #4ade80; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin-bottom: 0.4rem; }
.ib-val { font-size: 0.92rem; color: #c8e6c8; font-weight: 500; line-height: 1.4; }

.divider { border: none; border-top: 1px solid #1a3a1a; margin: 1.3rem 0; }

.list-section h4 {
    font-size: 0.68rem;
    font-weight: 800;
    color: #4ade80;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.9rem;
}
.list-item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 0.6rem;
    padding: 0.7rem 0.9rem;
    background: #060d06;
    border-radius: 10px;
    border: 1px solid #1a3a1a;
    transition: border-color 0.2s;
}
.dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.dot-green { background: #4ade80; }
.dot-blue { background: #60a5fa; }
.dot-yellow { background: #fbbf24; }
.dot-red { background: #f87171; }
.list-text { font-size: 0.87rem; color: #8ab88a; line-height: 1.6; }

.urdu-block {
    background: linear-gradient(135deg, #060d06, #0a150a);
    border: 1px solid #2a4a2a;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    margin-top: 1.3rem;
    direction: rtl;
    text-align: right;
}
.urdu-title { font-size: 0.75rem; color: #4ade80; margin-bottom: 0.7rem; font-weight: 800; letter-spacing: 0.8px; }
.urdu-text { font-size: 0.97rem; color: #8ab88a; line-height: 2.1; }

.healthy-banner {
    background: linear-gradient(135deg, rgba(34,197,94,0.07), rgba(34,197,94,0.02));
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
    margin: 1.2rem 0;
}

/* Alert Box */
.alert-box {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.alert-icon { font-size: 1rem; flex-shrink: 0; margin-top: 2px; }
.alert-text { font-size: 0.83rem; color: #fca5a5; line-height: 1.5; }

.footer-section {
    text-align: center;
    padding: 3rem 1.5rem;
    border-top: 1px solid #1a3a1a;
    margin-top: 3rem;
}
.footer-text { font-size: 0.72rem; color: #2a4a2a; line-height: 2.2; }

[data-testid="stFileUploadDropzone"] {
    background: #060d06 !important;
    border: 1.5px dashed #2a4a2a !important;
    border-radius: 12px !important;
    color: #4a6f4a !important;
}
.stSelectbox > div > div {
    background: #0a150a !important;
    border: 1px solid #2a4a2a !important;
    border-radius: 10px !important;
    color: #c8e6c8 !important;
}
div[data-testid="stMarkdownContainer"] p { color: #8ab88a; }
.stButton > button {
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; }

@media (max-width: 640px) {
    .info-grid { grid-template-columns: 1fr; }
    .stats-row { max-width: 100%; }
    .stat-item { padding: 0.8rem 1rem; }
    .hero-section { padding: 2.5rem 1rem 2rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Disease Knowledge Base ────────────────────────────────────────────────────
DB = {
    "Apple___Apple_scab": {
        "en": "Apple Scab", "ur": "سیب کا کھرنڈ",
        "cause": "Fungal (Venturia inaequalis)", "cause_ur": "فنگس — بہار میں بارش کے ساتھ پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Olive-green to brown scab-like spots on leaves", "Velvety texture on infected spots", "Fruit develops hard, corky scabs reducing market value"],
        "treatments": ["Apply Captan or Myclobutanil fungicide at bud-break stage", "Spray every 10 days during wet spring weather", "Remove and destroy all infected fallen leaves immediately"],
        "prevention": ["Plant scab-resistant apple varieties", "Rake and burn fallen leaves every autumn", "Prune trees annually for good air circulation"],
        "ur_sum": "سیب میں کھرنڈ بیماری ہے جو فنگس کی وجہ سے ہوتی ہے۔ کیپٹان یا مائیکلوبٹانیل فنگسائیڈ اسپرے کریں اور گرے ہوئے پتے فوری تلف کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% cosmetic + yield loss"
    },
    "Apple___Black_rot": {
        "en": "Apple Black Rot", "ur": "سیب کی کالی سڑن",
        "cause": "Fungal (Botryosphaeria obtusa)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "High", "part": "Fruit, Leaves & Bark", "urgent": True,
        "symptoms": ["Purple spots on leaves expanding to brown with purple border", "Fruit turns black and shrivels completely", "Cankers form on branches — bark cracks and dies"],
        "treatments": ["Remove and destroy ALL mummified fruit immediately — do not leave on tree", "Apply Captan or Thiophanate-methyl fungicide", "Prune out all dead and cankered wood to healthy tissue"],
        "prevention": ["Remove all fruit mummies before spring bud break", "Avoid wounding bark during pruning operations", "Maintain tree vigor with balanced NPK fertilization"],
        "ur_sum": "سیب میں کالی سڑن ہے — فوری عمل ضروری ہے۔ تمام متاثرہ پھل فوری ہٹائیں اور فنگسائیڈ اسپرے کریں۔ مردہ شاخیں کاٹ کر جلا دیں۔",
        "urgency": "Immediate action required", "ur_urgency": "فوری توجہ درکار ہے",
        "safe": False, "econ": "Up to 100% fruit loss if untreated"
    },
    "Apple___Cedar_apple_rust": {
        "en": "Cedar Apple Rust", "ur": "سیب کا زنگ",
        "cause": "Fungal (Gymnosporangium juniperi-virginianae)", "cause_ur": "فنگس — صنوبر اور سیب درختوں کے درمیان پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Bright orange-yellow spots on upper leaf surface", "Tube-like structures (aecia) on leaf undersides", "Premature leaf drop weakening the tree"],
        "treatments": ["Apply Myclobutanil or Propiconazole at pink bud stage", "Spray every 7-10 days during spring infection period", "Remove nearby cedar/juniper trees if feasible"],
        "prevention": ["Plant rust-resistant apple varieties", "Apply protective fungicide before symptoms appear each spring", "Remove galls from nearby juniper trees in winter"],
        "ur_sum": "سیب میں زنگ بیماری ہے۔ بہار میں مائیکلوبٹانیل اسپرے کریں اور قریبی صنوبر کے درختوں پر توجہ دیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss in heavy seasons"
    },
    "Apple___healthy": {
        "en": "Healthy Apple Plant", "ur": "صحت مند سیب کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor regularly every 2 weeks throughout growing season", "Maintain balanced NPK fertilization", "Ensure proper drainage and irrigation"],
        "ur_sum": "آپ کا سیب کا پودا بالکل صحت مند ہے۔ کوئی بیماری نہیں ملی۔ اسی طرح دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Blueberry___healthy": {
        "en": "Healthy Blueberry Plant", "ur": "صحت مند بلوبیری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Maintain soil pH between 4.5-5.5 for optimal growth", "Regular monitoring for pests and disease", "Ensure adequate drainage"],
        "ur_sum": "آپ کی بلوبیری کا پودا صحت مند ہے۔ باقاعدہ دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "en": "Cherry Powdery Mildew", "ur": "چیری کی سفید پھپھوندی",
        "cause": "Fungal (Podosphaera clandestina)", "cause_ur": "فنگس — خشک گرم موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Young Shoots", "urgent": False,
        "symptoms": ["White powdery coating on upper and lower leaf surfaces", "Young leaves distorted and curling inward", "Premature leaf drop in severe infections"],
        "treatments": ["Apply Sulfur-based fungicide or Myclobutanil spray", "Use potassium bicarbonate as organic alternative", "Remove and destroy severely infected shoots"],
        "prevention": ["Plant powdery mildew-resistant cherry varieties", "Avoid excess nitrogen fertilizer which promotes soft growth", "Prune for maximum air circulation through canopy"],
        "ur_sum": "چیری میں سفید پھپھوندی ہے۔ سلفر فنگسائیڈ اسپرے کریں اور متاثرہ ٹہنیاں کاٹ کر تلف کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "10-20% yield loss if untreated"
    },
    "Cherry_(including_sour)___healthy": {
        "en": "Healthy Cherry Plant", "ur": "صحت مند چیری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring throughout season", "Annual pruning for airflow", "Balanced fertilization"],
        "ur_sum": "آپ کی چیری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "en": "Gray Leaf Spot", "ur": "مکئی کا سرمئی دھبہ",
        "cause": "Fungal (Cercospora zeae-maydis)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Rectangular tan-to-gray lesions running parallel between leaf veins", "Lesions have distinct parallel edges unlike other diseases", "Severe infection causes complete leaf death before harvest"],
        "treatments": ["Apply Azoxystrobin or Propiconazole fungicide at first sign", "Spray at silking stage for critical protection window", "Remove and till infected crop residue after harvest"],
        "prevention": ["Plant certified gray leaf spot-resistant hybrids", "Practice crop rotation — avoid continuous maize planting", "Improve field drainage to reduce humidity"],
        "ur_sum": "مکئی میں سرمئی دھبہ بیماری ہے۔ فنگسائیڈ اسپرے کریں اور اگلے سال فصل بدلیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "Up to 50% yield loss in severe cases"
    },
    "Corn_(maize)___Common_rust_": {
        "en": "Common Rust", "ur": "مکئی کا عام زنگ",
        "cause": "Fungal (Puccinia sorghi)", "cause_ur": "فنگس — ٹھنڈے اور نم موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Small brick-red to brown powdery pustules on both leaf surfaces", "Pustules turn dark brown to black near plant maturity", "Heavy infection causes premature leaf death"],
        "treatments": ["Apply Propiconazole or Azoxystrobin at first pustule appearance", "Spray at early tassel stage for maximum protection", "Repeat spray after 14 days if infection pressure is high"],
        "prevention": ["Plant rust-resistant maize hybrids — check seed company ratings", "Early planting before peak rust season (avoid July planting)", "Monitor fields weekly from emergence onwards"],
        "ur_sum": "مکئی میں زنگ لگا ہے۔ پروپیکونازول فنگسائیڈ اسپرے کریں اور اگلے سال مزاحم اقسام لگائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں اسپرے کریں",
        "safe": True, "econ": "10-30% yield loss if uncontrolled"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "en": "Northern Leaf Blight", "ur": "مکئی کا شمالی جھلساؤ",
        "cause": "Fungal (Setosphaeria turcica)", "cause_ur": "فنگس — مکئی کے پتوں کو تیزی سے متاثر کرتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Long cigar-shaped gray-green lesions 2.5–15 cm in length", "Lesions start on lower leaves and move upward", "Tan/brown color at maturity — green spores visible in humid conditions"],
        "treatments": ["Apply Azoxystrobin or Propiconazole at first sign of disease", "Critical spray timing is at silking stage for yield protection", "Remove and incorporate all crop residue after harvest"],
        "prevention": ["Plant resistant hybrids — consult local seed suppliers", "Crop rotation with wheat, legumes, or other non-host crops", "Avoid excess nitrogen which promotes lush susceptible growth"],
        "ur_sum": "مکئی میں شمالی جھلساؤ ہے۔ فنگسائیڈ اسپرے کریں اور اگلے سال مزاحم اقسام استعمال کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "Up to 50% yield loss in severe cases"
    },
    "Corn_(maize)___healthy": {
        "en": "Healthy Maize Plant", "ur": "صحت مند مکئی کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor fields weekly from emergence to harvest", "Balanced NPK fertilization based on soil test", "Proper plant spacing (75cm rows) for air circulation"],
        "ur_sum": "آپ کی مکئی کا پودا صحت مند ہے۔ کوئی بیماری نہیں ملی۔ اچھی دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Grape___Black_rot": {
        "en": "Grape Black Rot", "ur": "انگور کی کالی سڑن",
        "cause": "Fungal (Guignardia bidwellii)", "cause_ur": "فنگس — گرم اور بارشی موسم میں بہت تیزی سے پھیلتی ہے۔",
        "sev": "High", "part": "Leaves & Fruit", "urgent": True,
        "symptoms": ["Circular tan spots with dark brown border on leaves", "Infected berries turn black and shrivel into hard mummies", "Black pycnidia (fruiting bodies) visible as tiny dots in spots"],
        "treatments": ["Apply Myclobutanil or Mancozeb starting at bud break", "Spray every 10-14 days throughout growing season", "Remove and destroy ALL infected fruit and leaves — zero tolerance"],
        "prevention": ["Remove all mummified fruit from vines and ground before spring", "Prune for open canopy structure to maximize air and sunlight", "Use disease-resistant grape varieties where available"],
        "ur_sum": "انگور میں کالی سڑن ہے — پھل بہت تیزی سے ضائع ہو سکتا ہے۔ فوری فنگسائیڈ اسپرے کریں اور تمام متاثرہ پھل ہٹائیں۔",
        "urgency": "Immediate action required", "ur_urgency": "فوری توجہ درکار ہے",
        "safe": False, "econ": "50-100% fruit loss if not controlled early"
    },
    "Grape___Esca_(Black_Measles)": {
        "en": "Esca (Black Measles)", "ur": "انگور کی خسرہ بیماری",
        "cause": "Fungal complex (Phaeomoniella + Phaeoacremonium)", "cause_ur": "کئی فنگسز مل کر یہ بیماری پیدا کرتی ہیں — پرانی بیلوں میں زیادہ ہوتی ہے۔",
        "sev": "High", "part": "Whole Vine", "urgent": True,
        "symptoms": ["Tiger-stripe yellowing/browning between leaf veins (interveinal chlorosis)", "Fruit develops small dark measle-like spots", "Sudden apoplexy — complete vine collapse in hot weather"],
        "treatments": ["No complete cure available — remove severely infected vines immediately", "Protect all pruning wounds with fungicide paste (Trichoderma-based)", "Trunk injection treatments available in some countries — consult expert"],
        "prevention": ["Always apply wound protectant after pruning — within minutes of cutting", "Avoid pruning during wet weather to prevent spore infection", "Remove and burn all infected wood"],
        "ur_sum": "انگور میں خسرہ بیماری ہے — کوئی مکمل علاج نہیں۔ شدید متاثرہ بیلیں نکالیں اور کٹائی کے زخموں پر فنگسائیڈ لگائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "فوری اقدامات کریں",
        "safe": False, "econ": "Progressive vine death over several years"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "en": "Grape Leaf Blight", "ur": "انگور کا پتہ جھلساؤ",
        "cause": "Fungal (Pseudocercospora vitis)", "cause_ur": "فنگس — گرم اور نم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Irregular dark brown spots on older leaves", "Yellow halo surrounding dark brown lesions", "Premature defoliation weakens vine before harvest"],
        "treatments": ["Apply Mancozeb or Copper-based fungicide", "Remove and destroy all infected leaves from vine and ground", "Spray every 10-14 days in humid conditions"],
        "prevention": ["Proper vine training system for air circulation", "Drip irrigation preferred over overhead sprinklers", "Remove all crop debris after harvest season"],
        "ur_sum": "انگور کے پتوں میں جھلساؤ ہے۔ مینکوزیب فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss if severe"
    },
    "Grape___healthy": {
        "en": "Healthy Grape Vine", "ur": "صحت مند انگور کی بیل",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor weekly during growing season", "Annual winter pruning for canopy management", "Balanced fertilization and proper irrigation"],
        "ur_sum": "آپ کی انگور کی بیل صحت مند ہے۔ باقاعدہ دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "en": "Citrus Greening (HLB)", "ur": "مالٹے کی سبزی بیماری (HLB)",
        "cause": "Bacterial (Candidatus Liberibacter asiaticus)", "cause_ur": "بیکٹیریا — سیلا کیڑے (Psyllid) کے ذریعے پھیلتا ہے — کوئی علاج نہیں۔",
        "sev": "High", "part": "Whole Tree", "urgent": True,
        "symptoms": ["Asymmetric blotchy yellowing of leaves (different from nutrient deficiency)", "Fruit remains small, green and lopsided even at maturity", "Fruit is bitter and drops early — seeds abort inside fruit"],
        "treatments": ["NO CURE EXISTS — infected trees must be removed and destroyed", "Control Asian Citrus Psyllid (Diaphorina citri) with Imidacloprid spray", "Report immediately to local Agriculture Department (محکمہ زراعت)"],
        "prevention": ["Use only certified disease-free nursery trees — never buy from roadside", "Aggressive psyllid control program in all nearby orchards", "Inspect all new plants thoroughly before planting"],
        "ur_sum": "یہ انتہائی خطرناک بیماری ہے جس کا کوئی علاج نہیں ہے۔ متاثرہ درخت فوری کاٹ کر جلا دیں اور محکمہ زراعت کو فوری اطلاع دیں۔",
        "urgency": "Immediate — Remove and destroy tree", "ur_urgency": "فوری — درخت کاٹ کر جلا دیں",
        "safe": False, "econ": "Complete orchard loss over 5-10 years"
    },
    "Peach___Bacterial_spot": {
        "en": "Peach Bacterial Spot", "ur": "آڑو کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas arboricola pv. pruni)", "cause_ur": "بیکٹیریا — بارش اور ہوا سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Small water-soaked spots on leaves turning dark brown with yellow halo", "Shot-hole effect as spots dry and fall out leaving holes", "Fruit develops dark sunken pits reducing quality significantly"],
        "treatments": ["Apply Copper hydroxide bactericide (Kocide) at petal fall", "Spray Oxytetracycline during bloom period if available", "Avoid overhead irrigation — use drip system instead"],
        "prevention": ["Plant bacterial spot-resistant peach and nectarine varieties", "Prune for good airflow through canopy", "Avoid excessive nitrogen promoting soft susceptible growth"],
        "ur_sum": "آڑو میں بیکٹیریل دھبے ہیں۔ کاپر بیکٹیریسائیڈ اسپرے کریں اور اوپر سے پانی دینا بند کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% fruit quality loss"
    },
    "Peach___healthy": {
        "en": "Healthy Peach Plant", "ur": "صحت مند آڑو کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Regular weekly monitoring during growing season", "Annual dormant pruning for shape and airflow", "Balanced fertilization — avoid excess nitrogen"],
        "ur_sum": "آپ کا آڑو کا پودا صحت مند ہے۔ اچھی دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Pepper,_bell___Bacterial_spot": {
        "en": "Bell Pepper Bacterial Spot", "ur": "شملہ مرچ کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas euvesicatoria)", "cause_ur": "بیکٹیریا — بارش کے چھینٹوں اور ہوا سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Small water-soaked lesions on leaves turning dark brown with yellow halo", "Shot-hole appearance as spots dry and fall out", "Raised scab-like lesions on fruit reducing commercial value"],
        "treatments": ["Apply Copper hydroxide bactericide every 5-7 days during wet weather", "Remove and destroy all severely infected plant parts", "Never work in field when plants are wet — spreads bacteria"],
        "prevention": ["Use only certified disease-free seed from reputable supplier", "Practice minimum 2-year crop rotation", "Install drip irrigation to keep foliage dry"],
        "ur_sum": "شملہ مرچ میں بیکٹیریل دھبے ہیں۔ کاپر بیکٹیریسائیڈ اسپرے کریں اور پانی پتوں پر نہ لگنے دیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss if untreated"
    },
    "Pepper,_bell___healthy": {
        "en": "Healthy Bell Pepper Plant", "ur": "صحت مند شملہ مرچ کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor regularly for pests and disease", "Maintain balanced fertilization", "Ensure good drainage — peppers dislike waterlogging"],
        "ur_sum": "آپ کی شملہ مرچ کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Potato___Early_blight": {
        "en": "Potato Early Blight", "ur": "آلو کا ابتدائی جھلساؤ",
        "cause": "Fungal (Alternaria solani)", "cause_ur": "فنگس — گرم موسم میں پرانے اور کمزور پتوں پر پہلے آتی ہے۔",
        "sev": "Medium", "part": "Leaves & Stem", "urgent": False,
        "symptoms": ["Dark brown spots with distinct concentric rings (target board/bullseye pattern)", "Yellow tissue surrounding the dark brown spots", "Lower and older leaves affected first — disease moves upward"],
        "treatments": ["Apply Mancozeb 80WP at 2.5g per liter of water", "Spray Chlorothalonil 75WP as alternative every 7-10 days", "Remove infected lower leaves immediately and destroy them"],
        "prevention": ["Practice crop rotation — no potatoes in same field for 2-3 years", "Avoid wetting foliage — use drip irrigation", "Adequate spacing (60x30cm) for air circulation"],
        "ur_sum": "آلو میں ابتدائی جھلساؤ ہے۔ مینکوزیب فنگسائیڈ اسپرے کریں اور نیچے کے متاثرہ پتے فوری ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss if untreated"
    },
    "Potato___Late_blight": {
        "en": "Potato Late Blight", "ur": "آلو کا جھلساؤ (اہم خطرہ)",
        "cause": "Fungal (Phytophthora infestans)", "cause_ur": "فنگس — نم اور ٹھنڈے موسم میں بہت تیزی سے پھیلتی ہے۔ انتہائی خطرناک!",
        "sev": "High", "part": "Leaves, Stem & Tubers", "urgent": True,
        "symptoms": ["Dark water-soaked lesions on leaf edges and tips — appear greasy", "White cottony fungal growth on leaf undersides in humid conditions", "Infected tubers show reddish-brown internal rot with foul smell"],
        "treatments": ["Apply Cymoxanil + Mancozeb (Curzate M8) IMMEDIATELY at first sign", "Spray every 5-7 days during wet/cool weather — do not skip", "Remove and bury infected plant material at least 30cm deep"],
        "prevention": ["Use only certified disease-free seed potatoes from reliable source", "Never plant in low-lying, waterlogged, or poorly drained areas", "Hill up soil around plants to protect tubers from sporangia splash"],
        "ur_sum": "آلو میں جھلساؤ بیماری ہے — یہ بہت تیزی سے پھیلتی ہے اور دو ہفتوں میں پوری فصل تباہ کر سکتی ہے۔ فوری کیوزیٹ ایم اسپرے کریں اور متاثرہ حصے مٹی میں دفن کریں۔",
        "urgency": "IMMEDIATE — Act within 24 hours", "ur_urgency": "فوری — 24 گھنٹے میں اسپرے کریں",
        "safe": False, "econ": "Complete crop failure within 2 weeks if untreated"
    },
    "Potato___healthy": {
        "en": "Healthy Potato Plant", "ur": "صحت مند آلو کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor weekly — late blight can appear overnight", "Proper hilling to protect developing tubers", "Balanced fertilization with adequate potassium for disease resistance"],
        "ur_sum": "آپ کا آلو کا پودا صحت مند ہے۔ کوئی بیماری نہیں ملی۔ ہفتہ وار نگرانی جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Raspberry___healthy": {
        "en": "Healthy Raspberry Plant", "ur": "صحت مند رسبری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring for cane diseases", "Proper pruning of old canes after harvest", "Balanced fertilization"],
        "ur_sum": "آپ کی رسبری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Soybean___healthy": {
        "en": "Healthy Soybean Plant", "ur": "صحت مند سویابین کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring for rust and other diseases", "Crop rotation every 2-3 years", "Balanced fertilization"],
        "ur_sum": "آپ کی سویابین کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Squash___Powdery_mildew": {
        "en": "Squash Powdery Mildew", "ur": "کدو کی سفید پھپھوندی",
        "cause": "Fungal (Podosphaera xanthii)", "cause_ur": "فنگس — خشک گرم موسم میں اور ٹھنڈی راتوں میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Stems", "urgent": False,
        "symptoms": ["White powdery coating on upper leaf surfaces — easily wiped off", "Leaves turn yellow then brown as infection progresses", "Severely infected plants produce stunted, low quality fruit"],
        "treatments": ["Spray 1% potassium bicarbonate or neem oil (2ml/L) solution", "Apply Sulfur-based fungicide (Thiovit Jet) in early morning", "Remove and destroy all severely infected leaves immediately"],
        "prevention": ["Plant powdery mildew-resistant squash/pumpkin varieties", "Avoid excess nitrogen fertilizer — promotes lush susceptible growth", "Space plants generously for maximum air circulation"],
        "ur_sum": "کدو میں سفید پھپھوندی ہے۔ سلفر یا بائیکاربونیٹ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "10-25% yield loss if unmanaged"
    },
    "Strawberry___Leaf_scorch": {
        "en": "Strawberry Leaf Scorch", "ur": "اسٹرابیری کا پتہ جلاؤ",
        "cause": "Fungal (Diplocarpon earliana)", "cause_ur": "فنگس — نم اور گرم موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Small dark purple to red spots on upper leaf surface", "Spots enlarge and merge turning leaves brown and scorched", "Severely affected leaves dry up completely and die"],
        "treatments": ["Apply Captan 50WP or Myclobutanil fungicide every 10-14 days", "Remove and destroy all infected leaves from bed", "Avoid overhead irrigation — water at soil level only"],
        "prevention": ["Plant only certified disease-free strawberry runners", "Maintain good air circulation by proper plant spacing (30x30cm)", "Remove all old leaves after harvest season"],
        "ur_sum": "اسٹرابیری کے پتوں میں جلاؤ بیماری ہے۔ کیپٹان فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss if untreated"
    },
    "Strawberry___healthy": {
        "en": "Healthy Strawberry Plant", "ur": "صحت مند اسٹرابیری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor regularly for leaf diseases and mites", "Proper drainage — strawberries hate waterlogged soil", "Balanced fertilization with adequate potassium"],
        "ur_sum": "آپ کی اسٹرابیری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
    "Tomato___Bacterial_spot": {
        "en": "Tomato Bacterial Spot", "ur": "ٹماٹر کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas vesicatoria)", "cause_ur": "بیکٹیریا — بارش کے چھینٹوں اور آلودہ بیجوں سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Small water-soaked spots turning dark brown with yellow halo on leaves", "Shot-hole appearance as infected tissue dries and falls out", "Raised scab spots on green fruit reducing market value"],
        "treatments": ["Apply Copper hydroxide bactericide (Kocide 2000) every 5-7 days", "Remove and destroy infected leaves and plant debris immediately", "Stop overhead irrigation — switch to drip system"],
        "prevention": ["Use certified disease-free seed — treat with hot water (50°C, 25 min)", "Practice 2-year rotation — no tomatoes or peppers in same bed", "Avoid working in field when plants are wet"],
        "ur_sum": "ٹماٹر میں بیکٹیریل دھبے ہیں۔ کاپر فنگسائیڈ اسپرے کریں اور اوپر سے پانی دینا بند کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% loss if untreated"
    },
    "Tomato___Early_blight": {
        "en": "Tomato Early Blight", "ur": "ٹماٹر کا ابتدائی جھلساؤ",
        "cause": "Fungal (Alternaria solani)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Stem", "urgent": False,
        "symptoms": ["Circular brown spots with distinct concentric target-board rings", "Yellow chlorotic halo surrounding each dark brown spot", "Lower and older leaves affected first — progresses upward"],
        "treatments": ["Apply Mancozeb 80WP at 2.5g/L every 7-10 days", "Spray Chlorothalonil 75WP as effective alternative", "Remove infected lower leaves immediately to slow spread"],
        "prevention": ["Annual crop rotation — never plant tomatoes in same spot", "Mulch around plants to prevent soil splash onto leaves", "Space plants 60cm apart for adequate airflow"],
        "ur_sum": "ٹماٹر میں ابتدائی جھلساؤ ہے — قابل علاج ہے۔ نیچے کے متاثرہ پتے ہٹائیں اور مینکوزیب فنگسائیڈ اسپرے کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% yield loss if untreated"
    },
    "Tomato___Late_blight": {
        "en": "Tomato Late Blight", "ur": "ٹماٹر کا جھلساؤ (انتہائی خطرناک)",
        "cause": "Fungal (Phytophthora infestans)", "cause_ur": "فنگس — نم اور ٹھنڈے موسم میں بہت تیزی سے پھیلتی ہے۔ انتہائی خطرناک!",
        "sev": "High", "part": "Leaves, Stem & Fruit", "urgent": True,
        "symptoms": ["Dark brown water-soaked lesions on leaf edges appearing overnight", "White cottony mold on leaf undersides in humid/cool conditions", "Fruit turns dark brown and rots rapidly — within days"],
        "treatments": ["Remove and destroy infected plant parts IMMEDIATELY — do not compost", "Apply Copper-based fungicide (Kocide/Blue Shield) same day", "Spray Mancozeb 80WP at 2.5g/L every 5-7 days", "Water only at base — never wet the foliage"],
        "prevention": ["Plant late-blight resistant varieties (Mountain Magic, Jasper)", "Ensure minimum 60cm spacing for air circulation", "Never work in field after rain when spores spread most"],
        "ur_sum": "ٹماٹر میں جھلساؤ بیماری ہے — انتہائی فوری توجہ ضروری ہے! متاثرہ پتے اور شاخیں فوری ہٹائیں اور کاپر فنگسائیڈ اسپرے کریں۔ دیر ہوئی تو پوری فصل ایک ہفتے میں تباہ ہو سکتی ہے۔",
        "urgency": "IMMEDIATE — Act today", "ur_urgency": "فوری — آج ہی اسپرے کریں",
        "safe": False, "econ": "70-100% loss if untreated within 1 week"
    },
    "Tomato___Leaf_Mold": {
        "en": "Tomato Leaf Mold", "ur": "ٹماٹر کی پتہ پھپھوندی",
        "cause": "Fungal (Passalora fulva)", "cause_ur": "فنگس — گرم اور زیادہ نمی والے بند ماحول میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Pale green to yellow spots on upper leaf surface", "Olive-green to brown velvety mold growth on leaf undersides", "Leaves curl upward and drop in severe infections"],
        "treatments": ["Reduce humidity immediately — improve ventilation in greenhouse", "Apply Chlorothalonil or Mancozeb fungicide every 7-10 days", "Remove infected leaves and destroy outside the growing area"],
        "prevention": ["Maintain relative humidity below 85% at all times", "Space plants 60-75cm apart for airflow", "Use resistant varieties — many modern hybrids have Cf resistance genes"],
        "ur_sum": "ٹماٹر کے پتوں پر پھپھوندی ہے۔ نمی کم کریں، ہوا کی آمدورفت بڑھائیں اور فنگسائیڈ اسپرے کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss in severe cases"
    },
    "Tomato___Septoria_leaf_spot": {
        "en": "Septoria Leaf Spot", "ur": "ٹماٹر کے سیپٹوریا دھبے",
        "cause": "Fungal (Septoria lycopersici)", "cause_ur": "فنگس — بارش اور اوس والے موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves", "urgent": False,
        "symptoms": ["Numerous small circular spots with dark brown border and grey-white center", "Tiny black dots (pycnidia — spore cases) visible inside each spot", "Lower leaves turn yellow and drop first — plant defoliates from bottom up"],
        "treatments": ["Apply Chlorothalonil 75WP or Mancozeb every 7-10 days", "Remove infected lower leaves immediately at first sign", "Avoid splashing water on foliage — use drip irrigation"],
        "prevention": ["Strict crop rotation — no tomatoes or related crops for 2+ years", "Sanitize all tools between plants with 10% bleach solution", "Remove all crop debris after season — do not leave in field"],
        "ur_sum": "ٹماٹر میں سیپٹوریا دھبے ہیں۔ فنگسائیڈ اسپرے کریں اور متاثرہ پتے فوری ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-30% loss if untreated"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "en": "Spider Mite Infestation", "ur": "ٹماٹر پر مکڑی کے کیڑے",
        "cause": "Pest (Tetranychus urticae — Two-spotted spider mite)", "cause_ur": "کیڑا (مکڑی کی قسم) — خشک اور گرم موسم میں بہت تیزی سے بڑھتا ہے۔",
        "sev": "Medium", "part": "Leaves (underside)", "urgent": False,
        "symptoms": ["Tiny yellow/white stippling dots on upper leaf surface — sandpaper feel", "Fine silky webbing visible on leaf undersides with magnifying glass", "Leaves turn bronze/rusty and dry up — plant looks scorched"],
        "treatments": ["Apply Abamectin 1.8EC (0.5ml/L) or Spiromesifen miticide", "Spray Neem oil solution (5ml/L) as effective organic alternative", "Strong water jet on undersides of leaves knocks off large populations"],
        "prevention": ["Maintain adequate soil moisture — mites thrive in dry dusty conditions", "Introduce predatory mites (Phytoseiulus persimilis) for biological control", "Avoid dusty roads near field — dust suppresses natural predators"],
        "ur_sum": "ٹماٹر پر مکڑی کے کیڑے ہیں۔ ابامیکٹن اسپرے کریں یا نیم کا تیل (5ml/L) استعمال کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% loss in severe infestations"
    },
    "Tomato___Target_Spot": {
        "en": "Tomato Target Spot", "ur": "ٹماٹر کا ہدف دھبہ",
        "cause": "Fungal (Corynespora cassiicola)", "cause_ur": "فنگس — گرم اور نم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit", "urgent": False,
        "symptoms": ["Brown spots with distinct concentric target/bullseye rings on leaves", "Spots have yellow halo similar to early blight but larger", "Dark sunken lesions on fruit surface reducing quality"],
        "treatments": ["Apply Chlorothalonil or Azoxystrobin fungicide every 7-14 days", "Remove infected leaves and fruit from field immediately", "Increase plant spacing to improve air circulation"],
        "prevention": ["Annual crop rotation", "Avoid leaf wetness — drip irrigation preferred", "Use resistant varieties where available"],
        "ur_sum": "ٹماٹر میں ہدف دھبہ بیماری ہے۔ فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% loss if untreated"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "en": "Yellow Leaf Curl Virus (TYLCV)", "ur": "ٹماٹر کا پیلا پتہ کرل وائرس",
        "cause": "Viral (TYLCV — transmitted by Bemisia tabaci whitefly)", "cause_ur": "وائرس — سفید مکھی (بیمیسیا) کے ذریعے پھیلتا ہے — کوئی علاج نہیں۔",
        "sev": "High", "part": "Whole Plant", "urgent": True,
        "symptoms": ["Young leaves curl upward and inward with yellow edges", "Plant severely stunted — remains dwarfed throughout season", "Little to no fruit set — flowers drop before setting"],
        "treatments": ["NO CURE — remove and destroy infected plants immediately", "Control whitefly vector with Imidacloprid 200SL (0.5ml/L) soil drench", "Install yellow sticky traps (1 per 50 sq.m) to monitor whitefly"],
        "prevention": ["Plant TYLCV-resistant tomato varieties (Thilak, Rossol, Sahel)", "Use 50-mesh insect-proof net houses for nursery raising", "Spray seedlings with Imidacloprid before transplanting"],
        "ur_sum": "ٹماٹر میں پیلا پتہ کرل وائرس ہے — کوئی علاج نہیں ہے۔ متاثرہ پودے فوری اکھاڑ کر جلا دیں اور سفید مکھی کو کنٹرول کریں۔",
        "urgency": "Immediate — Remove infected plants", "ur_urgency": "فوری — پودے ابھی نکالیں",
        "safe": False, "econ": "Up to 100% loss in severe outbreaks"
    },
    "Tomato___Tomato_mosaic_virus": {
        "en": "Tomato Mosaic Virus (ToMV)", "ur": "ٹماٹر کا موزیک وائرس",
        "cause": "Viral (ToMV — contact transmitted via hands/tools/seed)", "cause_ur": "وائرس — ہاتھوں، اوزاروں اور آلودہ بیجوں سے پھیلتا ہے۔",
        "sev": "High", "part": "Whole Plant", "urgent": True,
        "symptoms": ["Mosaic pattern of light and dark green on leaves — distinct mottled look", "Leaves distorted, wrinkled, cupped and puckered", "Fruit shows yellow mottling and ripens unevenly"],
        "treatments": ["NO CURE — remove and destroy all infected plants immediately", "Wash hands with soap thoroughly before handling any plants", "Sterilize ALL tools with 10% bleach or 70% alcohol between plants"],
        "prevention": ["Use virus-free certified seed — treat with trisodium phosphate (10%)", "Wash hands before every field entry — never smoke near plants (tobacco carries ToMV)", "Control aphid populations which can also spread the virus"],
        "ur_sum": "ٹماٹر میں موزیک وائرس ہے — کوئی علاج نہیں۔ متاثرہ پودے فوری ہٹائیں، ہاتھ صابن سے دھوئیں اور تمام اوزار صاف کریں۔",
        "urgency": "Immediate — Remove infected plants", "ur_urgency": "فوری — متاثرہ پودے ابھی ہٹائیں",
        "safe": False, "econ": "20-70% yield loss depending on infection timing"
    },
    "Tomato___healthy": {
        "en": "Healthy Tomato Plant", "ur": "صحت مند ٹماٹر کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "urgent": False,
        "symptoms": [], "treatments": [],
        "prevention": ["Monitor every 3-4 days — tomato diseases can develop fast", "Stake plants properly for air circulation and disease prevention", "Balanced NPK with adequate calcium to prevent blossom end rot"],
        "ur_sum": "آپ کا ٹماٹر کا پودا بالکل صحت مند ہے۔ کوئی بیماری نہیں ملی۔ اسی طرح دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں",
        "safe": True, "econ": "None"
    },
}

def get_info(label):
    if label in DB:
        return DB[label]
    for k in DB:
        if label.lower() in k.lower():
            return DB[k]
    healthy = "healthy" in label.lower()
    parts = label.split("___")
    dis = parts[1].replace("_", " ") if len(parts) > 1 else label
    return {
        "en": "Healthy Plant" if healthy else dis,
        "ur": "صحت مند پودا" if healthy else dis,
        "cause": "None" if healthy else "Pathogen detected",
        "cause_ur": "کوئی بیماری نہیں۔" if healthy else "بیماری ملی — مقامی زراعت افسر سے رابطہ کریں۔",
        "sev": "None" if healthy else "Medium",
        "part": "None" if healthy else "Leaves",
        "urgent": False,
        "symptoms": [],
        "treatments": [] if healthy else ["Consult your local Agricultural Extension Officer (زراعت افسر)", "Collect a leaf sample for laboratory testing", "Apply broad-spectrum fungicide as precaution"],
        "prevention": ["Regular monitoring", "Balanced fertilization", "Proper irrigation"],
        "ur_sum": "آپ کا پودا صحت مند ہے۔" if healthy else "پودا متاثر ہے۔ مقامی زراعت افسر سے مشورہ کریں۔",
        "urgency": "No action needed" if healthy else "Consult expert",
        "ur_urgency": "کوئی ضرورت نہیں" if healthy else "ماہر سے مشورہ کریں",
        "safe": True, "econ": "None" if healthy else "Monitor for spread"
    }

# ── Model Loading ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    checkpoint = torch.load("fasalguard_model.pth", map_location="cpu")
    class_names = checkpoint["class_names"]
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(model.last_channel, 512),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(512, len(class_names))
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    return model, transform, class_names

def predict(img_pil):
    try:
        model, transform, class_names = load_model()
        tensor = transform(img_pil.convert("RGB")).unsqueeze(0)
        with torch.no_grad():
            out = model(tensor)
            probs = torch.nn.functional.softmax(out, dim=1)
            top3_probs, top3_idx = torch.topk(probs, 3)
        results = [(class_names[top3_idx[0][i].item()], round(top3_probs[0][i].item()*100)) for i in range(3)]
        return results
    except Exception as e:
        return None

# ── Crops ─────────────────────────────────────────────────────────────────────
CROPS = [
    "🍎 Apple (سیب)", "🫐 Blueberry (بلوبیری)", "🍒 Cherry (چیری)",
    "🌽 Corn / Maize (مکئی)", "🍇 Grape (انگور)", "🍊 Orange / Citrus (مالٹا)",
    "🍑 Peach (آڑو)", "🌶️ Bell Pepper (شملہ مرچ)", "🥔 Potato (آلو)",
    "🫐 Raspberry (رسبری)", "🫘 Soybean (سویابین)", "🥗 Squash (کدو)",
    "🍓 Strawberry (اسٹرابیری)", "🍅 Tomato (ٹماٹر)"
]

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🌾 AI-Powered &nbsp;·&nbsp; 100% Free &nbsp;·&nbsp; Pakistan</div>
    <h1 class="hero-title">Fasal<span>Guard</span></h1>
    <p class="hero-subtitle">Upload a photo of your crop leaf — get instant AI diagnosis and complete treatment plan</p>
    <p class="hero-urdu">اپنی فصل کی تصویر اپلوڈ کریں — فوری تشخیص اور مکمل علاج پائیں</p>
    <div class="stats-row">
        <div class="stat-item"><span class="stat-num">99%</span><span class="stat-label">AI Accuracy</span></div>
        <div class="stat-item"><span class="stat-num">38</span><span class="stat-label">Diseases</span></div>
        <div class="stat-item"><span class="stat-num">14</span><span class="stat-label">Crops</span></div>
        <div class="stat-item"><span class="stat-num">Free</span><span class="stat-label">Always</span></div>
        <div class="stat-item"><span class="stat-num">EN+UR</span><span class="stat-label">Bilingual</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<span class="section-label">Select Your Crop &nbsp;·&nbsp; فصل منتخب کریں</span>', unsafe_allow_html=True)
    crop_choice = st.selectbox("Crop", CROPS, label_visibility="collapsed")
    st.markdown('<span class="section-label" style="margin-top:1.3rem;display:block">Upload Leaf Photo &nbsp;·&nbsp; پتے کی تصویر اپلوڈ کریں</span>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded:
        st.markdown('<span class="section-label" style="margin-top:0.8rem;display:block">Preview</span>', unsafe_allow_html=True)
        st.image(Image.open(uploaded), use_column_width=True, output_format="JPEG")

with col2:
    st.markdown("""
    <div class="how-card">
        <span class="section-label">How It Works &nbsp;·&nbsp; کیسے کام کرتا ہے</span>
        <div style="margin-top:1rem;">
            <div class="how-step"><div class="step-num">1</div><div><div class="step-en">Select your crop type</div><div class="step-ur">اپنی فصل منتخب کریں</div></div></div>
            <div class="how-step"><div class="step-num">2</div><div><div class="step-en">Upload a clear close-up leaf photo</div><div class="step-ur">پتے کی واضح قریبی تصویر اپلوڈ کریں</div></div></div>
            <div class="how-step"><div class="step-num">3</div><div><div class="step-en">Click Analyze — AI detects disease instantly</div><div class="step-ur">تجزیہ کریں — AI فوری بیماری پہچانے گا</div></div></div>
            <div class="how-step" style="margin-bottom:0;"><div class="step-num">4</div><div><div class="step-en">Follow the complete treatment plan</div><div class="step-ur">مکمل علاج پر عمل کریں</div></div></div>
        </div>
        <div class="photo-tips">
            <div class="tips-title">📸 Tips for Best Accuracy</div>
            <div class="tips-text">
                • Single leaf close-up — not whole plant<br>
                • Natural daylight — never use flash<br>
                • Sharp, in-focus image only<br>
                • Show the most affected area clearly<br>
                • Avoid shadows across the leaf
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if uploaded:
    if st.button("🔬  Analyze My Crop &nbsp;·&nbsp; فصل کا تجزیہ کریں", use_container_width=True):
        uploaded.seek(0)
        img_pil = Image.open(uploaded).convert("RGB")

        with st.spinner("🔬 AI is analyzing your crop... فصل کا تجزیہ ہو رہا ہے"):
            results = predict(img_pil)

        if results is None:
            st.error("Analysis error. Please try again with a clearer, close-up leaf photo.")
        else:
            label, confidence = results[0][0], results[0][1]
            info = get_info(label)
            is_healthy = info["sev"] == "None"
            sev = info["sev"]
            sev_map = {"High":("sev-high","🔴"), "Medium":("sev-medium","🟡"), "Low":("sev-low","🟢"), "None":("sev-none","🟢")}
            sev_class, sev_icon = sev_map.get(sev, ("sev-low","🟢"))

            if is_healthy:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-header">
                        <div style="flex:1;">
                            <div style="font-size:0.62rem;color:#4ade80;text-transform:uppercase;letter-spacing:1.5px;font-weight:800;margin-bottom:8px;">Diagnosis Result · تشخیص</div>
                            <div style="font-size:1.5rem;font-weight:800;color:#4ade80;">✓ {info['en']}</div>
                            <div style="font-size:1rem;color:#4a6f4a;margin-top:4px;">{info['ur']}</div>
                        </div>
                        <span class="severity-badge sev-none">🟢 No Disease</span>
                    </div>
                    <div class="result-body">
                        <div class="conf-bar-wrap">
                            <div class="conf-row"><span class="conf-label">AI Confidence</span><span class="conf-val">{confidence}%</span></div>
                            <div class="conf-bg"><div class="conf-fill" style="width:{confidence}%"></div></div>
                        </div>
                        <div class="healthy-banner">
                            <div style="font-size:2.5rem;margin-bottom:10px;">✅</div>
                            <div style="font-size:1.05rem;font-weight:700;color:#4ade80;margin-bottom:6px;">Your plant is perfectly healthy!</div>
                            <div style="font-size:0.85rem;color:#4a6f4a;">No signs of disease, pest damage, or nutrient deficiency detected by AI.</div>
                        </div>
                        <hr class="divider">
                        <div class="list-section"><h4>Preventive Care Recommendations · احتیاطی تدابیر</h4>
                        {''.join(f'<div class="list-item"><div class="dot dot-blue"></div><div class="list-text">{p}</div></div>' for p in info['prevention'])}
                        </div>
                        <div class="urdu-block">
                            <div class="urdu-title">اردو خلاصہ</div>
                            <div class="urdu-text">{info['ur_sum']}<br><br><strong style="color:#4ade80">{info['ur_urgency']}</strong></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                urgent_html = ""
                if info.get("urgent"):
                    urgent_html = f"""
                    <div class="alert-box">
                        <div class="alert-icon">🚨</div>
                        <div class="alert-text"><strong>Urgent Action Required!</strong> This disease can cause significant crop loss if not treated immediately. Follow the treatment plan below today.</div>
                    </div>"""

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-header">
                        <div style="flex:1;">
                            <div style="font-size:0.62rem;color:#4ade80;text-transform:uppercase;letter-spacing:1.5px;font-weight:800;margin-bottom:8px;">Diagnosis Result · تشخیص</div>
                            <div style="font-size:1.5rem;font-weight:800;color:#f0faf0;">{info['en']}</div>
                            <div style="font-size:1rem;color:#4ade80;margin-top:4px;">{info['ur']}</div>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end;">
                            <span class="severity-badge {sev_class}">{sev_icon} {sev} Severity</span>
                            <span style="font-size:0.7rem;color:#4a6f4a;white-space:nowrap;font-weight:600;">{info['urgency']}</span>
                        </div>
                    </div>
                    <div class="result-body">
                        {urgent_html}
                        <div class="conf-bar-wrap">
                            <div class="conf-row"><span class="conf-label">AI Confidence</span><span class="conf-val">{confidence}%</span></div>
                            <div class="conf-bg"><div class="conf-fill" style="width:{confidence}%"></div></div>
                        </div>
                        <div class="info-grid">
                            <div class="info-block"><div class="ib-label">Affected Part</div><div class="ib-val">{info['part']}</div></div>
                            <div class="info-block"><div class="ib-label">Cause</div><div class="ib-val">{info['cause']}</div></div>
                            <div class="info-block"><div class="ib-label">Safe to Harvest?</div><div class="ib-val" style="color:{'#4ade80' if info['safe'] else '#f87171'}">{'✓ Yes — safe' if info['safe'] else '✗ Not recommended'}</div></div>
                            <div class="info-block"><div class="ib-label">Economic Risk</div><div class="ib-val" style="font-size:0.85rem;">{info['econ']}</div></div>
                        </div>
                        <hr class="divider">
                """, unsafe_allow_html=True)

                if info['symptoms']:
                    st.markdown('<div class="list-section"><h4>Observed Symptoms · علامات</h4>', unsafe_allow_html=True)
                    for s in info['symptoms']:
                        st.markdown(f'<div class="list-item"><div class="dot dot-yellow"></div><div class="list-text">{s}</div></div>', unsafe_allow_html=True)
                    st.markdown('</div><hr class="divider">', unsafe_allow_html=True)

                if info['treatments']:
                    st.markdown('<div class="list-section"><h4>Treatment Plan · علاج کا طریقہ</h4>', unsafe_allow_html=True)
                    for t in info['treatments']:
                        st.markdown(f'<div class="list-item"><div class="dot dot-green"></div><div class="list-text">{t}</div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                if info['prevention']:
                    st.markdown('<hr class="divider"><div class="list-section"><h4>Prevention for Next Season · بچاؤ کے طریقے</h4>', unsafe_allow_html=True)
                    for p in info['prevention']:
                        st.markdown(f'<div class="list-item"><div class="dot dot-blue"></div><div class="list-text">{p}</div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Alternative diagnoses
                if len(results) > 1:
                    alt_html = ""
                    for alt_label, alt_conf in results[1:]:
                        alt_info = get_info(alt_label)
                        alt_html += f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1a3a1a;"><span style="font-size:0.82rem;color:#8ab88a;">{alt_info["en"]}</span><span style="font-size:0.78rem;color:#4a6f4a;font-weight:600;">{alt_conf}%</span></div>'
                    st.markdown(f"""
                    <hr class="divider">
                    <div style="margin-bottom:1rem;">
                        <div style="font-size:0.65rem;color:#4ade80;text-transform:uppercase;letter-spacing:1.5px;font-weight:800;margin-bottom:0.7rem;">Alternative Possibilities · دیگر ممکنہ تشخیص</div>
                        {alt_html}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                        <div class="urdu-block">
                            <div class="urdu-title">اردو خلاصہ</div>
                            <div class="urdu-text">{info['cause_ur']}<br><br>{info['ur_sum']}<br><br><strong style="color:#4ade80;font-size:1.05rem;">{info['ur_urgency']}</strong></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:5rem 1rem;">
        <div style="font-size:5rem;margin-bottom:1.2rem;opacity:0.25;">🌾</div>
        <div style="font-size:1.1rem;color:#3a5a3a;margin-bottom:0.5rem;font-weight:600;">Upload a crop photo to begin analysis</div>
        <div style="font-size:0.9rem;color:#2a4a2a;">تصویر اپلوڈ کریں اور شروع کریں</div>
        <div style="margin-top:1.5rem;font-size:0.78rem;color:#1a3a1a;">For best results: close-up photo of a single affected leaf in natural daylight</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-section">
    <div class="footer-text">
        <strong style="color:#3a5a3a;font-size:0.82rem;">FasalGuard</strong> &nbsp;·&nbsp; Pakistan's AI Crop Health Platform &nbsp;·&nbsp; پاکستان کا پہلا AI فصل صحت پلیٹ فارم<br>
        Trained on 70,000+ images &nbsp;·&nbsp; <strong style="color:#3a5a3a;">99% Accuracy</strong> &nbsp;·&nbsp; 38 Disease Classes &nbsp;·&nbsp; 14 Crops &nbsp;·&nbsp; MobileNetV2 Full Fine-Tuning<br><br>
        <span style="color:#1a3a1a;">⚠️ For serious disease outbreaks, always consult your local Agricultural Extension Officer (زراعت افسر)</span><br>
        <span style="color:#0f2a0f;font-size:0.65rem;margin-top:8px;display:block;">
            Powered by PyTorch + MobileNetV2 &nbsp;·&nbsp; 100% Free &nbsp;·&nbsp; No API Key &nbsp;·&nbsp; No Limits &nbsp;·&nbsp; Open Source
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
