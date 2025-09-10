import cv2
import pytesseract
import pandas as pd
from PIL import Image

# Path to your screenshot
image_path = "d:\\Personal\\Jogos\\PKMN_Sleep\\photos\\2025_08_01_to_09_09\\Screenshot_2025-09-05-15-18-29-711_jp.pokemon.pokemonsleep.jpg"

# Load image
img = cv2.imread(image_path)

# Optional: preprocess for better OCR (grayscale + threshold)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Run OCR
text = pytesseract.image_to_string(thresh, lang="eng")

# Split into lines and filter
lines = [line.strip() for line in text.split("\n") if line.strip()]

# Extract rows (heuristic parsing)
data = []
i = 0
while i < len(lines):
    line = lines[i]
    if "I studied" in line:
        # Example: "riddelhx I studied Swablu’s Roosting Sleep!"
        parts = line.split("I studied")
        username = parts[0].strip()
        studied = parts[1].replace("!", "").strip()

        # Next line should contain reward
        reward = None
        if i+1 < len(lines) and "Reward" in lines[i+1]:
            reward_line = lines[i+1]
            reward = reward_line.replace("Reward", "").strip()

        data.append([username, studied, reward])
    i += 1

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Username", "Studied", "Reward"])

print(df)
