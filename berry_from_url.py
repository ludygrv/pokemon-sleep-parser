import re
import requests
import pandas as pd

# 1. Fetch a sample page to discover the BUILD_ID
sample_resp = requests.get("https://pks.raenonx.cc/en/berry/1")
sample_html = sample_resp.text

# Use regex to find the Next.js data URL pattern
m = re.search(r'/_next/data/([^/]+)/en/berry/1\.json', sample_html)
if not m:
    raise RuntimeError("Could not find BUILD_ID in page HTML")
build_id = m.group(1)
print(f"Detected Next.js BUILD_ID: {build_id}")

# 2. Berry ID → Type mapping
BERRY_TYPES = {
    1: "Normal",   2: "Fire",    3: "Water",   4: "Electric",
    5: "Grass",    6: "Ice",     7: "Fighting",8: "Poison",
    9: "Ground",  10: "Flying", 11: "Psychic",12: "Bug",
   13: "Rock",    14: "Ghost",  15: "Dragon", 16: "Dark",
   17: "Steel",   18: "Fairy"
}

# 3. Build DataFrame for levels 1-100
levels = list(range(1, 101))
df = pd.DataFrame({"Level": levels})

# 4. Loop through berries and fetch JSON
for berry_id, ptype in BERRY_TYPES.items():
    url = f"https://pks.raenonx.cc/_next/data/{build_id}/en/berry/{berry_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    # Navigate the JSON
    levels_data = data["pageProps"]["berry"]["calculations"]["levels"]
    strengths = [entry["baseStrength"] for entry in levels_data]
    df[ptype] = strengths

# 5. Display and save
import ace_tools as tools; tools.display_dataframe_to_user(name="Berry Strengths Lv1-100", dataframe=df)