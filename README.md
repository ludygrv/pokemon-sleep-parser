# Pokémon Sleep Research Screenshot Parser

This project extracts structured data from Pokémon Sleep "Sleep Research Results" screenshots using OCR. It aims to automate the process of tracking and analyzing your sleep-related game data.

---

## ✅ Current Features

### 1. Extracted Information
From each screenshot, the script extracts:
- 📅 `Date`: from the filename (e.g., `Screenshot_2025-05-03-...`)
- 🔍 `Pokémon Seen`
- 🔬 `Research EXP`
- ✨ `EXP Multiplier` (e.g., Bonus x1.09)
- 💎 `Dream Shards` (handles values like "1,117")

### 2. OCR Approaches
- **`pytesseract` (Tesseract OCR)** was initially used.
- We later upgraded to **`doctr`**, a more accurate deep learning-based OCR tool.

---

## 📦 Dependencies

### If using `pytesseract`
```bash
pip install pytesseract pillow
sudo apt install tesseract-ocr  # or install via Windows installer
```
### If using `doc_tr`
```bash
pip install python-doctr[torch]
```
# 🕹️ Next Steps
Here’s where we stopped and what you can do next:

 ✅ Confirm doctr OCR results on more screenshots

 📁 Add batch processing: load all screenshots from a folder

 📊 Save output to CSV or Excel

 🧠 (Optional) Improve OCR robustness for layout variations

 🖼️ (Optional) Visualize OCR detection boxes for debugging