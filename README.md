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
$OUTPUT = "D:\Personal\Jogos\PKMN_Sleep\Sample5\OCR_extract"
python .\read_report_session_info.py $IMGS $OUTPUT 
```

### Plot the graph
```bash
$DATA = "D:\Personal\Jogos\PKMN_Sleep\Sample5\OCR_extract"
python plot_drowsy_power.py $DATA
```


### Debug Evidence
Finally have a code that works for 2 image types and expands previous runs!

```bash
PS D:\Personal\Jogos\PKMN_Sleep\PKMN_Sleep_Code> python read_sleep_result_doc_tr.py $IMGS $OUTPUT 
Found 5 images. 4 already processed, 1 to process.
Skipping D:\Personal\Jogos\PKMN_Sleep\Sample5\images\Screenshot_2025-05-05-06-49-59-085_jp.pokemon.pokemonsleep.jpg: Unknown Image
Extraction complete. Results saved to D:\Personal\Jogos\PKMN_Sleep\Sample5\OCR_extract
PS D:\Personal\Jogos\PKMN_Sleep\PKMN_Sleep_Code> python read_sleep_result_doc_tr.py $IMGS $OUTPUT 
Found 5 images. 5 already processed, 0 to process.
Extraction complete. Results saved to D:\Personal\Jogos\PKMN_Sleep\Sample5\OCR_extract
PS D:\Personal\Jogos\PKMN_Sleep\PKMN_Sleep_Code> 
```
# 🕹️ Next Steps
Here’s where we stopped and what you can do next:

Issues:
1 - OCR seesm to be wrong in some instances
2 - "date" on report and on session are off-by-one
3 - Verify Graph is logical
4 - Include Current Rank Info
5 - Adjust the effect of Multipliers (Research Exp Bonus or Events)
6 - Plot Newfound pokemon Lvl x Rank
🖼️ (Optional) Visualize OCR detection boxes for debugging
N - Auto Retrieve new images from Photos?

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