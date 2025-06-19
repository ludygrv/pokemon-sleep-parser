from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
import os

def extract_info_with_doctr(image_path):
    # Load model
    model = ocr_predictor(pretrained=True)

    # Load image
    doc = DocumentFile.from_images(image_path)

    # Perform OCR
    result = model(doc)
    extracted_text = result.render()

    # Extract date from filename
    filename = os.path.basename(image_path)
    date_match = re.search(r"Screenshot_(\d{4}-\d{2}-\d{2})", filename)
    date = date_match.group(1) if date_match else "Unknown"

    # Use regex to extract values
    pokemon_seen = re.search(r'Pokémon Seen\s*(\d+)', extracted_text)
    research_exp = re.search(r'Research EXP\s*(\d+)', extracted_text)
    multiplier = re.search(r'Bonus\s*x?([0-9.]+)', extracted_text)
    dream_shards = re.search(r'Dream Shards\s*([0-9,]+)', extracted_text)

    return {
        "date": date,
        "pokemon_seen": int(pokemon_seen.group(1)) if pokemon_seen else None,
        "research_exp": int(research_exp.group(1)) if research_exp else None,
        "exp_multiplier": float(multiplier.group(1)) if multiplier else None,
        "dream_shards": int(dream_shards.group(1).replace(',', '')) if dream_shards else None,
        "raw_text": extracted_text
    }

# Example usage:
image_path = r"\Personal\Jogos\PKMN_Sleep\Photos-1-001\Screenshot_2025-05-03-06-56-37-980_jp.pokemon.pokemonsleep.jpg"
info = extract_info_with_doctr(image_path)
print(info)
