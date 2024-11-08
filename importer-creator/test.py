import pandas as pd
import os

# Ensure the necessary directories exist
os.makedirs("./generated/step_4/steps", exist_ok=True)

# # Define a list of possible gpc_refno values, including "1", "I.1", "II.2", etc.
# gpc_refno_values = ["1", "I.1", "II.2", "III.3", "IV.4", "V.5"]

# # Create a toy dataset with 20 rows, required columns, and some additional columns
# data = {
#     "actor_name": ["Actor" + str(i % 5 if i % 5 != 0 else "") for i in range(1, 21)],
#     "gpc_refno": [gpc_refno_values[i % len(gpc_refno_values)] for i in range(1, 21)],
#     "methodology_name": ["Methodology" + str(i % 4 + 1) for i in range(1, 21)],
#     "other_column": ["Other data " + str(i) for i in range(1, 21)],
# }

unique_combinations = [
    ("Actor1", "I.1", "Methodology1"),
    ("Actor1", "II.2", "Methodology2"),
    ("Actor1", None, "Methodology2"),
    (None, "IV.4", "Methodology4"),
    ("Actor1", "V.5", "Methodology1"),  # Missing actor name
]

# Create the dataset with 20 rows, cycling through the 5 unique combinations
data = {
    "actor_name": [unique_combinations[i % 5][0] for i in range(20)],
    "gpc_refno": [unique_combinations[i % 5][1] for i in range(20)],
    "methodology_name": [unique_combinations[i % 5][2] for i in range(20)],
    "other_column": ["Other data " + str(i) for i in range(1, 21)],
}

df = pd.DataFrame(data)

# Save the toy dataset to the expected input path
input_csv_path = "./generated/step_4/steps/extracted_methodology_name.csv"
df.to_csv(input_csv_path, index=False)

# Import the function from the module
from agents.step_4.get_emissionfactor_value_agent_step_4 import (
    get_emissionfactor_value_agent_step_4,
)

# Run the function
get_emissionfactor_value_agent_step_4()
