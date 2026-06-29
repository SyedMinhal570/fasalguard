import streamlit as st
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn as nn
import json
import os
import io

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FasalGuard 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: #0a0f0a !important; color: #e8f0e8 !important; font-family: 'Inter', sans-serif; }
.stApp > header { display: none; }
[data-testid="stSidebar"] { display: none; }

.hero-section {
    background: linear-gradient(135deg, #0a0f0a 0%, #0f1f0f 40%, #0a1a0a 100%);
    border-bottom: 1px solid #1a3a1a;
    padding: 3rem 2rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(34,197,94,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    color: #f0faf0;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}
.hero-title span { color: #4ade80; }
.hero-subtitle { font-size: 1rem; color: #6b9f6b; max-width: 540px; margin: 0 auto 0.4rem; line-height: 1.6; }
.hero-urdu { font-size: 1.1rem; color: #4ade80; opacity: 0.8; margin-bottom: 2rem; font-weight: 300; }
.stats-row { display: flex; justify-content: center; gap: 3rem; margin-top: 1.5rem; flex-wrap: wrap; }
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 1.6rem; font-weight: 700; color: #4ade80; line-height: 1; }
.stat-label { display: block; font-size: 0.68rem; color: #6b9f6b; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 4px; }

.main-container { max-width: 960px; margin: 0 auto; padding: 2rem 1.5rem; }
.section-label { font-size: 0.68rem; font-weight: 600; color: #4ade80; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.7rem; display: block; }

.how-card {
    background: #0f1f0f;
    border: 1px solid #1a3a1a;
    border-radius: 14px;
    padding: 1.4rem;
}
.how-step { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 1rem; }
.step-num {
    width: 28px; height: 28px; border-radius: 50%;
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; color: #4ade80; flex-shrink: 0;
}
.step-en { font-size: 0.85rem; color: #c8e6c8; font-weight: 500; }
.step-ur { font-size: 0.75rem; color: #6b9f6b; margin-top: 2px; }

.photo-tips {
    margin-top: 1rem; padding: 0.8rem;
    background: #0a150a; border-radius: 8px; border: 1px solid #1a3a1a;
}
.tips-title { font-size: 0.7rem; color: #4ade80; font-weight: 600; margin-bottom: 4px; }
.tips-text { font-size: 0.75rem; color: #6b9f6b; line-height: 1.7; }

.result-card { background: #0f1f0f; border: 1px solid #1a3a1a; border-radius: 16px; overflow: hidden; margin-top: 1.5rem; }
.result-header { background: linear-gradient(135deg, #0f2a0f, #162816); padding: 1.5rem; border-bottom: 1px solid #1a3a1a; display: flex; align-items: flex-start; gap: 1rem; }
.result-body { padding: 1.5rem; }

.severity-badge { padding: 4px 14px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }
.sev-high { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); color: #f87171; }
.sev-medium { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); color: #fbbf24; }
.sev-low { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.4); color: #4ade80; }
.sev-none { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.4); color: #4ade80; }

.conf-bar-wrap { margin: 1rem 0; }
.conf-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
.conf-label { font-size: 0.73rem; color: #6b9f6b; }
.conf-val { font-size: 0.73rem; color: #4ade80; font-weight: 700; }
.conf-bg { background: #1a3a1a; border-radius: 6px; height: 7px; overflow: hidden; }
.conf-fill { height: 100%; background: linear-gradient(90deg, #16a34a, #4ade80); border-radius: 6px; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin: 1rem 0; }
.info-block { background: #0a150a; border: 1px solid #1a3a1a; border-radius: 10px; padding: 0.9rem; }
.ib-label { font-size: 0.65rem; color: #4ade80; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 0.35rem; }
.ib-val { font-size: 0.9rem; color: #c8e6c8; font-weight: 500; line-height: 1.4; }

.divider { border: none; border-top: 1px solid #1a3a1a; margin: 1.2rem 0; }

.list-section h4 { font-size: 0.72rem; font-weight: 700; color: #4ade80; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 0.8rem; }
.list-item { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 0.55rem; padding: 0.65rem 0.8rem; background: #0a150a; border-radius: 8px; border: 1px solid #1a3a1a; }
.dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 7px; flex-shrink: 0; }
.dot-green { background: #4ade80; }
.dot-blue { background: #60a5fa; }
.dot-yellow { background: #fbbf24; }
.list-text { font-size: 0.86rem; color: #a8cca8; line-height: 1.55; }

.urdu-block {
    background: linear-gradient(135deg, #0a150a, #0f1f0f);
    border: 1px solid #2a4a2a;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-top: 1.2rem;
    direction: rtl;
    text-align: right;
}
.urdu-title { font-size: 0.78rem; color: #4ade80; margin-bottom: 0.6rem; font-weight: 700; letter-spacing: 0.5px; }
.urdu-text { font-size: 0.97rem; color: #a8cca8; line-height: 2; }

.healthy-banner {
    background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(34,197,94,0.03));
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}

.footer-section { text-align: center; padding: 2.5rem 1.5rem; border-top: 1px solid #1a3a1a; margin-top: 3rem; }
.footer-text { font-size: 0.73rem; color: #3d5c3d; line-height: 2; }

[data-testid="stFileUploadDropzone"] {
    background: #0a150a !important;
    border: 1.5px dashed #2a4a2a !important;
    border-radius: 12px !important;
    color: #6b9f6b !important;
}
.stSelectbox > div > div {
    background: #0f1f0f !important;
    border: 1px solid #2a4a2a !important;
    border-radius: 8px !important;
    color: #c8e6c8 !important;
}
div[data-testid="stMarkdownContainer"] p { color: #a8cca8; }

@media (max-width: 640px) {
    .info-grid { grid-template-columns: 1fr; }
    .stats-row { gap: 1.5rem; }
    .hero-section { padding: 2rem 1rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ─── Disease Knowledge Base (All 38 Classes) ─────────────────────────────────
DB = {
    "Apple___Apple_scab": {
        "en": "Apple Scab", "ur": "سیب کا کھرنڈ",
        "cause": "Fungal (Venturia inaequalis)", "cause_ur": "فنگس — بہار میں بارش کے ساتھ پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Olive-green to brown scab-like spots on leaves", "Velvety texture on spots", "Fruit develops hard, corky scabs"],
        "treatments": ["Apply Captan or Myclobutanil fungicide at bud-break", "Spray every 10 days during wet weather", "Remove and destroy infected fallen leaves"],
        "prevention": ["Plant scab-resistant apple varieties", "Rake and burn fallen leaves every season", "Prune trees for good airflow"],
        "ur_sum": "سیب میں کھرنڈ بیماری ہے جو فنگس کی وجہ سے ہوتی ہے۔ کیپٹان یا مائیکلوبٹانیل فنگسائیڈ اسپرے کریں اور گرے ہوئے پتے تلف کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% cosmetic + yield loss"
    },
    "Apple___Black_rot": {
        "en": "Apple Black Rot", "ur": "سیب کی کالی سڑن",
        "cause": "Fungal (Botryosphaeria obtusa)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں پھیلتی ہے۔",
        "sev": "High", "part": "Fruit, Leaves & Bark",
        "symptoms": ["Purple spots on leaves expanding to brown with purple border", "Fruit turns black and shrivels", "Cankers form on branches"],
        "treatments": ["Remove and destroy all mummified fruit immediately", "Apply Captan or Thiophanate-methyl fungicide", "Prune out all dead/cankered wood"],
        "prevention": ["Remove all fruit mummies from trees and ground", "Avoid wounding bark during pruning", "Maintain tree vigor with proper fertilization"],
        "ur_sum": "سیب میں کالی سڑن ہے۔ تمام متاثرہ پھل فوری ہٹائیں اور فنگسائیڈ اسپرے کریں۔ مردہ شاخیں کاٹ کر جلا دیں۔",
        "urgency": "Immediate", "ur_urgency": "فوری توجہ درکار ہے",
        "safe": False, "econ": "Up to 100% fruit loss if untreated"
    },
    "Apple___Cedar_apple_rust": {
        "en": "Cedar Apple Rust", "ur": "سیب کا زنگ",
        "cause": "Fungal (Gymnosporangium juniperi-virginianae)", "cause_ur": "فنگس — صنوبر اور سیب کے درختوں کے درمیان پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Bright orange-yellow spots on upper leaf surface", "Tube-like structures on leaf undersides", "Premature leaf drop in severe cases"],
        "treatments": ["Apply Myclobutanil or Propiconazole at pink bud stage", "Spray every 7-10 days during spring", "Remove nearby cedar/juniper trees if possible"],
        "prevention": ["Plant rust-resistant apple varieties", "Remove juniper/cedar trees within 1km if feasible", "Apply protective fungicide before symptoms appear"],
        "ur_sum": "سیب میں زنگ بیماری ہے۔ بہار میں مائیکلوبٹانیل اسپرے کریں اور قریبی صنوبر کے درختوں سے دور رہیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss in heavy infections"
    },
    "Apple___healthy": {
        "en": "Healthy Apple Plant", "ur": "صحت مند سیب کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None",
        "symptoms": [], "treatments": [],
        "prevention": ["Continue regular monitoring every 2 weeks", "Maintain balanced NPK fertilization", "Ensure proper irrigation and drainage"],
        "ur_sum": "آپ کا سیب کا پودا بالکل صحت مند ہے۔ کوئی بیماری نہیں ملی۔ اسی طرح دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Blueberry___healthy": {
        "en": "Healthy Blueberry Plant", "ur": "صحت مند بلوبیری",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Maintain soil pH 4.5-5.5 for blueberries", "Ensure adequate drainage"],
        "ur_sum": "آپ کی بلوبیری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "en": "Cherry Powdery Mildew", "ur": "چیری کی سفید پھپھوندی",
        "cause": "Fungal (Podosphaera clandestina)", "cause_ur": "فنگس — خشک گرم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Young Shoots",
        "symptoms": ["White powdery coating on leaf surfaces", "Distorted and curling young leaves", "Premature leaf drop in severe cases"],
        "treatments": ["Apply Sulfur-based fungicide or Myclobutanil", "Spray potassium bicarbonate solution as organic option", "Remove severely infected shoots"],
        "prevention": ["Plant resistant varieties", "Avoid excess nitrogen fertilizer", "Prune for good air circulation"],
        "ur_sum": "چیری میں سفید پھپھوندی ہے۔ سلفر فنگسائیڈ اسپرے کریں اور متاثرہ ٹہنیاں کاٹیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "10-20% yield loss if untreated"
    },
    "Cherry_(including_sour)___healthy": {
        "en": "Healthy Cherry Plant", "ur": "صحت مند چیری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Balanced fertilization", "Proper pruning for airflow"],
        "ur_sum": "آپ کی چیری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "en": "Gray Leaf Spot", "ur": "مکئی کا سرمئی دھبہ",
        "cause": "Fungal (Cercospora zeae-maydis)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Rectangular tan-to-gray lesions between leaf veins", "Lesions run parallel to leaf veins", "Severe infection causes leaf death"],
        "treatments": ["Apply Azoxystrobin or Propiconazole fungicide", "Spray at first sign of disease", "Remove infected lower leaves"],
        "prevention": ["Plant resistant hybrids", "Crop rotation — avoid continuous maize", "Till crop residue after harvest"],
        "ur_sum": "مکئی میں سرمئی دھبہ بیماری ہے۔ فنگسائیڈ اسپرے کریں اور اگلے سال فصل بدلیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "Up to 50% yield loss in severe cases"
    },
    "Corn_(maize)___Common_rust_": {
        "en": "Common Rust", "ur": "مکئی کا عام زنگ",
        "cause": "Fungal (Puccinia sorghi)", "cause_ur": "فنگس — ٹھنڈے اور نم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Small powdery reddish-brown pustules on both leaf surfaces", "Pustules turn dark near maturity", "Leaves may yellow and die in severe cases"],
        "treatments": ["Apply Propiconazole or Azoxystrobin fungicide at early tassel stage", "Spray every 14 days if disease pressure is high", "Remove severely infected plants"],
        "prevention": ["Plant rust-resistant maize hybrids", "Early planting to avoid peak rust season", "Monitor fields from July onwards in Pakistan"],
        "ur_sum": "مکئی میں زنگ لگا ہے۔ پروپیکونازول فنگسائیڈ اسپرے کریں اور مزاحم اقسام لگائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں اسپرے کریں",
        "safe": True, "econ": "10-30% yield loss if uncontrolled"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "en": "Northern Leaf Blight", "ur": "مکئی کا شمالی جھلساؤ",
        "cause": "Fungal (Setosphaeria turcica)", "cause_ur": "فنگس — مکئی کے پتوں کو متاثر کرتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Long cigar-shaped gray-green lesions 2.5–15 cm long", "Lesions turn tan/brown as they age", "Severe infection kills leaves before harvest"],
        "treatments": ["Apply Azoxystrobin or Propiconazole at early sign", "Spray at silking stage for best protection", "Remove and till crop residue after harvest"],
        "prevention": ["Plant resistant hybrids when available", "Crop rotation with wheat or legumes", "Balanced fertilization — avoid excess nitrogen"],
        "ur_sum": "مکئی میں شمالی جھلساؤ ہے۔ فنگسائیڈ اسپرے کریں اور اگلے سال مزاحم اقسام استعمال کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "Up to 50% yield loss in severe cases"
    },
    "Corn_(maize)___healthy": {
        "en": "Healthy Maize Plant", "ur": "صحت مند مکئی کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular field monitoring", "Balanced NPK fertilization", "Proper plant spacing for air circulation"],
        "ur_sum": "آپ کی مکئی کا پودا صحت مند ہے۔ کوئی بیماری نہیں ملی۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Grape___Black_rot": {
        "en": "Grape Black Rot", "ur": "انگور کی کالی سڑن",
        "cause": "Fungal (Guignardia bidwellii)", "cause_ur": "فنگس — گرم اور بارشی موسم میں تیزی سے پھیلتی ہے۔",
        "sev": "High", "part": "Leaves & Fruit",
        "symptoms": ["Circular tan spots with dark border on leaves", "Infected fruit turns black and shrivels into mummies", "Black pycnidia (dots) visible inside spots"],
        "treatments": ["Apply Myclobutanil or Mancozeb from bud break", "Spray every 10-14 days during season", "Remove and destroy all infected fruit and leaves immediately"],
        "prevention": ["Remove mummified fruit from vines before spring", "Prune for open canopy and maximum air circulation", "Use disease-resistant grape varieties"],
        "ur_sum": "انگور میں کالی سڑن ہے — پھل تیزی سے ضائع ہو سکتا ہے۔ فوری فنگسائیڈ اسپرے اور متاثرہ پھل ہٹائیں۔",
        "urgency": "Immediate", "ur_urgency": "فوری توجہ درکار ہے",
        "safe": False, "econ": "50-100% fruit loss if not controlled early"
    },
    "Grape___Esca_(Black_Measles)": {
        "en": "Esca (Black Measles)", "ur": "انگور کی خسرہ بیماری",
        "cause": "Fungal complex (Phaeomoniella, Phaeoacremonium)", "cause_ur": "کئی فنگسز مل کر یہ بیماری پیدا کرتی ہیں — پرانی بیلوں میں زیادہ ہوتی ہے۔",
        "sev": "High", "part": "Whole Vine",
        "symptoms": ["Tiger-stripe pattern on leaves (interveinal yellowing/browning)", "Fruit develops small dark spots (measles)", "Sudden vine collapse in severe apoplexy form"],
        "treatments": ["No complete cure — remove severely infected vines", "Apply sodium arsenite trunk injection where legal", "Protect pruning wounds with fungicide paste"],
        "prevention": ["Avoid pruning in wet weather", "Apply wound protectant (Trichoderma paste) immediately after pruning", "Remove and burn infected wood"],
        "ur_sum": "انگور میں خسرہ بیماری ہے جو پرانی بیلوں کو متاثر کرتی ہے۔ شدید متاثرہ بیلیں نکالیں اور کٹائی کے زخموں پر فنگسائیڈ لگائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں اقدامات کریں",
        "safe": False, "econ": "Can kill entire vines over several years"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "en": "Grape Leaf Blight", "ur": "انگور کا پتہ جھلساؤ",
        "cause": "Fungal (Pseudocercospora vitis)", "cause_ur": "فنگس — گرم اور نم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Irregular dark brown spots on older leaves", "Spots have yellow halo", "Premature defoliation in severe cases"],
        "treatments": ["Apply Mancozeb or Copper fungicide", "Remove and destroy infected leaves", "Spray every 10-14 days in humid conditions"],
        "prevention": ["Proper vine training for air circulation", "Avoid wetting foliage during irrigation", "Remove crop debris after harvest"],
        "ur_sum": "انگور کے پتوں میں جھلساؤ ہے۔ مینکوزیب فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss if severe"
    },
    "Grape___healthy": {
        "en": "Healthy Grape Vine", "ur": "صحت مند انگور کی بیل",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Proper pruning for airflow", "Balanced fertilization"],
        "ur_sum": "آپ کی انگور کی بیل صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "en": "Citrus Greening (HLB)", "ur": "مالٹے کی سبزی بیماری",
        "cause": "Bacterial (Candidatus Liberibacter asiaticus)", "cause_ur": "بیکٹیریا — سیلا کیڑے کے ذریعے پھیلتا ہے — کوئی علاج نہیں۔",
        "sev": "High", "part": "Whole Tree",
        "symptoms": ["Asymmetric yellowing of leaves (blotchy mottle)", "Fruit stays green and small even at maturity", "Fruit tastes bitter and drops early"],
        "treatments": ["NO CURE EXISTS — infected trees must be removed", "Control Asian Citrus Psyllid (vector) with Imidacloprid", "Report to local agriculture department immediately"],
        "prevention": ["Use certified disease-free nursery plants only", "Control psyllid population aggressively", "Inspect new plants before introducing to orchard"],
        "ur_sum": "یہ بہت خطرناک بیماری ہے جس کا کوئی علاج نہیں۔ متاثرہ درخت فوری کاٹ کر جلا دیں اور محکمہ زراعت کو اطلاع دیں۔",
        "urgency": "Immediate — Remove tree", "ur_urgency": "فوری — درخت کاٹ دیں",
        "safe": False, "econ": "Complete orchard loss over 5-10 years"
    },
    "Peach___Bacterial_spot": {
        "en": "Peach Bacterial Spot", "ur": "آڑو کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas arboricola pv. pruni)", "cause_ur": "بیکٹیریا — بارش اور ہوا سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Small water-soaked spots on leaves turning dark with yellow halo", "Spots fall out leaving shot-hole appearance", "Fruit develops sunken dark pits"],
        "treatments": ["Apply Copper-based bactericide (Copper hydroxide)", "Spray Oxytetracycline during bloom if available", "Avoid overhead irrigation"],
        "prevention": ["Plant resistant peach varieties", "Prune for good airflow", "Avoid wetting foliage"],
        "ur_sum": "آڑو میں بیکٹیریل دھبے ہیں۔ کاپر فنگسائیڈ اسپرے کریں اور اوپر سے پانی نہ دیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% fruit quality loss"
    },
    "Peach___healthy": {
        "en": "Healthy Peach Plant", "ur": "صحت مند آڑو کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Balanced fertilization", "Annual pruning for airflow"],
        "ur_sum": "آپ کا آڑو کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Pepper,_bell___Bacterial_spot": {
        "en": "Bell Pepper Bacterial Spot", "ur": "شملہ مرچ کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas euvesicatoria)", "cause_ur": "بیکٹیریا — بارش کے چھینٹوں سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Small water-soaked lesions on leaves turning dark brown", "Lesions with yellow halo giving shot-hole appearance", "Raised scab-like spots on fruit surface"],
        "treatments": ["Apply Copper hydroxide bactericide every 5-7 days", "Remove severely infected plant parts", "Avoid working in wet fields to reduce spread"],
        "prevention": ["Use certified disease-free seed", "Avoid overhead irrigation", "Practice 2-year crop rotation"],
        "ur_sum": "شملہ مرچ میں بیکٹیریل دھبے ہیں۔ کاپر بیکٹیریسائیڈ اسپرے کریں اور بیجوں کو ٹریٹ کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss if untreated"
    },
    "Pepper,_bell___healthy": {
        "en": "Healthy Bell Pepper Plant", "ur": "صحت مند شملہ مرچ کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Balanced fertilization", "Avoid waterlogging"],
        "ur_sum": "آپ کی شملہ مرچ کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Potato___Early_blight": {
        "en": "Potato Early Blight", "ur": "آلو کا ابتدائی جھلساؤ",
        "cause": "Fungal (Alternaria solani)", "cause_ur": "فنگس — گرم موسم میں پرانے پتوں پر پہلے آتی ہے۔",
        "sev": "Medium", "part": "Leaves & Stem",
        "symptoms": ["Dark brown spots with concentric rings (target board pattern)", "Yellow tissue surrounding the spots", "Lower and older leaves affected first"],
        "treatments": ["Apply Mancozeb 80WP at 2.5g per liter", "Spray Chlorothalonil every 7-10 days", "Remove infected lower leaves immediately"],
        "prevention": ["Crop rotation every 2-3 years", "Avoid wetting foliage during irrigation", "Adequate plant spacing for air circulation"],
        "ur_sum": "آلو میں ابتدائی جھلساؤ ہے۔ مینکوزیب فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss if untreated"
    },
    "Potato___Late_blight": {
        "en": "Potato Late Blight", "ur": "آلو کا جھلساؤ",
        "cause": "Fungal (Phytophthora infestans)", "cause_ur": "فنگس — نم اور ٹھنڈے موسم میں تیزی سے پھیلتی ہے۔ بہت خطرناک!",
        "sev": "High", "part": "Leaves, Stem & Tubers",
        "symptoms": ["Dark water-soaked lesions on leaf edges and tips", "White cottony fungal growth on leaf undersides in humid weather", "Tubers show reddish-brown rot that smells bad"],
        "treatments": ["Apply Cymoxanil + Mancozeb (Curzate M) immediately", "Spray every 5-7 days in wet weather", "Remove and bury infected plant material deep in soil"],
        "prevention": ["Use certified disease-free seed potatoes", "Avoid planting in low-lying or waterlogged areas", "Hill up soil around plants to protect tubers"],
        "ur_sum": "آلو میں جھلساؤ بیماری ہے — یہ بہت تیزی سے پھیلتی ہے۔ فوری کیوزیٹ ایم اسپرے کریں اور متاثرہ حصے مٹی میں دبا دیں۔",
        "urgency": "Immediate", "ur_urgency": "فوری اسپرے کریں — دیر نہ کریں",
        "safe": False, "econ": "Complete crop failure within 2 weeks if untreated"
    },
    "Potato___healthy": {
        "en": "Healthy Potato Plant", "ur": "صحت مند آلو کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring every week", "Balanced fertilization", "Proper hilling and drainage"],
        "ur_sum": "آپ کا آلو کا پودا صحت مند ہے۔ کوئی بیماری نہیں ملی۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Raspberry___healthy": {
        "en": "Healthy Raspberry Plant", "ur": "صحت مند رسبری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Proper pruning", "Balanced fertilization"],
        "ur_sum": "آپ کی رسبری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Soybean___healthy": {
        "en": "Healthy Soybean Plant", "ur": "صحت مند سویابین کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Crop rotation", "Balanced fertilization"],
        "ur_sum": "آپ کی سویابین کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Squash___Powdery_mildew": {
        "en": "Squash Powdery Mildew", "ur": "کدو کی سفید پھپھوندی",
        "cause": "Fungal (Podosphaera xanthii)", "cause_ur": "فنگس — خشک گرم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["White powdery coating on upper leaf surfaces", "Leaves turn yellow and brown", "Fruit development stunted in severe cases"],
        "treatments": ["Spray potassium bicarbonate or neem oil solution", "Apply Sulfur-based fungicide", "Remove severely infected leaves"],
        "prevention": ["Plant resistant varieties", "Avoid excessive nitrogen", "Space plants for good airflow"],
        "ur_sum": "کدو میں سفید پھپھوندی ہے۔ سلفر یا بائیکاربونیٹ اسپرے کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "10-20% yield loss"
    },
    "Strawberry___Leaf_scorch": {
        "en": "Strawberry Leaf Scorch", "ur": "اسٹرابیری کا پتہ جلاؤ",
        "cause": "Fungal (Diplocarpon earliana)", "cause_ur": "فنگس — نم اور گرم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Small dark purple spots on upper leaf surface", "Spots enlarge and coalesce turning leaves brown/scorched", "Severely affected leaves dry up and die"],
        "treatments": ["Apply Captan or Myclobutanil fungicide", "Remove and destroy infected leaves", "Avoid overhead irrigation"],
        "prevention": ["Plant certified disease-free runners", "Maintain good air circulation", "Remove old leaves after harvest"],
        "ur_sum": "اسٹرابیری کے پتوں میں جلاؤ بیماری ہے۔ کیپٹان فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% yield loss if untreated"
    },
    "Strawberry___healthy": {
        "en": "Healthy Strawberry Plant", "ur": "صحت مند اسٹرابیری کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Regular monitoring", "Proper drainage", "Balanced fertilization"],
        "ur_sum": "آپ کی اسٹرابیری کا پودا صحت مند ہے۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
    },
    "Tomato___Bacterial_spot": {
        "en": "Tomato Bacterial Spot", "ur": "ٹماٹر کے بیکٹیریل دھبے",
        "cause": "Bacterial (Xanthomonas vesicatoria)", "cause_ur": "بیکٹیریا — بارش اور ہوا سے پھیلتا ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Small water-soaked spots on leaves turning dark with yellow halo", "Shot-hole appearance as spots dry out", "Raised scab spots on green fruit"],
        "treatments": ["Apply Copper hydroxide bactericide every 5-7 days", "Remove infected leaves and plant debris", "Avoid overhead irrigation completely"],
        "prevention": ["Use certified disease-free seed", "2-year crop rotation", "Avoid working in wet fields"],
        "ur_sum": "ٹماٹر میں بیکٹیریل دھبے ہیں۔ کاپر فنگسائیڈ اسپرے کریں اور اوپر سے پانی نہ دیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% loss if untreated"
    },
    "Tomato___Early_blight": {
        "en": "Tomato Early Blight", "ur": "ٹماٹر کا ابتدائی جھلساؤ",
        "cause": "Fungal (Alternaria solani)", "cause_ur": "فنگس — گرم اور مرطوب موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Stem",
        "symptoms": ["Circular brown spots with concentric target-board rings", "Yellow halo surrounding the spots", "Lower/older leaves affected first"],
        "treatments": ["Apply Mancozeb 80WP at 2.5g/L every 7-10 days", "Spray Chlorothalonil as alternative", "Remove infected lower leaves immediately"],
        "prevention": ["Crop rotation every year", "Mulch around plants to prevent soil splash", "Space plants for proper airflow"],
        "ur_sum": "ٹماٹر میں ابتدائی جھلساؤ ہے — قابل علاج ہے۔ نیچے کے پتے ہٹائیں اور مینکوزیب اسپرے کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% yield loss if untreated"
    },
    "Tomato___Late_blight": {
        "en": "Tomato Late Blight", "ur": "ٹماٹر کا جھلساؤ",
        "cause": "Fungal (Phytophthora infestans)", "cause_ur": "فنگس — نم اور ٹھنڈے موسم میں تیزی سے پھیلتی ہے۔ بہت خطرناک!",
        "sev": "High", "part": "Leaves & Fruit",
        "symptoms": ["Dark brown water-soaked lesions on leaf edges", "White cottony mold on leaf undersides in humid weather", "Fruit turns dark brown and rots rapidly"],
        "treatments": ["Remove and destroy infected parts immediately", "Apply Copper-based fungicide (Kocide / Blue Shield)", "Spray Mancozeb 80WP at 2.5g/L every 7 days", "Avoid overhead irrigation — water at base only"],
        "prevention": ["Plant resistant varieties (e.g., Mountain Magic)", "Ensure good air circulation between plants", "Never work in field when plants are wet"],
        "ur_sum": "ٹماٹر میں جھلساؤ بیماری ہے — فوری توجہ ضروری ہے۔ متاثرہ پتے ہٹائیں اور کاپر فنگسائیڈ اسپرے کریں۔ دیر ہوئی تو پوری فصل تباہ ہو سکتی ہے۔",
        "urgency": "Immediate", "ur_urgency": "فوری اسپرے کریں — دیر نہ کریں",
        "safe": False, "econ": "70-100% loss if untreated within 1 week"
    },
    "Tomato___Leaf_Mold": {
        "en": "Tomato Leaf Mold", "ur": "ٹماٹر کی پتہ پھپھوندی",
        "cause": "Fungal (Passalora fulva)", "cause_ur": "فنگس — گرم اور زیادہ نمی والے ماحول میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Pale green-yellow spots on upper leaf surface", "Olive-green to brown velvety mold on undersides", "Leaves curl and drop in severe cases"],
        "treatments": ["Reduce humidity — improve greenhouse ventilation", "Apply Chlorothalonil or Mancozeb fungicide", "Remove infected leaves and destroy them"],
        "prevention": ["Maintain relative humidity below 85%", "Space plants properly for airflow", "Avoid wetting foliage"],
        "ur_sum": "ٹماٹر کے پتوں پر پھپھوندی ہے۔ نمی کم کریں اور فنگسائیڈ اسپرے کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-30% yield loss in severe cases"
    },
    "Tomato___Septoria_leaf_spot": {
        "en": "Septoria Leaf Spot", "ur": "ٹماٹر کے سیپٹوریا دھبے",
        "cause": "Fungal (Septoria lycopersici)", "cause_ur": "فنگس — بارش اور اوس میں تیزی سے پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Small circular spots with dark border and grey-white center", "Tiny black dots (pycnidia) visible inside spots", "Lower leaves yellow and drop first"],
        "treatments": ["Apply Chlorothalonil or Mancozeb fungicide every 7-10 days", "Remove infected leaves immediately", "Avoid wetting leaves during irrigation"],
        "prevention": ["Crop rotation — don't grow tomatoes in same spot twice", "Sanitize tools between plants", "Remove crop debris completely after season"],
        "ur_sum": "ٹماٹر میں سیپٹوریا دھبے ہیں۔ فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-30% loss if untreated"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "en": "Spider Mite Infestation", "ur": "ٹماٹر پر مکڑی کے چھوٹے کیڑے",
        "cause": "Pest (Tetranychus urticae)", "cause_ur": "کیڑا — خشک اور گرم موسم میں تیزی سے بڑھتا ہے۔",
        "sev": "Medium", "part": "Leaves",
        "symptoms": ["Tiny yellow/white stippling dots on upper leaf surface", "Fine webbing on leaf undersides", "Leaves turn bronze and dry up in severe cases"],
        "treatments": ["Apply Abamectin or Spiromesifen miticide", "Spray Neem oil solution (2%) as organic option", "Strong water spray on undersides to knock off mites"],
        "prevention": ["Maintain adequate soil moisture — mites prefer dry conditions", "Introduce predatory mites (Phytoseiulus) for biological control", "Avoid dusty conditions around plants"],
        "ur_sum": "ٹماٹر پر مکڑی کے کیڑے (چھوٹے) ہیں۔ ابامیکٹن اسپرے کریں یا نیم کا تیل استعمال کریں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "20-40% loss in severe infestations"
    },
    "Tomato___Target_Spot": {
        "en": "Tomato Target Spot", "ur": "ٹماٹر کا ہدف دھبہ",
        "cause": "Fungal (Corynespora cassiicola)", "cause_ur": "فنگس — گرم اور نم موسم میں پھیلتی ہے۔",
        "sev": "Medium", "part": "Leaves & Fruit",
        "symptoms": ["Brown spots with concentric rings (target pattern) on leaves", "Spots have yellow halo", "Dark sunken lesions on fruit surface"],
        "treatments": ["Apply Chlorothalonil or Azoxystrobin fungicide", "Remove infected leaves and fruit", "Spray every 7-14 days during humid weather"],
        "prevention": ["Maintain good plant spacing", "Avoid leaf wetness", "Crop rotation annually"],
        "ur_sum": "ٹماٹر میں ہدف دھبہ بیماری ہے۔ فنگسائیڈ اسپرے کریں اور متاثرہ پتے ہٹائیں۔",
        "urgency": "Within 1 week", "ur_urgency": "ایک ہفتے میں علاج کریں",
        "safe": True, "econ": "15-25% loss if untreated"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "en": "Yellow Leaf Curl Virus", "ur": "ٹماٹر کا پیلا پتہ وائرس",
        "cause": "Viral (TYLCV via Bemisia whitefly)", "cause_ur": "وائرس — سفید مکھی کے ذریعے پھیلتا ہے — کوئی علاج نہیں۔",
        "sev": "High", "part": "Whole Plant",
        "symptoms": ["Upward curling and yellowing of young leaves", "Severely stunted plant growth", "Little to no fruit production"],
        "treatments": ["NO CURE — remove and destroy infected plants immediately", "Control whitefly with Imidacloprid or Thiamethoxam", "Install yellow sticky traps to monitor whitefly"],
        "prevention": ["Plant virus-resistant tomato varieties (TYLCV-R)", "Use insect-proof net houses for seedlings", "Control whitefly population before transplanting"],
        "ur_sum": "ٹماٹر میں پیلا پتہ وائرس ہے — کوئی علاج نہیں۔ متاثرہ پودے فوری اکھاڑ کر جلا دیں اور سفید مکھی کنٹرول کریں۔",
        "urgency": "Immediate — Remove plants", "ur_urgency": "فوری — پودے اکھاڑیں",
        "safe": False, "econ": "Up to 100% loss in severe outbreaks"
    },
    "Tomato___Tomato_mosaic_virus": {
        "en": "Tomato Mosaic Virus", "ur": "ٹماٹر کا موزیک وائرس",
        "cause": "Viral (ToMV — contact transmitted)", "cause_ur": "وائرس — ہاتھوں، اوزاروں اور بیجوں سے پھیلتا ہے۔",
        "sev": "High", "part": "Whole Plant",
        "symptoms": ["Mosaic pattern of light and dark green on leaves", "Leaves distorted, wrinkled and cupped", "Fruit shows yellow mottling and uneven ripening"],
        "treatments": ["NO CURE — remove and destroy infected plants", "Wash hands thoroughly before handling plants", "Sterilize all tools with 10% bleach solution"],
        "prevention": ["Use virus-free certified seed", "Wash hands before entering field", "Control aphids which can spread the virus"],
        "ur_sum": "ٹماٹر میں موزیک وائرس ہے — کوئی علاج نہیں۔ متاثرہ پودے ہٹائیں، ہاتھ اور اوزار صاف کریں۔",
        "urgency": "Immediate — Remove plants", "ur_urgency": "فوری — متاثرہ پودے ہٹائیں",
        "safe": False, "econ": "20-70% yield loss depending on timing"
    },
    "Tomato___healthy": {
        "en": "Healthy Tomato Plant", "ur": "صحت مند ٹماٹر کا پودا",
        "cause": "None", "cause_ur": "کوئی بیماری نہیں ملی۔",
        "sev": "None", "part": "None", "symptoms": [], "treatments": [],
        "prevention": ["Monitor regularly every 3-4 days", "Maintain balanced NPK fertilization", "Stake plants and maintain airflow"],
        "ur_sum": "آپ کا ٹماٹر کا پودا بالکل صحت مند ہے۔ کوئی بیماری نہیں ملی۔ اسی طرح دیکھ بھال جاری رکھیں۔",
        "urgency": "No action needed", "ur_urgency": "کوئی ضرورت نہیں", "safe": True, "econ": "None"
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
    crop = parts[0].replace("_", " ") if len(parts) > 0 else "Crop"
    dis = parts[1].replace("_", " ") if len(parts) > 1 else label
    return {
        "en": "Healthy Plant" if healthy else dis,
        "ur": "صحت مند پودا" if healthy else dis,
        "cause": "None" if healthy else "Pathogen detected",
        "cause_ur": "کوئی بیماری نہیں۔" if healthy else "بیماری ملی — مقامی زراعت افسر سے رابطہ کریں۔",
        "sev": "None" if healthy else "Medium",
        "part": "None" if healthy else "Leaves",
        "symptoms": [],
        "treatments": [] if healthy else ["Consult your local agricultural extension officer (زراعت افسر)", "Collect a sample for laboratory testing", "Apply broad-spectrum fungicide as precaution"],
        "prevention": ["Regular monitoring", "Balanced fertilization", "Proper irrigation"],
        "ur_sum": f"{'آپ کا پودا صحت مند ہے۔' if healthy else 'پودا متاثر ہے۔ مقامی زراعت افسر سے مشورہ کریں۔'}",
        "urgency": "No action needed" if healthy else "Consult expert",
        "ur_urgency": "کوئی ضرورت نہیں" if healthy else "ماہر سے مشورہ کریں",
        "safe": True, "econ": "None" if healthy else "Monitor for spread"
    }

# ─── Model Loading ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    # NOTE: architecture below MUST exactly mirror the classifier used during
    # training (Cell 3), otherwise load_state_dict() will fail with a
    # size-mismatch / missing-key error. The trained checkpoint's classifier is:
    #   Dropout(0.3) -> Linear(1280, 512) -> ReLU -> Dropout(0.2) -> Linear(512, 38)
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(model.last_channel, 512),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(512, 38)
    )
    checkpoint = torch.load("fasalguard_model.pth", map_location="cpu")
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    with open("class_names.json") as f:
        class_names = json.load(f)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return model, transform, class_names

def predict(img_pil):
    try:
        model, transform, class_names = load_model()
        tensor = transform(img_pil.convert("RGB")).unsqueeze(0)
        with torch.no_grad():
            out = model(tensor)
            probs = torch.nn.functional.softmax(out, dim=1)
            conf, idx = torch.max(probs, 1)
        return class_names[idx.item()], round(conf.item() * 100)
    except Exception as e:
        return None, str(e)

# ─── Crops List ──────────────────────────────────────────────────────────────
CROPS = [
    "🍎 Apple (سیب)", "🫐 Blueberry (بلوبیری)", "🍒 Cherry (چیری)",
    "🌽 Corn / Maize (مکئی)", "🍇 Grape (انگور)", "🍊 Orange / Citrus (مالٹا)",
    "🍑 Peach (آڑو)", "🌶️ Bell Pepper (شملہ مرچ)", "🥔 Potato (آلو)",
    "🫐 Raspberry (رسبری)", "🫘 Soybean (سویابین)", "🥗 Squash (کدو)",
    "🍓 Strawberry (اسٹرابیری)", "🍅 Tomato (ٹماٹر)"
]

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🌾 AI-Powered &nbsp;·&nbsp; 100% Free &nbsp;·&nbsp; Pakistan</div>
    <h1 class="hero-title">Fasal<span>Guard</span></h1>
    <p class="hero-subtitle">Upload a photo of your crop leaf — get instant AI diagnosis and complete treatment plan</p>
    <p class="hero-urdu">اپنی فصل کی تصویر اپلوڈ کریں — فوری تشخیص اور علاج پائیں</p>
    <div class="stats-row">
        <div class="stat-item"><span class="stat-num">96.7%</span><span class="stat-label">AI Accuracy</span></div>
        <div class="stat-item"><span class="stat-num">38</span><span class="stat-label">Diseases</span></div>
        <div class="stat-item"><span class="stat-num">14</span><span class="stat-label">Crops</span></div>
        <div class="stat-item"><span class="stat-num">Free</span><span class="stat-label">Always</span></div>
        <div class="stat-item"><span class="stat-num">EN+UR</span><span class="stat-label">Bilingual</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<span class="section-label">Select Your Crop &nbsp;·&nbsp; فصل منتخب کریں</span>', unsafe_allow_html=True)
    crop_choice = st.selectbox("Crop", CROPS, label_visibility="collapsed")
    st.markdown('<span class="section-label" style="margin-top:1.2rem;display:block">Upload Leaf / Plant Photo &nbsp;·&nbsp; تصویر اپلوڈ کریں</span>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded:
        st.markdown('<span class="section-label" style="margin-top:0.8rem;display:block">Preview</span>', unsafe_allow_html=True)
        st.image(Image.open(uploaded), use_column_width=True, output_format="JPEG")

with col2:
    st.markdown("""
    <div class="how-card">
        <span class="section-label">How It Works &nbsp;·&nbsp; کیسے کام کرتا ہے</span>
        <div style="margin-top:0.8rem;">
            <div class="how-step"><div class="step-num">1</div><div><div class="step-en">Select your crop type</div><div class="step-ur">اپنی فصل چنیں</div></div></div>
            <div class="how-step"><div class="step-num">2</div><div><div class="step-en">Upload a clear leaf photo</div><div class="step-ur">پتے کی واضح تصویر اپلوڈ کریں</div></div></div>
            <div class="how-step"><div class="step-num">3</div><div><div class="step-en">Click Analyze — AI detects disease</div><div class="step-ur">تجزیہ کریں — AI بیماری پہچانے گا</div></div></div>
            <div class="how-step" style="margin-bottom:0;"><div class="step-num">4</div><div><div class="step-en">Follow the treatment plan</div><div class="step-ur">علاج پر عمل کریں</div></div></div>
        </div>
        <div class="photo-tips">
            <div class="tips-title">📸 Photo Tips for Best Results</div>
            <div class="tips-text">
                • Close-up of one affected leaf<br>
                • Natural daylight — avoid flash<br>
                • Clear, in-focus image<br>
                • Show the most affected area
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if uploaded:
    if st.button("🔬 Analyze My Crop &nbsp;·&nbsp; فصل کا تجزیہ کریں", use_container_width=True):
        uploaded.seek(0)
        img_pil = Image.open(uploaded).convert("RGB")
        with st.spinner("🔬 AI is analyzing your crop... فصل کا تجزیہ ہو رہا ہے"):
            label, confidence = predict(img_pil)

        if label is None:
            st.error(f"Analysis error: {confidence}. Please try again with a clearer image.")
        else:
            info = get_info(label)
            is_healthy = info["sev"] == "None"
            sev = info["sev"]
            sev_map = {"High": ("sev-high", "🔴"), "Medium": ("sev-medium", "🟡"), "Low": ("sev-low", "🟢"), "None": ("sev-none", "🟢")}
            sev_class, sev_icon = sev_map.get(sev, ("sev-low", "🟢"))

            if is_healthy:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-header">
                        <div style="flex:1;">
                            <div style="font-size:0.65rem;color:#4ade80;text-transform:uppercase;letter-spacing:1.2px;font-weight:700;margin-bottom:6px;">Diagnosis Result · تشخیص</div>
                            <div style="font-size:1.4rem;font-weight:700;color:#4ade80;">✓ {info['en']}</div>
                            <div style="font-size:0.95rem;color:#6b9f6b;margin-top:3px;">{info['ur']}</div>
                        </div>
                        <span class="severity-badge sev-none">🟢 No Disease</span>
                    </div>
                    <div class="result-body">
                        <div class="conf-bar-wrap">
                            <div class="conf-row"><span class="conf-label">AI Confidence</span><span class="conf-val">{confidence}%</span></div>
                            <div class="conf-bg"><div class="conf-fill" style="width:{confidence}%"></div></div>
                        </div>
                        <div class="healthy-banner">
                            <div style="font-size:2rem;margin-bottom:8px;">✅</div>
                            <div style="font-size:1rem;font-weight:600;color:#4ade80;margin-bottom:4px;">Your plant is healthy!</div>
                            <div style="font-size:0.85rem;color:#6b9f6b;">No signs of disease, pest damage, or nutrient deficiency detected.</div>
                        </div>
                        <hr class="divider">
                        <div class="list-section"><h4>Preventive Care · احتیاط</h4>
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
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-header">
                        <div style="flex:1;">
                            <div style="font-size:0.65rem;color:#4ade80;text-transform:uppercase;letter-spacing:1.2px;font-weight:700;margin-bottom:6px;">Diagnosis Result · تشخیص</div>
                            <div style="font-size:1.4rem;font-weight:700;color:#f0faf0;">{info['en']}</div>
                            <div style="font-size:1rem;color:#4ade80;margin-top:3px;">{info['ur']}</div>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end;">
                            <span class="severity-badge {sev_class}">{sev_icon} {sev} Severity</span>
                            <span style="font-size:0.72rem;color:#6b9f6b;white-space:nowrap;">{info['urgency']}</span>
                        </div>
                    </div>
                    <div class="result-body">
                        <div class="conf-bar-wrap">
                            <div class="conf-row"><span class="conf-label">AI Confidence</span><span class="conf-val">{confidence}%</span></div>
                            <div class="conf-bg"><div class="conf-fill" style="width:{confidence}%"></div></div>
                        </div>
                        <div class="info-grid">
                            <div class="info-block"><div class="ib-label">Affected Part</div><div class="ib-val">{info['part']}</div></div>
                            <div class="info-block"><div class="ib-label">Cause</div><div class="ib-val">{info['cause']}</div></div>
                            <div class="info-block"><div class="ib-label">Safe to Harvest?</div><div class="ib-val" style="color:{'#4ade80' if info['safe'] else '#f87171'}">{'✓ Yes' if info['safe'] else '✗ Not Recommended'}</div></div>
                            <div class="info-block"><div class="ib-label">Economic Risk</div><div class="ib-val" style="font-size:0.82rem;">{info['econ']}</div></div>
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
                    st.markdown('<hr class="divider"><div class="list-section"><h4>Prevention · بچاؤ کے طریقے</h4>', unsafe_allow_html=True)
                    for p in info['prevention']:
                        st.markdown(f'<div class="list-item"><div class="dot dot-blue"></div><div class="list-text">{p}</div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown(f"""
                        <div class="urdu-block">
                            <div class="urdu-title">اردو خلاصہ</div>
                            <div class="urdu-text">{info['cause_ur']}<br><br>{info['ur_sum']}<br><br><strong style="color:#4ade80">{info['ur_urgency']}</strong></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:4rem 1rem;">
        <div style="font-size:4rem;margin-bottom:1rem;opacity:0.35;">🌾</div>
        <div style="font-size:1.05rem;color:#4a6f4a;margin-bottom:0.4rem;font-weight:500;">Upload a crop photo to begin analysis</div>
        <div style="font-size:0.88rem;color:#3d5c3d;">تصویر اپلوڈ کریں اور شروع کریں</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-section">
    <div class="footer-text">
        <strong style="color:#4a6f4a;">FasalGuard</strong> &nbsp;·&nbsp; Pakistan's AI Crop Health Platform &nbsp;·&nbsp; پاکستان کا پہلا AI فصل صحت پلیٹ فارم<br>
        Trained on 70,000+ images &nbsp;·&nbsp; 96.7% Accuracy &nbsp;·&nbsp; 38 Disease Classes &nbsp;·&nbsp; 14 Crops<br><br>
        <span style="color:#2a4a2a;">⚠️ For serious outbreaks, always consult your local Agricultural Extension Officer (زراعت افسر)</span><br>
        <span style="color:#1a3a1a;font-size:0.68rem;margin-top:6px;display:block;">
            Powered by MobileNetV2 + PyTorch &nbsp;·&nbsp; 100% Free &nbsp;·&nbsp; No API Key &nbsp;·&nbsp; No Limits &nbsp;·&nbsp; Open Source
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
