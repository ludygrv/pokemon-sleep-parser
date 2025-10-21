import argparse
import csv
import os
import re
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def get_report_info(extracted_text):
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

def get_session_info(extracted_text):
    # Extract fields
    date_match = re.search(r'([A-Za-z]+,?\s+[A-Za-z]+\s+\d{1,2},\s+\d{4})', extracted_text)
    session_match = re.search(r'Session\s*(\d+)', extracted_text)

    # Extract all numbers in order (remove commas)
    all_numbers = [int(n.replace(',', '')) for n in re.findall(r'\d[\d,]*', extracted_text)]

    print(f"Extracted numbers: {all_numbers}")
    
    # Apply heuristics to classify values
    drowsy_power = all_numbers[3]  # next((n for n in all_numbers if n > 1_000_000), None)
    snorlax_strength = all_numbers[4] # next((n for n in all_numbers if 10_000 < n < 1_000_000), None)
    sleep_score = all_numbers[5] # 
    
    if drowsy_power < 100_000 or snorlax_strength < 1_000 or sleep_score < 50 or sleep_score > 150:
        print(f"Warning! Invalid values detected: drowsy_power={drowsy_power}, snorlax_strength={snorlax_strength}, sleep_score={sleep_score}")
            

    return {
        "image_type": "Session",
        "date": date_match.group(1) if date_match else None,
        "session_number": int(session_match.group(1)) if session_match else None,
        "drowsy_power": drowsy_power,
        "snorlax_strength": snorlax_strength,
        "sleep_score": sleep_score,
        "raw_text": extracted_text,
        "status": "OK" if drowsy_power and snorlax_strength and sleep_score else "Incomplete"
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
        fields = get_report_info(extracted_text)
        return {
            "image_type": "Report",
            "date": date,
            **fields,
            "raw_text": extracted_text,
            "status": "OK"
        }
    elif "Session" in extracted_text:
        fields = get_session_info(extracted_text)
        return {
            "image_type": "Session",
            **fields,
            "status": "OK"
        }
    else:
        return {
            "image_type": "Unknown",
            "status": "Error"
        }

def get_image_files(folder):
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def main():
    parser = argparse.ArgumentParser(description="Extract PKMN Sleep session data from screenshots using OCR.")
    parser.add_argument("folder", help="Folder containing screenshot images")
    parser.add_argument("output", help="Directory to save output")
    args = parser.parse_args()

    image_files = get_image_files(args.folder)

    # Create output directory if it doesn't exist
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    report_csv = os.path.join(output_dir, "report_info.csv")
    session_csv = os.path.join(output_dir, "session_info.csv")
    unknown_csv = os.path.join(output_dir, "unknown_images.csv")

    # Check for already processed images in existing CSVs
    processed_images = set()
    for csv_file, image_key in [(report_csv, "report_image"),
                                (session_csv, "session_image"),
                                (unknown_csv, "unknown_image")]:
        if os.path.exists(csv_file):
            with open(csv_file, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get(image_key):
                        processed_images.add(row[image_key])

    # Filter out images that have already been processed
    total_images = len(image_files)
    image_files = [img for img in image_files if os.path.basename(img) not in processed_images]
    already_processed = total_images - len(image_files)
    to_process = len(image_files)
    print(f"Found {total_images} images. {already_processed} already processed, {to_process} to process.")
    
    report_results = []
    session_results = []
    # Collect unknown image filenames for later saving
    unknown_images = []

    for img_path in image_files:
        info = extract_info_with_doctr(img_path)
        
        if info["image_type"] == "Report":
            print(f"Report data extracted from {img_path}: {info}")
            report_results.append({
                "report_image": os.path.basename(img_path),
                **info,            
            })
        elif info["image_type"] == "Session":
            print(f"Session data extracted from {img_path}: {info}")
            session_results.append({
                "session_image": os.path.basename(img_path),
                **info,            
            })
        elif info["image_type"] == "Unknown":
            print(f"Skipping {img_path}: Unknown Image")
            unknown_images.append(os.path.basename(img_path))
            continue
        else:
            print(f"Warning! Image with invalid image_type ({info['image_type']}) Status={info['status']}")

    # Save report results
    report_exists = os.path.exists(report_csv)
    with open(report_csv, "a", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["date", "pokemon_seen", "research_exp", "exp_multiplier", "dream_shards", "report_image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not report_exists:
            writer.writeheader()
        for row in report_results:
            filtered_row = {key: row.get(key) for key in fieldnames}
            writer.writerow(filtered_row)

    # Save session results
    session_exists = os.path.exists(report_csv)
    with open(session_csv, "a", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["date", "session_number", "drowsy_power", "snorlax_strength", "sleep_score", "session_image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not session_exists:
            writer.writeheader()
        for row in session_results:
            filtered_row = {key: row.get(key) for key in fieldnames}
            writer.writerow(filtered_row)

    # Save unknown images to a CSV for skipping in future runs
    if unknown_images:
        unknown_exists = os.path.exists(unknown_csv)
        with open(unknown_csv, "a", newline='', encoding="utf-8") as csvfile:
            fieldnames = ["unknown_image"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not unknown_exists:
                writer.writeheader()
            for img in unknown_images:
                writer.writerow({"unknown_image": img})


    print(f"Extraction complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()
