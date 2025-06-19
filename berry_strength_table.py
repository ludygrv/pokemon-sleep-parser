import pandas as pd

# Define levels and types
levels = [75, 60, 50, 40, 30, 20, 10, 1]
types = [
    'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
    'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
    'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
]

# Strength values extracted from the screenshots (flame-icon numbers)
strengths = {
    75: [174, 168, 193, 155, 120,  91, 168, 199, 199, 162, 118, 126, 187, 130,  94, 193, 205, 162],
    60: [120, 116, 133, 107, 116, 103, 116, 137, 137, 112, 114, 121, 129, 125,  90, 133, 142, 112],
    50: [ 94,  91, 104,  84, 101,  80,  91, 107, 107,  87, 111, 119, 101, 122,  87, 104, 111,  87],
    40: [ 73,  71,  81,  65,  79,  63,  71,  84,  84,  68, 113, 116,  79, 119,  83,  81,  86,  68],
    30: [ 57,  56,  63,  54,  61,  53,  56,  65,  65,  59, 108, 110,  61, 117,  85,  63,  68,  55],
    20: [ 47,  46,  50,  44,  49,  43,  46,  51,  51,  48, 103, 110,  49, 111,  79,  50,  53,  45],
    10: [ 37,  36,  40,  34,  39,  33,  36,  41,  41,  38,  96, 108,  39, 112,  79,  40,  42,  35],
     1: [ 28,  27,  31,  25,  30,  24,  27,  32,  32,  29,  99, 106,  30, 100,  77,  31,  33,  26]
}

# Build rows
rows = []
for lvl in levels:
    for t, s in zip(types, strengths[lvl]):
        rows.append({'Level': lvl, 'Type': t, 'Strength': s})

# Create DataFrame
df = pd.DataFrame(rows)

# Display to user
print("Berry Strength Sample Data:")
print(df)


import pandas as pd
import numpy as np

# Parameters from the fitted power-law
params = {
    'Normal':   (20.7528, 0.3786),
    'Fire':     (20.1150, 0.3793),
    'Water':    (22.6696, 0.3804),
    'Electric': (18.8902, 0.3776),
    'Grass':    (23.7735, 0.3336),
    'Ice':      (21.9922, 0.2951),
    'Fighting': (19.2727, 0.3716),
    'Poison':   (23.2548, 0.3166),
    'Ground':   (23.4298, 0.3232),
    'Flying':   (17.0189, 0.4008),
    'Psychic':  (20.0514, 0.3646),
    'Bug':      (19.1365, 0.4094),
    'Rock':     (23.6798, 0.3047),
    'Ghost':    (18.5520, 0.3765),
    'Dragon':   (33.7195, 0.2185),
    'Dark':     (22.4416, 0.3484),
    'Steel':    (23.5633, 0.2998),
    'Fairy':    (24.1318, 0.3272),
}

# Build DataFrame for levels 1-100
levels = np.arange(1, 101)
data = {'Level': levels}
for t, (a, k) in params.items():
    data[t] = np.round(a * (levels ** k), 2)

df_full = pd.DataFrame(data)

print("Full Berry Strength Table (Levels 1–100):")
print(df_full)
# tools.display_dataframe_to_user(name="Full Berry Strength Table (Levels 1–100)", dataframe=df_full)
