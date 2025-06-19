import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# 1) Berry ID → Type mapping
BERRY_TYPES = {
    1: "Normal",   2: "Fire",    3: "Water",   4: "Electric",
    5: "Grass",    6: "Ice",     7: "Fighting",8: "Poison",
    9: "Ground",  10: "Flying", 11: "Psychic",12: "Bug",
   13: "Rock",    14: "Ghost",  15: "Dragon", 16: "Dark",
   17: "Steel",   18: "Fairy"
}

def fetch_strengths_for_berry(berry_id):
    """
    Fetch levels 1–60 strength values by parsing the Next.js JSON blob.
    """
    url = f"https://pks.raenonx.cc/en/berry/{berry_id}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    # Parse the full HTML
    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for the Next.js payload
    data_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})
    if not data_tag:
        raise RuntimeError("❌ Could not find the __NEXT_DATA__ script tag")

    # Safely load the JSON
    try:
        full_json = json.loads(data_tag.string)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"❌ JSON decode failed: {e}")

    # Drill into the page props
    # We’ll try both common paths under props.pageProps and props.initialState
    levels_data = None
    try:
        levels_data = full_json["props"]["pageProps"]["berry"]["calculations"]["levels"]
    except (KeyError, TypeError):
        try:
            levels_data = full_json["props"]["initialState"]["berryCalc"]["levels"]
        except (KeyError, TypeError):
            # Dump top-level keys for debugging
            raise RuntimeError(
                "❌ Unexpected JSON structure. Top-level keys are: "
                + ", ".join(full_json.get("props", {}).keys())
            )

    # Ensure we have at least 60 entries
    if not isinstance(levels_data, list) or len(levels_data) < 60:
        raise RuntimeError(f"❌ Got {len(levels_data)} levels, expected ≥60")

    # Extract the flame-icon baseStrength
    return [entry.get("baseStrength") for entry in levels_data[:60]]

# Build the full table
levels = list(range(1, 61))
df = pd.DataFrame({"Level": levels})

for berry_id, ptype in BERRY_TYPES.items():
    try:
        strengths = fetch_strengths_for_berry(berry_id)
    except Exception as e:
        print(f"⚠️  Failed to fetch {ptype} (ID={berry_id}): {e}")
        strengths = [None] * 60
    time.sleep(0.1)
    df[ptype] = strengths

# Save out
df.to_csv("berry_strengths_lvl1-60_exact.csv", index=False)
print("✅ Generated berry_strengths_lvl1-60_exact.csv!")
print(df.head())
