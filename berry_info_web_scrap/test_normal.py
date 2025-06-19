import pandas as pd
import re
import numpy as np

# SVG path data from the provided SVG element (truncated example)
d = ("M50,379.892L59.111,378.638L68.222,377.384L77.333,376.13L86.444,374.876L95.556,373.622"
     "L104.667,372.368L113.778,371.115L122.889,369.861L132,368.607L141.111,367.353L150.222,366.099"
     "L159.333,364.845L168.444,363.591L177.556,362.337L186.667,361.084L195.778,359.83L204.889,358.576"
     "L214,357.322L223.111,356.068L232.222,354.814L241.333,353.56L250.444,352.307L259.556,351.053"
     "L268.667,349.799L277.778,348.545L286.889,347.291L296,346.037L305.111,344.783L314.222,343.529"
     "L323.333,341.022L332.444,339.768L341.556,337.26L350.667,336.006L359.778,333.498L368.889,332.245"
     "L378,329.737L387.111,327.229L396.222,324.721L405.333,323.467L414.444,320.96L423.556,318.452"
     "L432.667,315.944L441.778,313.437L450.889,310.929L460,308.421L469.111,305.913L478.222,303.406"
     "L487.333,299.644L496.444,297.136L505.556,294.628L514.667,290.867L523.778,288.359L532.889,284.598"
     "L542,282.09L551.111,278.328L560.222,274.567L569.333,272.059L578.444,268.297L587.556,264.536"
     "L596.667,260.774L605.778,257.012L614.889,253.251L624,248.235L633.111,244.474L642.222,240.712"
     "L651.333,235.697L660.444,231.935L669.556,226.92L678.667,221.904L687.778,216.889L696.889,211.873"
     "L706,206.858L715.111,201.842L724.222,196.827L733.333,191.811L742.444,185.542L751.556,180.526"
     "L760.667,174.257L769.778,167.988L778.889,161.718L788,155.449L797.111,149.18L806.222,142.91"
     "L815.333,135.387L824.444,129.118L833.556,121.594L842.667,114.071L851.778,106.548L860.889,99.025"
     "L870,91.502L879.111,82.724L888.222,75.201L897.333,66.424L906.444,57.647L915.556,48.87"
     "L924.667,38.839L933.778,30.062L942.889,20.031L952,10")

# Parse path into list of (x, y) floats
coords = re.findall(r'[ML]([\d\.]+),([\d\.]+)', d)
coords = [(float(x), float(y)) for x, y in coords]

# Mapping parameters
x_min, x_max = 50, 952  # pixel range maps to level 1-100
y_min, y_max = 415, 10  # pixel range maps to value 0-323

# Convert coords to level and strength
data = []
for x, y in coords:
    level = 1 + (x - x_min) / (x_max - x_min) * 99  # continuous level
    strength = (y_min - y) / (y_min - y_max) * 323
    data.append((level, strength))

# Interpolate to integer levels 1-100
levels = np.arange(1, 101)
strengths = np.interp(levels, [pt[0] for pt in data], [pt[1] for pt in data])

# Create DataFrame
df = pd.DataFrame({
    "Level": levels,
    "Strength": np.round(strengths, 2)
})
print("Extracted Strength from SVG")
print(df)
# import ace_tools as tools; tools.display_dataframe_to_user(name="Extracted Strength from SVG", dataframe=df)
