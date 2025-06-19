import re
from PIL import Image
import pytesseract
from datetime import datetime
import os
import json

def extract_sleep_research_info(image_path):
    # Extract date from filename (format: Screenshot_YYYY-MM-DD-HH-MM-SS-xxx_...)
    filename = os.path.basename(image_path)
    date_match = re.search(r"Screenshot_(\d{4}-\d{2}-\d{2})", filename)
    date = date_match.group(1) if date_match else "Unknown"

    # OCR on the image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Print all text boxes found by the OCR
    print(f"OCR Text from {image_path}:\n{text}\n")
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(ocr_data['level'])
    for i in range(n_boxes):
        if ocr_data['text'][i].strip():
            print(f"Box {i}: '{ocr_data['text'][i]}' at (left={ocr_data['left'][i]}, top={ocr_data['top'][i]}, width={ocr_data['width'][i]}, height={ocr_data['height'][i]})")
    
    # Extract relevant data using regex
    pokemon_seen = re.search(r'Pokémon Seen\s*(\d+)', text)
    research_exp = re.search(r'Research EXP\s*[^0-9]*(\d+)', text)
    multiplier = re.search(r'Bonus\s*x?([0-9.]+)', text)

    #dream_shards = re.search(r'Dream Shards\s*[^0-9]*(\d+)', text)

    # Extract Dream Shards using a more flexible pattern that tolerates noise and commas
    dream_shards_match = re.search(r'Dream Shards[^\d]*(\d[\d,]*)', text)
    dream_shards = int(dream_shards_match.group(1).replace(',', '')) if dream_shards_match else None

    return {
        "date": date,
        "pokemon_seen": int(pokemon_seen.group(1)) if pokemon_seen else None,
        "research_exp": int(research_exp.group(1)) if research_exp else None,
        "exp_multiplier": float(multiplier.group(1)) if multiplier else None,
        "dream_shards": dream_shards
    }

# Example usaged:

# image_path = "/mnt/data/Screenshot_2025-05-07-06-42-56-721_jp.pokemon.pokemonsleep.jpg"
image_path = r"\Personal\Jogos\PKMN_Sleep\Photos-1-001\Screenshot_2025-05-03-06-56-37-980_jp.pokemon.pokemonsleep.jpg"
result = extract_sleep_research_info(image_path)
print(json.dumps(result, indent=2))
