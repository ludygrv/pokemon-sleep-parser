from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

def fetch_svg_strengths(berry_id):
    session = HTMLSession()
    # 1) GET + render JavaScript  
    r = session.get(f"https://pks.raenonx.cc/en/berry/{berry_id}")
    r.html.render(timeout=20)    # ← wait for React to draw the chart

    # 2) Extract the SVG HTML
    svg_html = r.html.find("svg.recharts-surface", first=True).html
    session.close()

    # 3) Parse out the path 'd' attribute
    soup = BeautifulSoup(svg_html, "html.parser")
    path = soup.select_one("path.recharts-line-curve")["d"]

    # 4) Extract coordinate pairs
    coords = re.findall(r'[ML]([\d\.]+),([\d\.]+)', path)
    coords = [(float(x), float(y)) for x, y in coords]

    # 5) Map pixel→data (same as before)
    x_min, x_max = 50, 952   # SVG px → Level 1–100
    y_min, y_max = 415, 10   # SVG px → Strength 0–323

    data = []
    for x, y in coords:
        level = 1 + (x - x_min)/(x_max - x_min)*99
        strength = (y_min - y)/(y_min - y_max)*323
        data.append((level, strength))

    # 6) Interpolate to integer levels
    levels = np.arange(1, 101)
    strengths = np.interp(levels, [pt[0] for pt in data], [pt[1] for pt in data])
    strengths = np.round(strengths, 2)

    return pd.DataFrame({"Level": levels, "Strength": strengths})

# Example: Leppa Berry (ID=2)
df_leppa = fetch_svg_strengths(2)
print(df_leppa.head())