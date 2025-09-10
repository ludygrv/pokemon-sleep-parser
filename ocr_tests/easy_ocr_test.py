import easyocr
import time
import torch
import pandas as pd
import os
import pickle
import cv2
import numpy as np
min_conf = 0.3  # Minimum confidence to consider a word valid
height_gap = 140  # Max vertical gap to consider words in the same row

###########################################
# EasyOCR-based OCR and parsing for Pokémon Sleep community research screenshots
def test_gpu():
    print("Testing GPU availability for EasyOCR")
    print("EasyOCR version:", easyocr.__version__)
    print("Torch version:", torch.__version__)
    print("CUDA version:", torch.version.cuda)   # CUDA version PyTorch was built with
    print("Is CUDA available:", torch.cuda.is_available())

## OCR Processing
def ocr_image_with_easyocr(img):
    reader = easyocr.Reader(['en'], gpu=True)  # gpu=True if you have CUDA
    results = reader.readtext(img)
    return results

def print_ocr_results(ocr_results):
    print("OCR Results:")
    for bbox, text, conf in ocr_results:
        bbox_str = ", ".join([f"({int(x)},{int(y)})" for x, y in bbox])
        print(f" BBox: {bbox_str}, Text: '{text}', Conf: {conf:.2f}")

def draw_bboxes_on_image(image_path, ocr_results, output_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not load image: {image_path}")
        return

    for bbox, text, conf in ocr_results:
        # Convert bbox to integer coordinates
        pts = [(int(x), int(y)) for x, y in bbox]
        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # Draw bounding box
        cv2.polylines(image, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
        # Put text (in red)
        x, y = pts[0][0]
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imwrite(output_path, image)
    print(f"Overlay image saved to: {output_path}")

# ---------------------------
# Parsing logic
# ---------------------------
# ---------------------------
# Step 2: Simple cleanup dictionary
# ---------------------------
fix_map = {
    "Sleepl": "Sleep",
    "Sieep": "Sleep",
    "Emper": "Ember",
    "Sleepl": "Sleep",
    "Sllep": "Sleep"
}

def clean_text(t):
    for wrong, right in fix_map.items():
        t = t.replace(wrong, right)
    return t.strip(" !?")

def group_into_rows(ocr_results, row_threshold=height_gap):
    """
    Group OCR tokens into rows based on vertical alignment.
    Each result is (bbox, text, conf) where bbox=(x,y).
    """
    # Add vertical center for better alignment
    results = [(bbox, text) for bbox, text, conf in ocr_results if conf > min_conf]
    
    # Sort by vertical center, then by x
    results.sort(key=lambda x: (x[0][1], x[0][0]))

    rows = []
    current_row = []
    row_start_y = None

    for bbox, text in results:
        if row_start_y is None or abs(bbox[1] - row_start_y) > row_threshold:
            if current_row:
                # Save finished row
                current_row.sort(key=lambda x: x[0][0])  # sort row left-to-right
                rows.append(current_row)
                current_row = []
            current_row.append((bbox, text))
            row_start_y = bbox[1]
        else:
            current_row.append((bbox, text))

    if current_row:
        current_row.sort(key=lambda x: x[0][0])
        rows.append(current_row)

    return rows

def parse_rows_to_table(rows):
    """
    Convert grouped OCR rows into structured table: Username, Studied, Reward.
    """
    parsed = []
    for row in rows:
        texts = [t for _, t in row if t]  # filter out empty strings

        username, pokemon, style, reward = None, None, None, None
        friend_level = "5"  # Default friend level
        for t in texts:
            if t == "+1":
                friend_level = "0 to 4"
                continue
            elif "Reward" in t:
                continue
            elif "studied" in t:
                pokemon = t.split("studied")[1].strip()
                if pokemon.endswith("'s"):
                    pokemon = pokemon[:-2].strip()
            elif "Sleep" in t:
                style = t.split("Sleep")[0].strip()
            elif t.isdigit():
                reward = t
            else:
                username = t if username is None else username

        if reward is None:
            reward = 1  # Default reward if not found

        if username and pokemon and style and reward and friend_level:
            parsed.append([username, pokemon, style, reward, friend_level])
            print(f"Parsed row: Username={username}, Pokemon={pokemon}, Style={style}, Reward={reward}, Friend Level={friend_level}")
        else:
            print(f"Could not fully parse row: {texts}")

    return pd.DataFrame(parsed, columns=["Username", "Pokemon", "Sleep_Style", "Reward", "Friend_Level"])

def convert_bbox_format(bbox, debug=False):
    # Convert bbox from ((x0,y0),(x0,y1),(x1,y0),(x1,y1)) to (x0,y0,x1,y1)
    if debug:
        print("Converting bbox format")
        print(f" Original bbox: {bbox}")

    x0 = int(min([pt[0] for pt in bbox]))
    y0 = int(min([pt[1] for pt in bbox]))
    x1 = int(max([pt[0] for pt in bbox]))
    y1 = int(max([pt[1] for pt in bbox]))
    new_bbox = ((x0+x1)/2, (y0+y1)/2)

    if debug:
        print(f" Converted bbox: (x,y) = {new_bbox}")

    return new_bbox

def parse_ocr_result(ocr_results):
    rows = []
    current_user = None
    current_study = []
    reward = None

    # Convert bbox from ((x0,y0),(x0,y1),(x1,y0),(x1,y1)) to , bbox=(x0,y0,x1,y1).
    ocr_results = [
        (
            convert_bbox_format(bbox),
            clean_text(text),
            conf
        )
        for bbox, text, conf in ocr_results
    ]

    rows = group_into_rows(ocr_results)
    print(f"Grouped into {len(rows)} rows based on vertical alignment.")
    print("Rows detail (bbox midpoints and texts):")
    for i, row in enumerate(rows):
        print(f" Row {i}: {row}")

    # ---------------------------
    # Step 4: Parse each row into Username / Studied / Reward
    # ---------------------------
    df = parse_rows_to_table(rows)

    return df

if __name__ == "__main__":
    start_time = time.time()
    # test_gpu()

    image_folder = "d:\\Personal\\Jogos\\PKMN_Sleep\\photos\\2025_08_01_to_09_09\\"
    img = "Screenshot_2025-09-05-15-18-29-711_jp.pokemon.pokemonsleep.jpg"
    img_path = os.path.join(image_folder, img)
    ocr_result_folder = "d:\\Personal\\Jogos\\PKMN_Sleep\\ocr_extracts\\"
    if not os.path.exists(ocr_result_folder):
        os.makedirs(ocr_result_folder)

    print(f"Processing image: {img}")
    ocr_cache_file = ocr_result_folder + img + ".easyocr.pkl"
    if os.path.exists(ocr_cache_file):
        print(f"Loading OCR results from cache: {ocr_cache_file}")
        with open(ocr_cache_file, "rb") as f:
            results = pickle.load(f)
        ocr_completed_time = time.time()
        print(f"OCR Load time: {ocr_completed_time - start_time:.2f} seconds")
    else:
        results = ocr_image_with_easyocr(img_path)
        with open(ocr_cache_file, "wb") as f:
            pickle.dump(results, f)
        print(f"OCR results saved to cache: {ocr_cache_file}")
        ocr_completed_time = time.time()
        print(f"Total OCR time: {ocr_completed_time - start_time:.2f} seconds")

    print_ocr_results(results)
    overlay_path = os.path.join(ocr_result_folder, f"{img}_overlay.jpg")
    draw_bboxes_on_image(img_path, results, overlay_path)

    ocr_csv_file = os.path.join(ocr_result_folder, f"{img}_ocr_result.csv")
    if os.path.exists(ocr_csv_file):
        print(f"Loading extracted info from CSV: {ocr_csv_file}")
        extracted_info_df = pd.read_csv(ocr_csv_file)
    else:
        extracted_info_df = parse_ocr_result(results)
        extracted_info_df.to_csv(ocr_csv_file, index=False)
        print(f"Extracted info saved to CSV: {ocr_csv_file}")

    print(f"Text formatting time: {time.time() - ocr_completed_time:.2f} seconds")
    
    print(extracted_info_df)