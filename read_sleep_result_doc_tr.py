import argparse
import csv
import os
import re
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def extract_fields_from_text(extracted_text):
    # Use regex to extract values
    pokemon_seen = re.search(r'Pokémon Seen\s*(\d+)', extracted_text)
    research_exp = re.search(r'Research EXP[^\d]*([0-9,]+)', extracted_text)
    multiplier = re.search(r'Bonus\s*x?([0-9.]+)', extracted_text)
    dream_shards = re.search(r'Dream Shards[^\d]*([0-9,]+)', extracted_text)
    return {
        "pokemon_seen": int(pokemon_seen.group(1)) if pokemon_seen else None,
        "research_exp": int(research_exp.group(1).replace(',', '')) if research_exp else None,
        "exp_multiplier": float(multiplier.group(1)) if multiplier else None,
        "dream_shards": int(dream_shards.group(1).replace(',', '')) if dream_shards else None,
    }

def extract_info_with_doctr(image_path):
    model = ocr_predictor(pretrained=True)
    doc = DocumentFile.from_images(image_path)
    result = model(doc)
    extracted_text = result.render()

    # Extract date from filename
    filename = os.path.basename(image_path)
    date_match = re.search(r"Screenshot_(\d{4}-\d{2}-\d{2})", filename)
    date = date_match.group(1) if date_match else "Unknown"

    if "Sleep Research Result" in extracted_text:
        fields = extract_fields_from_text(extracted_text)
        return {
            "date": date,
            **fields,
            "raw_text": extracted_text,
            "status": "OK"
        }
    else:
        return {
            "date": date,
            "pokemon_seen": None,
            "research_exp": None,
            "exp_multiplier": None,
            "dream_shards": None,
            "raw_text": extracted_text,
            "status": "Unknown Image"
        }

def get_image_files(folder):
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def main():
    parser = argparse.ArgumentParser(description="Extract PKMN Sleep session data from screenshots using OCR.")
    parser.add_argument("folder", help="Folder containing screenshot images")
    parser.add_argument("--output", default="sleep_results.csv", help="Output CSV file")
    args = parser.parse_args()

    image_files = get_image_files(args.folder)
    results = []

    print(f"Processing {len(image_files)} images...")
    for img_path in image_files:
        info = extract_info_with_doctr(img_path)
        if info["status"] == "Unknown Image":
            print(f"Skipping {img_path}: Unknown Image")
            continue
        results.append({
            "date": info["date"],
            "pokemon_seen": info["pokemon_seen"],
            "research_exp": info["research_exp"],
            "exp_multiplier": info["exp_multiplier"],
            "dream_shards": info["dream_shards"],
            "image": os.path.basename(img_path)
        })

    with open(args.output, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["date", "pokemon_seen", "research_exp", "exp_multiplier", "dream_shards", "image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Extraction complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()
