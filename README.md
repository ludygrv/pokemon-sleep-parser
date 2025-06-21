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

# Sleep Session Result

### Windows
```bash
$IMGS = "D:\Personal\Jogos\PKMN_Sleep\Sample5\images"
$OUTPUT = "D:\Personal\Jogos\PKMN_Sleep\Sample5\session_result.csv"
python read_sleep_result_doc_tr.py --output $OUTPUT $IMGS
```
echo python read_sleep_result_doc_tr.py --output $OUTPUT $IMGS

# 🕹️ Next Steps
Here’s where we stopped and what you can do next:

 ✅ Confirm doctr OCR results on more screenshots

 📁 Add batch processing: load all screenshots from a folder

 📊 Save output to CSV or Excel

 🧠 (Optional) Improve OCR robustness for layout variations

 🖼️ (Optional) Visualize OCR detection boxes for debugging

 ### Connecting to Github:

git remote add origin https://github.com/ludygrv/pokemon-sleep-parser.git
with SSH
git remote add origin git@github.com:ludygrv/pokemon-sleep-parser.git

Change User:
git config user.name "Ludy17L"
git config user.email "ludy17ludy@gmail.com"

Failure to use "New" fine grained Token please try again with a classic one.

If necessary reset credential manager:

Steps to Manually Remove GitHub Credentials
Open Windows Credential Manager:

Press Win + S and type Credential Manager, then open it.
Go to "Windows Credentials" or "Generic Credentials":

Look for any entries related to github.com.
Remove GitHub Credentials:

Click on the entry (it may be called git:https://github.com or similar).
Click Remove.
Restart VS Code or your terminal.

Try pushing again: