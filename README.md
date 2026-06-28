# 🌾 FasalGuard — AI Crop Disease Detector

> **Pakistan's first self-contained AI crop health platform.**
> Upload a leaf photo → get instant diagnosis in English + Urdu → complete treatment plan.
> **No API key. No login. No limits. 100% Free. Forever.**

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Accuracy-96.7%25-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Diseases-38-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Crops-14-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Cost-FREE-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Language-EN%20%2B%20UR-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/API%20Key-NOT%20REQUIRED-brightgreen?style=for-the-badge"/>
</p>

---

## 🚀 Live Demo

**🌐 [fasalguard.onrender.com](https://fasalguard.onrender.com)**

> Open on any device — phone, tablet, computer. No login. No signup. Completely free.

---

## 🎯 The Problem We Solve

Pakistan's agriculture employs **42% of the workforce** and contributes **26% of GDP**.
Farmers lose **20–70% of their crop** to diseases they cannot identify in time.
No free, accessible, Urdu-language crop disease tool exists in Pakistan.

**FasalGuard changes that.**

A farmer with any smartphone can now diagnose crop disease in under 30 seconds — for free.

---

## ✨ What FasalGuard Does

Upload a photo of your crop leaf → FasalGuard's AI model instantly returns:

| Output | Detail |
|--------|--------|
| 🔬 Disease Name | English + Urdu |
| 📊 AI Confidence | Percentage bar |
| 🔴 Severity Level | High / Medium / Low / None |
| 🌿 Affected Part | Leaves / Fruit / Stem / Whole Plant |
| 🧫 Cause | Fungal / Bacterial / Viral / Pest |
| 💊 Treatment Plan | Step-by-step with locally available products |
| 🛡️ Prevention Tips | How to avoid next season |
| ✅ Harvest Safe? | Yes / No |
| 💰 Economic Risk | Estimated yield loss if untreated |
| 🇵🇰 Urdu Summary | Complete diagnosis in Urdu for farmers |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| AI Model | MobileNetV2 (Transfer Learning) |
| Training Dataset | PlantVillage — 70,000+ images |
| Training Framework | PyTorch |
| Model Accuracy | **96.7% on validation set** |
| Frontend | Streamlit |
| Image Processing | Pillow |
| Hosting | Render.com (Free Tier) |
| Languages | English + Urdu (Bilingual) |
| API Keys Required | **None** |
| Cost to Users | **Zero — Forever** |

---

## 🌱 Supported Crops & Diseases (38 Classes)

| Crop | Diseases Detected |
|------|-------------------|
| 🍎 Apple | Apple Scab, Black Rot, Cedar Rust, Healthy |
| 🫐 Blueberry | Healthy |
| 🍒 Cherry | Powdery Mildew, Healthy |
| 🌽 Corn / Maize | Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| 🍇 Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| 🍊 Orange | Citrus Greening (HLB) |
| 🍑 Peach | Bacterial Spot, Healthy |
| 🌶️ Bell Pepper | Bacterial Spot, Healthy |
| 🥔 Potato | Early Blight, Late Blight, Healthy |
| 🫐 Raspberry | Healthy |
| 🫘 Soybean | Healthy |
| 🥗 Squash | Powdery Mildew |
| 🍓 Strawberry | Leaf Scorch, Healthy |
| 🍅 Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

---

## 📂 Project Structure

```
fasalguard/
├── app.py                    # Complete Streamlit application (808 lines)
├── fasalguard_model.pth      # Trained MobileNetV2 model (9MB)
├── class_names.json          # 38 class labels
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # Dark green theme configuration
└── README.md                 # This file
```

---

## ⚙️ How the AI Works

```
Farmer uploads leaf photo
        ↓
Image resized to 224×224 pixels
        ↓
Normalized with ImageNet mean/std
        ↓
MobileNetV2 forward pass (CPU inference ~2-3 sec)
        ↓
Softmax → Top prediction + confidence score
        ↓
Disease info looked up from expert knowledge base
        ↓
English + Urdu result displayed instantly
```

**Model Architecture:** MobileNetV2 pretrained on ImageNet → fine-tuned classifier head on PlantVillage dataset (70,295 training images, 17,572 validation images) for 10 epochs using Transfer Learning.

**Why MobileNetV2?**
- Fast CPU inference (2-3 seconds — no GPU needed)
- Small model size (9MB — fits in GitHub repo)
- 96.7% validation accuracy
- Designed for mobile/edge deployment

---

## 🚀 Deploy Your Own Instance (Free)

### Prerequisites
- GitHub account (free)
- Render.com account (free)
- That's it — no credit card, no API keys

### Step 1 — Fork / Upload to GitHub
```bash
# Clone this repo
git clone https://github.com/SyedMinhal570/fasalguard.git

# Or upload files manually on github.com → New Repository
```

Upload all files including `fasalguard_model.pth` and `class_names.json`.

### Step 2 — Deploy on Render.com

1. Go to **render.com** → Sign up with GitHub
2. Click **New +** → **Web Service**
3. Connect your `fasalguard` GitHub repository
4. Set these values:

| Setting | Value |
|---------|-------|
| **Name** | fasalguard |
| **Region** | Singapore (closest to Pakistan) |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |
| **Instance Type** | Free |

5. Click **Create Web Service**
6. Wait 3-5 minutes → your live URL is ready ✅

> **Keep app awake 24/7 (free):** Sign up at [uptimerobot.com](https://uptimerobot.com) → Add HTTP monitor → paste your Render URL → set interval to 14 minutes. Done.

---

## 💻 Run Locally

```bash
# Clone the repository
git clone https://github.com/SyedMinhal570/fasalguard.git
cd fasalguard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

> **Requirements:** Python 3.11, ~1GB RAM, no GPU needed.

---

## 📸 Photo Tips for Best Accuracy

| ✅ Do | ❌ Avoid |
|-------|---------|
| Close-up of one affected leaf | Whole plant far away |
| Natural daylight | Flash or artificial light |
| Clear, in-focus image | Blurry or shaky photo |
| Show the most affected area | Healthy parts only |
| Plain background if possible | Cluttered background |

---

## 🔬 Model Training Details

| Parameter | Value |
|-----------|-------|
| Base Model | MobileNetV2 (ImageNet pretrained) |
| Dataset | PlantVillage (Augmented) |
| Train Images | 70,295 |
| Validation Images | 17,572 |
| Classes | 38 |
| Epochs | 10 |
| Batch Size | 64 |
| Optimizer | Adam (lr=0.001) |
| Scheduler | StepLR (step=5, gamma=0.5) |
| Final Val Accuracy | **96.7%** |
| Training Platform | Google Colab (T4 GPU) |
| Training Time | ~68 minutes |

---

## 🗺️ Future Roadmap

- [ ] Mobile app (Flutter) — direct camera capture
- [ ] Offline mode (TFLite) — works without internet
- [ ] WhatsApp Bot — farmer sends photo, gets diagnosis
- [ ] Voice output in Urdu — for illiterate farmers
- [ ] More Pakistani crops — Wheat, Cotton, Sugarcane
- [ ] Disease spread map — community reporting
- [ ] Weather-based disease alerts

---

## ⚠️ Disclaimer

FasalGuard provides AI-based guidance only. For serious crop disease outbreaks, always consult your local **Agricultural Extension Officer (زراعت افسر)**. AI diagnosis should complement, not replace, expert agronomic advice.

---

## 👨‍💻 Built By

**Syed Minhal** — Computer Engineering Student, ITU Lahore (Batch CE24, Graduating 2028)

[![GitHub](https://img.shields.io/badge/GitHub-SyedMinhal570-black?style=flat-square&logo=github)](https://github.com/SyedMinhal570)

---

## 🇵🇰 Impact

> Pakistan's agriculture employs 42% of the workforce and contributes 26% of GDP.
> Early disease detection prevents up to 70% crop loss.
> FasalGuard makes expert-level AI diagnosis free and accessible to every farmer with a smartphone.

---

*Built with ❤️ for Pakistani farmers · پاکستانی کسانوں کے لیے بنایا گیا*
